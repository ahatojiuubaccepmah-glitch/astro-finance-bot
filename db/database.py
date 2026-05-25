import sqlite3


def get_connection():
    return sqlite3.connect("bot.db")


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ пользователи
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        birth_date TEXT,
        birth_time TEXT,
        city TEXT,
        lat REAL,
        lon REAL,
        timezone TEXT
    )
    """)

    # ✅ города
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        name TEXT PRIMARY KEY,
        lat REAL,
        lon REAL
    )
    """)

    conn.commit()
    conn.close()


def save_user(user_id, birth_date, birth_time, city, lat, lon, timezone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (user_id, birth_date, birth_time, city, lat, lon, timezone)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        birth_date=excluded.birth_date,
        birth_time=excluded.birth_time,
        city=excluded.city,
        lat=excluded.lat,
        lon=excluded.lon,
        timezone=excluded.timezone
    """, (user_id, birth_date, birth_time, city, lat, lon, timezone))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT birth_date, birth_time, city, lat, lon, timezone
        FROM users WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "birth_date": result[0],
            "birth_time": result[1],
            "city": result[2],
            "lat": result[3],
            "lon": result[4],
            "timezone": result[5]
        }

    return None


def get_city(city_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT lat, lon FROM cities WHERE name = ?", (city_name,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return {"lat": result[0], "lon": result[1]}

    return None


def save_city(city_name, lat, lon):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO cities (name, lat, lon)
    VALUES (?, ?, ?)
    """, (city_name, lat, lon))

    conn.commit()
    conn.close()