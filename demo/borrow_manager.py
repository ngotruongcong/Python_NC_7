# borrow_manager.py
from database import get_db_connection

def borrow_book(reader_id, book_id, borrow_date, return_date):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO borrows (reader_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (reader_id, book_id, borrow_date, return_date))
    connection.commit()
    cursor.close()
    connection.close()

def return_book(reader_id, book_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM borrows WHERE reader_id = %s AND book_id = %s"
    cursor.execute(query, (reader_id, book_id))
    connection.commit()
    cursor.close()
    connection.close()
