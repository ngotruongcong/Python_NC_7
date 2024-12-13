# database.py
import mysql.connector
from config import MYSQL_CONFIG

def initialize_database():
    try:
        # Kết nối tới MySQL server (chưa cần chọn database)
        connection = mysql.connector.connect(
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            host=MYSQL_CONFIG["host"]
        )
        cursor = connection.cursor()

        # Tạo database nếu chưa tồn tại
        cursor.execute("CREATE DATABASE IF NOT EXISTS library_management;")
        print("Database 'library_management' đã được tạo (nếu chưa tồn tại).")

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Lỗi khi tạo database: {err}")

def get_db_connection():
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    return connection

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Tạo các bảng nếu chúng chưa tồn tại
    cursor.execute("""
        CREATE DATABASE IF NOT EXISTS library_management;
    """)
    
    cursor.execute("""
        USE library_management;
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INT PRIMARY KEY,
            book_name VARCHAR(255),
            category VARCHAR(255)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readers (
            reader_id INT PRIMARY KEY,
            reader_name VARCHAR(255)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrows (
            borrow_id INT PRIMARY KEY AUTO_INCREMENT,
            reader_id INT,
            book_id INT,
            borrow_date DATE,
            return_date DATE,
            FOREIGN KEY (reader_id) REFERENCES readers(reader_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        );
    """)

    connection.commit()
    cursor.close()
    connection.close()

