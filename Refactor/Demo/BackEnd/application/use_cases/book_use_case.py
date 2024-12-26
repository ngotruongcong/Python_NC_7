from application.interfaces.book_repository import BookRepository
from infra.repositories.book_repo import MySQLBookRepository
from api.schemas.book_schema import BookCreate

class BookUseCase:
    def __init__(self, repo: BookRepository = MySQLBookRepository()):
        self.repo = repo

    def get_all_books(self):
        return self.repo.get_all_books()

    def add_book(self, book: BookCreate):
        self.repo.add_book(book)
