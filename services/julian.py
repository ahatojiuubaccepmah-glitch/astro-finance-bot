from datetime import datetime


def to_julian_date(dt: datetime) -> float:
    """
    Конвертация datetime (UTC) → Julian Date
    """

    year = dt.year
    month = dt.month
    day = dt.day

    hour = dt.hour
    minute = dt.minute
    second = dt.second

    # ✅ дробная часть дня
    day_fraction = (hour + minute / 60 + second / 3600) / 24

    # ✅ корректировка для января/февраля
    if month <= 2:
        year -= 1
        month += 12

    A = int(year / 100)
    B = 2 - A + int(A / 4)

    jd = int(365.25 * (year + 4716)) \
         + int(30.6001 * (month + 1)) \
         + day + B - 1524.5

    return jd + day_fraction