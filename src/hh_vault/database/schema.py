from .db import get_connection


def create_tables():
    """Создаёт таблицы companies и vacancies, если они ещё не существуют."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            hh_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            url TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            hh_id INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            url TEXT,
            salary_from INTEGER,
            salary_to INTEGER,
            currency TEXT,
            employer_id INTEGER NOT NULL,
            FOREIGN KEY (employer_id) REFERENCES companies(hh_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("🐀 Таблицы успешно созданы.")
