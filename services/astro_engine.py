from datetime import datetime

from services.astrology import calculate_chart
from services.houses import calculate_houses
from services.planet_houses import assign_planets_to_houses


def build_natal_chart(dt: datetime, lat: float, lon: float):
    """
    Главная функция Astro Engine (по ТЗ)
    """

    # ✅ планеты + аспекты
    chart = calculate_chart(dt)

    planets = chart["planets"]
    aspects = chart["aspects"]

    # ✅ дома
    houses = calculate_houses(dt, lat, lon)

    # ✅ привязка планет к домам
    planets_with_houses = assign_planets_to_houses(planets, houses)

    return {
        "planets": planets_with_houses,
        "houses": houses,
        "aspects": aspects
    }