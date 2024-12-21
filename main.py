import tkinter as tk
from tkinter import ttk
from book_manager import BookManagerScreen  # Import class từ file book_manager.py
from reader_manager import ReaderManagerScreen  # Import class từ file reader_manager.py
from borrow_manager import BorrowManagerScreen  # Import class từ file borrow_manager.py
from database import create_tables, initialize_database

class LibraryManagementScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý thư viện")
        self.root.geometry("800x600")
        
        initialize_database()
        create_tables()
        self.create_dashboard()

    def create_dashboard(self):
        # Màn hình Dashboard
        self.dashboard_frame = ttk.Frame(self.root)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

        self.book_management_button = tk.Button(self.dashboard_frame, text="Quản lý sách", command=self.book_manager)
        self.book_management_button.grid(row=0, column=0, padx=10)

        self.reader_management_button = tk.Button(self.dashboard_frame, text="Quản lý độc giả", command=self.manage_readers)
        self.reader_management_button.grid(row=0, column=1, padx=10)

        self.borrow_management_button = tk.Button(self.dashboard_frame, text="Quản lý mượn sách", command=self.manage_borrows)
        self.borrow_management_button.grid(row=1, column=0, padx=10)

        self.report_button = tk.Button(self.dashboard_frame, text="Thông kê", command=self.generate_report)
        self.report_button.grid(row=1, column=1, padx=10)

    def book_manager(self):
        # Ẩn các widget hiện tại của main screen
        for widget in self.dashboard_frame.winfo_children():
            widget.grid_forget()

        # Khởi tạo màn hình quản lý sách và hiển thị nó
        book_manager_screen = BookManagerScreen(self.root)

    def manage_readers(self):
         # Ẩn các widget hiện tại của main screen
        for widget in self.dashboard_frame.winfo_children():
            widget.grid_forget()

        # Khởi tạo màn hình quản lý sách và hiển thị nó
        book_manager_screen = ReaderManagerScreen(self.root)

    def manage_borrows(self):
         # Ẩn các widget hiện tại của main screen
        for widget in self.dashboard_frame.winfo_children():
            widget.grid_forget()

        # Khởi tạo màn hình quản lý sách và hiển thị nó
        book_manager_screen = BorrowManagerScreen(self.root)

    def generate_report(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementScreen(root)
    root.mainloop()
