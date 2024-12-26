from tkinter import Tk, Button
from tkinter import ttk
from tkinter.font import Font
import tkinter as tk
from tkinter import ttk
from book_manager import BookManagerScreen  # Import class từ file book_manager.py
from reader_manager import ReaderManagerScreen  # Import class từ file reader_manager.py
from borrow_manager import BorrowManagerScreen  # Import class từ file borrow_manager.py
from library_statistics import LibraryStatisticsScreen # Import class từ file library_statistics.py
from database import initialize_database

class LibraryManagementScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý thư viện")
        self.root.geometry("800x600")
        initialize_database()
        self.create_dashboard()
    def create_fonts(self):
        # Font tùy chỉnh
        self.header_font = Font(family="Arial", size=14, weight="bold")
        self.button_font = Font(family="Arial", size=10, weight="bold")
        self.label_bg_color = "#f7f7f7"

    def create_dashboard(self):
       # Áp dụng style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.create_fonts()

        # Màn hình Dashboard
        self.dashboard_frame = ttk.Frame(self.root, padding=(20, 20))
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

        # Căn chỉnh lưới
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_rowconfigure((0, 1), weight=1)
        self.dashboard_frame.grid_columnconfigure((0, 1), weight=1)

        # Nút Quản lý sách
        self.book_management_button = Button(
            self.dashboard_frame,
            text="Quản lý sách",
            command=self.book_manager,
            font=self.button_font,
            bg="#4CAF50",  # Màu xanh lá
            fg="white",
            activebackground="#45a049",
            padx=20, pady=10
        )
        self.book_management_button.grid(row=0, column=0, padx=20, pady=20)

        # Nút Quản lý độc giả
        self.reader_management_button = Button(
            self.dashboard_frame,
            text="Quản lý độc giả",
            command=self.manage_readers,
            font=self.button_font,
            bg="#2196F3",  # Màu xanh dương
            fg="white",
            activebackground="#1976D2",
            padx=20, pady=10
        )
        self.reader_management_button.grid(row=0, column=1, padx=20, pady=20)

        # Nút Quản lý mượn sách
        self.borrow_management_button = Button(
            self.dashboard_frame,
            text="Quản lý mượn sách",
            command=self.manage_borrows,
            font=self.button_font,
            bg="#FFC107",  # Màu vàng
            fg="black",
            activebackground="#FFA000",
            padx=20, pady=10
        )
        self.borrow_management_button.grid(row=1, column=0, padx=20, pady=20)

        # Nút Thống kê
        self.report_button = Button(
            self.dashboard_frame,
            text="Thống kê",
            command=self.generate_report,
            font=self.button_font,
            bg="#F44336",  # Màu đỏ
            fg="white",
            activebackground="#D32F2F",
            padx=20, pady=10
        )
        self.report_button.grid(row=1, column=1, padx=20, pady=20)
    def book_manager(self):
        self.dashboard_frame.destroy()
        # # Khởi tạo màn hình quản lý sách và hiển thị nó
        self.book_manager_screen = BookManagerScreen(self.root)
    def manage_readers(self):
        self.dashboard_frame.destroy()

        # Khởi tạo màn hình quản lý sách và hiển thị nó
        reader_manager_screen = ReaderManagerScreen(self.root)
    def manage_borrows(self):
        self.dashboard_frame.destroy()
        

        # Khởi tạo màn hình quản lý sách và hiển thị nó
        borrow_manager_screen = BorrowManagerScreen(self.root)
    def generate_report(self):
        self.dashboard_frame.destroy()
        self.statics_manager_screen = LibraryStatisticsScreen(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementScreen(root)
    root.mainloop()
