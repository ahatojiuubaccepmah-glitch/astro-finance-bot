import swisseph as swe
from datetime import datetime


# ✅ путь к эфемеридам (можно оставить пустым)
swe.set_ephe_path(".")


PLANETS = {
    "Sun ☀️": swe.SUN,
    "Moon 🌙": swe.MOON,
    "Mercury ☿": swe.MERCURY,
    "Venus ♀": swe.VENUS,
    "Mars ♂": swe.MARS,
    "Jupiter ♃": swe.JUPITER,
    "Saturn ♄": swe.SATURN,
}


ZODIAC_SIGNS = [
    "Овен ♈",
    "Телец ♉",
    "Близнецы ♊",
    "Рак ♋",
    "Лев ♌",
    "Дева ♍",
    "Весы ♎",
    "Скорпион ♏",
    "Стрелец ♐",
    "Козерог ♑",
    "Водолей ♒",
    "Рыбы ♓"
]


ASPECTS = {
    0: "Соединение ☌",
    60: "Секстиль ✶",
    90: "Квадрат □",
    120: "Тригон △",
    180: "Оппозиция ☍"
}


# ✅ JD из datetime
def datetime_to_jd(dt: datetime):
    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60 + dt.second / 3600
    )


# ✅ знак зодиака
def get_sign(degree):
    return ZODIAC_SIGNS[int(degree // 30)]


# ✅ все планеты
def get_planets(dt: datetime):
    jd = datetime_to_jd(dt)

    planets = {}

    for name, planet_id in PLANETS.items():
        pos = swe.calc_ut(jd, planet_id)[0][0]

        planets[name] = {
            "degree": pos,
            "sign": get_sign(pos)
        }

    return planets


# ✅ аспекты
def calculate_aspects(planets):
    aspects_found = []

    names = list(planets.keys())

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1 = names[i]
            p2 = names[j]

            d1 = planets[p1]["degree"]
            d2 = planets[p2]["degree"]

            diff = abs(d1 - d2)
            if diff > 180:
                diff = 360 - diff

            for aspect_angle in ASPECTS:
                if abs(diff - aspect_angle) <= 6:  # орбис
                    aspects_found.append(
                        f"{p1} — {p2}: {ASPECTS[aspect_angle]}"
                    )

    return aspects_found


# ✅ главный метод
def calculate_chart(dt: datetime):
    planets = get_planets(dt)
    aspects = calculate_aspects(planets)

    return {
        "planets": planets,
        "aspects": aspects
    }