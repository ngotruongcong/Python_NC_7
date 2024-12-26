import requests

class LibraryController:
    BASE_URL = "http://127.0.0.1:8000/api/books"

    def get_books(self):
        response = requests.get(self.BASE_URL)
        return response.json()

    def add_book(self, title, author):
        requests.post(self.BASE_URL, json={"title": title, "author": author})
