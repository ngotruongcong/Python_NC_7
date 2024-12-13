# book_manager.py
from database import get_db_connection

def add_book(book_id, book_name, category):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO books (book_id, book_name, category) VALUES (%s, %s, %s)"
    cursor.execute(query, (book_id, book_name, category))
    connection.commit()
    cursor.close()
    connection.close()

def update_book(book_id, book_name, category):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE books SET book_name = %s, category = %s WHERE book_id = %s"
    cursor.execute(query, (book_name, category, book_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_book(book_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    connection.commit()
    cursor.close()
    connection.close()
