import mysql.connector
from shared.config import DATABASE_CONFIG

def get_db():
    return mysql.connector.connect(**DATABASE_CONFIG)

def create_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255)
        )
    """)
    db.commit()
