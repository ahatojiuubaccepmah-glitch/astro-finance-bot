import sqlite3


def get_connection():
    return sqlite3.connect("bot.db")


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # ✅ города (главная таблица гео)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        name TEXT PRIMARY KEY,
        lat REAL,
        lon REAL,
        timezone TEXT
    )
    """)

    # ✅ пользователи
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        birth_date TEXT,
        birth_time TEXT,
        city_name TEXT
    )
    """)

    conn.commit()
    conn.close()


# ✅ сохранить/обновить пользователя
def save_user(user_id, birth_date, birth_time, city_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (user_id, birth_date, birth_time, city_name)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        birth_date=excluded.birth_date,
        birth_time=excluded.birth_time,
        city_name=excluded.city_name
    """, (user_id, birth_date, birth_time, city_name))

    conn.commit()
    conn.close()


# ✅ получить пользователя
def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT birth_date, birth_time, city_name
        FROM users WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "birth_date": result[0],
            "birth_time": result[1],
            "city_name": result[2]
        }

    return None


# ✅ получить город
def get_city(city_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lat, lon, timezone 
        FROM cities WHERE name = ?
    """, (city_name,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "lat": result[0],
            "lon": result[1],
            "timezone": result[2]
        }

    return None


# ✅ сохранить город
def save_city(city_name, lat, lon, timezone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO cities (name, lat, lon, timezone)
    VALUES (?, ?, ?, ?)
    """, (city_name, lat, lon, timezone))

    conn.commit()
    conn.close()