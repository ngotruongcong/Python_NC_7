# reader_manager.py
from database import get_db_connection

def add_reader(reader_id, reader_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO readers (reader_id, reader_name) VALUES (%s, %s)"
    cursor.execute(query, (reader_id, reader_name))
    connection.commit()
    cursor.close()
    connection.close()

def update_reader(reader_id, reader_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE readers SET reader_name = %s WHERE reader_id = %s"
    cursor.execute(query, (reader_name, reader_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_reader(reader_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM readers WHERE reader_id = %s"
    cursor.execute(query, (reader_id,))
    connection.commit()
    cursor.close()
    connection.close()
