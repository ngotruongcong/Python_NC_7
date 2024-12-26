from fastapi import APIRouter
from api.schemas.book_schema import BookCreate
from application.use_cases.book_use_case import BookUseCase

router = APIRouter(prefix="/api/books", tags=["Books"])
book_use_case = BookUseCase()

@router.get("/")
def get_books():
    return book_use_case.get_all_books()

@router.post("/")
def create_book(book: BookCreate):
    book_use_case.add_book(book)
    return {"message": "Book added successfully"}
