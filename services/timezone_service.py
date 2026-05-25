from timezonefinder import TimezoneFinder


tf = TimezoneFinder()


def get_timezone(lat: float, lon: float) -> str:
    timezone = tf.timezone_at(lat=lat, lng=lon)

    if not timezone:
        return "UTC"

    return timezone
