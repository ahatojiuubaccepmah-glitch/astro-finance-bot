import sqlite3


# ✅ подключение к базе
def get_connection():
    return sqlite3.connect("bot.db")


# ✅ создание таблицы
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        birth_date TEXT,
        birth_time TEXT,
        city TEXT
    )
    """)

    conn.commit()
    conn.close()


# ✅ сохранить пользователя
def save_user(user_id: int, birth_date: str, birth_time: str, city: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (user_id, birth_date, birth_time, city)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        birth_date=excluded.birth_date,
        birth_time=excluded.birth_time,
        city=excluded.city
    """, (user_id, birth_date, birth_time, city))

    conn.commit()
    conn.close()


# ✅ получить пользователя
def get_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT birth_date, birth_time, city FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return {
            "birth_date": result[0],
            "birth_time": result[1],
            "city": result[2]
        }

    return None
