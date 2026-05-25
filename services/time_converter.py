from datetime import datetime
import pytz


def convert_to_utc(date_str: str, time_str: str, timezone_str: str):
    try:
        # ✅ создаём datetime без timezone
        dt_naive = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

        # ✅ берём timezone
        tz = pytz.timezone(timezone_str)

        # ✅ локализуем (учитывает DST автоматически)
        dt_local = tz.localize(dt_naive, is_dst=None)

        # ✅ перевод в UTC
        dt_utc = dt_local.astimezone(pytz.utc)

        return {
            "utc_time": dt_utc.strftime("%H:%M"),
            "utc_date": dt_utc.strftime("%d.%m.%Y"),
            "datetime": dt_utc,
            "offset": dt_local.utcoffset().total_seconds() / 3600
        }

    # ✅ случай: двусмысленное время (например переход времени)
    except pytz.AmbiguousTimeError:
        return {"error": "ambiguous_time"}

    # ✅ случай: несуществующее время (перевод часов вперёд)
    except pytz.NonExistentTimeError:
        return {"error": "non_existent_time"}

    except Exception:
        return None
``