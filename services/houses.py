import swisseph as swe
from datetime import datetime


# ✅ JD
def datetime_to_jd(dt: datetime):
    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60 + dt.second / 3600
    )


# ✅ знак зодиака (формат по ТЗ)
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


def format_degree(degree):
    sign_index = int(degree // 30)
    sign_degree = degree % 30
    return f"{sign_degree:.1f}° {ZODIAC_SIGNS[sign_index]}"


# ✅ ДОМА (Placidus)
def calculate_houses(dt: datetime, lat: float, lon: float):
    jd = datetime_to_jd(dt)

    # ✅ Placidus = 'P'
    houses, ascmc = swe.houses(jd, lat, lon, b'P')

    result = {}

    # ✅ 12 домов
    for i in range(12):
        result[f"House {i+1}"] = {
            "degree": houses[i],
            "formatted": format_degree(houses[i])
        }

    # ✅ ASC и MC
    result["ASC"] = {
        "degree": ascmc[0],
        "formatted": format_degree(ascmc[0])
    }

    result["MC"] = {
        "degree": ascmc[1],
        "formatted": format_degree(ascmc[1])
    }

    return result