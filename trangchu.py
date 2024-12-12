import tkinter as tk
from tkinter import messagebox
import mysql.connector

def connect_to_db():
    """Kết nối đến cơ sở dữ liệu MySQL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Thay bằng tài khoản MySQL của bạn
            password="dong10082003",  # Thay bằng mật khẩu MySQL của bạn
            port=3306
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Không thể kết nối đến cơ sở dữ liệu: {err}")
        return None

def create_database():
    """Tạo cơ sở dữ liệu nếu chưa tồn tại."""
    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS LibraryDB")
            cursor.close()
            conn.close()
            messagebox.showinfo("Thông báo", "Database 'LibraryDB' đã được tạo thành công hoặc đã tồn tại!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Không thể tạo cơ sở dữ liệu: {err}")

def open_book_management():
    """Mở cửa sổ quản lý sách."""
    messagebox.showinfo("Quản lý Sách", "Chức năng Quản lý Sách đang được phát triển.")

def open_reader_management():
    """Mở cửa sổ quản lý độc giả."""
    messagebox.showinfo("Quản lý Độc giả", "Chức năng Quản lý Độc giả đang được phát triển.")

def open_borrow_return_management():
    """Mở cửa sổ quản lý mượn trả sách."""
    messagebox.showinfo("Quản lý Mượn Trả", "Chức năng Quản lý Mượn Trả đang được phát triển.")

def open_statistics():
    """Mở cửa sổ thống kê."""
    messagebox.showinfo("Thống kê", "Chức năng Thống kê đang được phát triển.")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x400")

# Tiêu đề chính
title_label = tk.Label(root, text="Dashboard", font=("Arial", 16))
title_label.pack(pady=10)

# Các nút chức năng
frame = tk.Frame(root)
frame.pack(pady=20)

btn_book = tk.Button(frame, text="Quản lý Sách", width=20, command=open_book_management)
btn_book.grid(row=0, column=0, padx=10, pady=10)

btn_reader = tk.Button(frame, text="Quản lý Độc giả", width=20, command=open_reader_management)
btn_reader.grid(row=0, column=1, padx=10, pady=10)

btn_borrow_return = tk.Button(frame, text="Quản lý Mượn Trả Sách", width=20, command=open_borrow_return_management)
btn_borrow_return.grid(row=1, column=0, padx=10, pady=10)

btn_statistics = tk.Button(frame, text="Thống kê", width=20, command=open_statistics)
btn_statistics.grid(row=1, column=1, padx=10, pady=10)

# Tạo cơ sở dữ liệu khi chạy chương trình
create_database()

# Kết nối cơ sở dữ liệu khi chạy chương trình
conn = connect_to_db()
if conn:
    try:
        conn.database = "LibraryDB"  # Chọn database vừa tạo
        messagebox.showinfo("Thông báo", "Kết nối cơ sở dữ liệu thành công!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Không thể chọn cơ sở dữ liệu: {err}")

# Chạy vòng lặp giao diện
root.mainloop()

# Đóng kết nối cơ sở dữ liệu khi thoát
if conn:
    conn.close()