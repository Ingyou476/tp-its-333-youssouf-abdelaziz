import sqlite3

def init_db():
    conn = sqlite3.connect("sante.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            adresse TEXT,
            pin TEXT
        )
    """)
    conn.commit()
    conn.close()
