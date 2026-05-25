def get_house(degree, houses):
    """
    Определяет, в каком доме находится планета
    """

    house_degrees = [houses[f"House {i}"]["degree"] for i in range(1, 13)]

    for i in range(12):
        start = house_degrees[i]
        end = house_degrees[(i + 1) % 12]

        # случай перехода через 360°
        if start > end:
            if degree >= start or degree < end:
                return i + 1
        else:
            if start <= degree < end:
                return i + 1

    return None


def assign_planets_to_houses(planets, houses):
    result = {}

    for planet_name, data in planets.items():
        degree = data["degree"]
        house = get_house(degree, houses)

        result[planet_name] = {
            "degree": degree,
            "sign": data["sign"],
            "house": house
        }

    return result