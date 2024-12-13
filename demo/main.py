# main.py
import tkinter as tk
from tkinter import messagebox
from book_manager import add_book, update_book, delete_book
from reader_manager import add_reader, update_reader, delete_reader
from borrow_manager import borrow_book, return_book
from report_generator import generate_report
from database import create_tables, initialize_database

class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý thư viện")
        self.root.geometry("800x600")
        initialize_database()
        create_tables()
        self.create_dashboard()

    def create_dashboard(self):
        # Màn hình Dashboard
        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack(pady=20)

        self.book_management_button = tk.Button(self.dashboard_frame, text="Quản lý sách", command=self.manage_books)
        self.book_management_button.grid(row=0, column=0, padx=10)

        self.reader_management_button = tk.Button(self.dashboard_frame, text="Quản lý độc giả", command=self.manage_readers)
        self.reader_management_button.grid(row=0, column=1, padx=10)

        self.borrow_management_button = tk.Button(self.dashboard_frame, text="Quản lý mượn sách", command=self.manage_borrows)
        self.borrow_management_button.grid(row=1, column=0, padx=10)

        self.report_button = tk.Button(self.dashboard_frame, text="Thông kê", command=self.generate_report)
        self.report_button.grid(row=1, column=1, padx=10)

    def manage_books(self):
        pass  # Hiển thị giao diện quản lý sách

    def manage_readers(self):
        pass  # Hiển thị giao diện quản lý độc giả

    def manage_borrows(self):
        pass  # Hiển thị giao diện quản lý mượn sách

    def generate_report(self):
        generate_report()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()
