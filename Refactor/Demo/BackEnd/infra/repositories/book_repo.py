from application.interfaces.book_repository import BookRepository
from api.schemas.book_schema import BookCreate
from infra.database.db_connection import get_db

class MySQLBookRepository(BookRepository):
    def get_all_books(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT title, author FROM books")
        rows = cursor.fetchall()
        return [{"title": row[0], "author": row[1]} for row in rows]

    def add_book(self, book: BookCreate):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (book.title, book.author))
        db.commit()
