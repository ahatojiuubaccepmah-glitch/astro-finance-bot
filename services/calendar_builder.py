from datetime import datetime, timedelta
from calendar import monthrange

from services.finance_engine import build_finance_analysis


def build_month_calendar(chart, year: int, month: int):
    """
    Генерация календаря на месяц

    вход:
    - chart (natal chart)
    - год
    - месяц

    выход:
    [
        {
            "day": int,
            "score": float,
            "color": str
        }
    ]
    """

    days_in_month = monthrange(year, month)[1]

    result = []

    for day in range(1, days_in_month + 1):
        dt = datetime(year, month, day, 12, 0)  # фиксируем время

        analysis = build_finance_analysis(chart, dt)

        result.append({
            "day": day,
            "score": analysis["score"],
            "color": analysis["color"]
        })

    return result