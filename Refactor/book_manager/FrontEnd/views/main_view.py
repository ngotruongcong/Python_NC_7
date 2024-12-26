import tkinter as tk
from controllers.library_controller import LibraryController

class MainView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.controller = LibraryController()

        # UI Components
        self.book_list = tk.Listbox(self.root, width=50, height=20)
        self.book_list.pack()

        tk.Button(self.root, text="Add Book", command=self.add_book).pack()
        tk.Button(self.root, text="Load Books", command=self.load_books).pack()

    def run(self):
        self.root.mainloop()

    def add_book(self):
        self.controller.add_book("New Book", "Author Name")
        self.load_books()

    def load_books(self):
        books = self.controller.get_books()
        self.book_list.delete(0, tk.END)
        for book in books:
            self.book_list.insert(tk.END, f"{book['title']} by {book['author']}")
