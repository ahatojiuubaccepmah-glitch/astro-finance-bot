import swisseph as swe
from datetime import datetime


# ✅ Управители знаков (по ТЗ)
RULERS = {
    "Овен ♈": "Mars ♂",
    "Телец ♉": "Venus ♀",
    "Близнецы ♊": "Mercury ☿",
    "Рак ♋": "Moon 🌙",
    "Лев ♌": "Sun ☀️",
    "Дева ♍": "Mercury ☿",
    "Весы ♎": "Venus ♀",
    "Скорпион ♏": "Mars ♂",
    "Стрелец ♐": "Jupiter ♃",
    "Козерог ♑": "Saturn ♄",
    "Водолей ♒": "Saturn ♄",
    "Рыбы ♓": "Jupiter ♃",
}


# ✅ Транзитные планеты
TRANSIT_PLANETS = {
    "Sun ☀️": swe.SUN,
    "Moon 🌙": swe.MOON,
    "Mercury ☿": swe.MERCURY,
    "Venus ♀": swe.VENUS,
    "Mars ♂": swe.MARS
}


# ✅ Аспекты → score
ASPECTS = {
    0: 2,      # соединение
    60: 1,     # секстиль
    90: -0.5,  # квадрат
    120: 2,    # тригон
    180: -0.5  # оппозиция
}


# ✅ Орбисы (по ТЗ)
ORBIS = {
    "Sun ☀️": 10,
    "Moon 🌙": 9,
    "Jupiter ♃": 7
}


# ✅ Получить знак по градусу
def get_sign_from_degree(degree: float):
    signs = [
        "Овен ♈", "Телец ♉", "Близнецы ♊", "Рак ♋",
        "Лев ♌", "Дева ♍", "Весы ♎", "Скорпион ♏",
        "Стрелец ♐", "Козерог ♑", "Водолей ♒", "Рыбы ♓"
    ]
    return signs[int(degree // 30)]


# ✅ Орбис по планете
def get_orbis(planet):
    return ORBIS.get(planet, 5)


# ✅ Финансовые точки (ядро)
def extract_financial_points(chart):
    houses = chart["houses"]
    planets = chart["planets"]

    # 2 дом
    house_2_degree = houses["House 2"]["degree"]
    house_2_sign = get_sign_from_degree(house_2_degree)

    # управитель
    ruler_2 = RULERS[house_2_sign]

    # планеты во 2 доме
    planets_in_2 = [
        planet for planet, data in planets.items()
        if data["house"] == 2
    ]

    return {
        "house_2_sign": house_2_sign,
        "ruler_2": ruler_2,
        "planets_in_2": planets_in_2
    }


# ✅ Транзиты
def get_transit_positions(dt: datetime):
    jd = swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60
    )

    result = {}

    for name, pid in TRANSIT_PLANETS.items():
        degree = swe.calc_ut(jd, pid)[0][0]
        result[name] = degree

    return result


# ✅ Аспекты транзит → натал
def calculate_transit_aspects(natal_points, transit_positions):
    aspects = []

    for t_name, t_deg in transit_positions.items():
        for n_name, n_deg in natal_points.items():

            diff = abs(t_deg - n_deg)
            if diff > 180:
                diff = 360 - diff

            for angle, score in ASPECTS.items():
                if abs(diff - angle) <= get_orbis(t_name):

                    # по ТЗ: Луна = 0
                    if t_name == "Moon 🌙":
                        score = 0

                    aspects.append({
                        "transit": t_name,
                        "natal": n_name,
                        "aspect": angle,
                        "score": score
                    })

    return aspects


# ✅ Итоговый score
def calculate_score(aspects):
    return sum(a["score"] for a in aspects)


# ✅ Цвет по ТЗ
def score_to_color(score: float):
    if score >= 3:
        return "dark_green"
    elif 1 <= score < 3:
        return "light_green"
    elif score == 0:
        return "gray"
    elif score == -1:
        return "orange"
    elif score <= -2:
        return "red"
    return "gray"


# ✅ Главный метод Finance Engine
def build_finance_analysis(chart, dt: datetime):
    """
    Вход:
    - chart (результат astro_engine)
    - dt (дата для транзитов)

    Выход:
    - score
    - color
    - аспекты
    - финансовые точки
    """

    financial = extract_financial_points(chart)

    # ✅ Натальные точки
    natal_points = {}

    # управитель
    if financial["ruler_2"] in chart["planets"]:
        natal_points[financial["ruler_2"]] = chart["planets"][financial["ruler_2"]]["degree"]

    # планеты во 2 доме
    for p in financial["planets_in_2"]:
        natal_points[p] = chart["planets"][p]["degree"]

    # ✅ Транзиты
    transits = get_transit_positions(dt)

    # ✅ Аспекты
    aspects = calculate_transit_aspects(natal_points, transits)

    # ✅ Score
    score = calculate_score(aspects)

    # ✅ Цвет
    color = score_to_color(score)

    return {
        "score": score,
        "color": color,
        "aspects": aspects,
        "points": financial
    }