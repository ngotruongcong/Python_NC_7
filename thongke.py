import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
import mysql.connector
from datetime import datetime
from tkinter.filedialog import asksaveasfilename
import openpyxl


def connect_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            database="book_manager"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", f"Không thể kết nối cơ sở dữ liệu:\n{e}")
        return None

def get_statistics():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        try:
            # Tổng số lượng sách
            cursor.execute("SELECT SUM(SoLuong) FROM Sach")
            total_books = cursor.fetchone()[0] or 0
            lbl_total_books.config(text=total_books)

            # Tổng số độc giả
            cursor.execute("SELECT COUNT(*) FROM DocGia")
            total_readers = cursor.fetchone()[0] or 0
            lbl_total_readers.config(text=total_readers)

            # Số sách mượn nhưng chưa trả
            cursor.execute(""" 
                SELECT COUNT(*) 
                FROM MuonTra 
                WHERE NgayTra IS NULL
            """)
            books_not_returned_count = cursor.fetchone()[0] or 0

            # Số sách còn lại trong thư viện
            remaining_books = total_books - books_not_returned_count
            lbl_remaining_books.config(text=remaining_books)

            # Tỉ lệ trả sách đúng hạn
            cursor.execute(""" 
                SELECT COUNT(*) 
                FROM MuonTra 
                WHERE NgayTra IS NOT NULL 
                AND NgayTra <= NgayTraDuKien
            """)
            on_time_returns = cursor.fetchone()[0] or 0
            cursor.execute("SELECT COUNT(*) FROM MuonTra WHERE NgayTra IS NOT NULL")
            total_returns = cursor.fetchone()[0] or 1  # tránh chia cho 0
            return_rate = (on_time_returns / total_returns) * 100
            lbl_return_rate.config(text=f"{return_rate:.2f}%")

            # Sách đến hẹn mà chưa trả
            cursor.execute(""" 
                SELECT Sach.TenSach, DocGia.TenDocGia, MuonTra.NgayMuon, MuonTra.NgayTraDuKien 
                FROM MuonTra
                JOIN Sach ON MuonTra.MaSach = Sach.MaSach
                JOIN DocGia ON MuonTra.MaDocGia = DocGia.MaDocGia
                WHERE MuonTra.NgayTra IS NULL 
                AND MuonTra.NgayTraDuKien < %s
            """, (datetime.now().strftime('%Y-%m-%d'),))
            books_due_not_returned = cursor.fetchall()
            for item in tree_books_due_not_returned.get_children():
                tree_books_due_not_returned.delete(item)
            for book, reader, borrow_date, return_date in books_due_not_returned:
                tree_books_due_not_returned.insert("", tk.END, values=(book, reader, borrow_date, return_date))

            # Số lượng sách đến hẹn mà chưa trả
            lbl_books_due_not_returned_count.config(text=f"Số lượng: {len(books_due_not_returned)}")

            # Sách chưa trả
            cursor.execute(""" 
                SELECT Sach.TenSach, DocGia.TenDocGia, MuonTra.NgayMuon, MuonTra.NgayTraDuKien 
                FROM MuonTra
                JOIN Sach ON MuonTra.MaSach = Sach.MaSach
                JOIN DocGia ON MuonTra.MaDocGia = DocGia.MaDocGia
                WHERE MuonTra.NgayTra IS NULL
            """)
            books_not_returned = cursor.fetchall()
            for item in tree_books_not_returned.get_children():
                tree_books_not_returned.delete(item)
            for book, reader, borrow_date, return_date in books_not_returned:
                tree_books_not_returned.insert("", tk.END, values=(book, reader, borrow_date, return_date))

            # Số lượng sách chưa trả
            lbl_books_not_returned_count.config(text=f"Số lượng: {len(books_not_returned)}")

            # Sách được mượn nhiều nhất
            cursor.execute(""" 
                SELECT TenSach 
                FROM Sach
                JOIN MuonTra ON Sach.MaSach = MuonTra.MaSach
                GROUP BY TenSach
                ORDER BY COUNT(MuonTra.MaSach) DESC
                LIMIT 1
            """)
            most_borrowed_book = cursor.fetchone()
            lbl_most_borrowed_book_val.config(text=most_borrowed_book[0] if most_borrowed_book else "Không có dữ liệu")

            # Độc giả tích cực nhất
            cursor.execute(""" 
                SELECT TenDocGia 
                FROM DocGia
                JOIN MuonTra ON DocGia.MaDocGia = MuonTra.MaDocGia
                GROUP BY TenDocGia
                ORDER BY COUNT(MuonTra.MaDocGia) DESC
                LIMIT 1
            """)
            most_active_reader = cursor.fetchone()
            lbl_most_active_reader_val.config(text=most_active_reader[0] if most_active_reader else "Không có dữ liệu")

        except Exception as e:
            messagebox.showerror("Query Error", f"Lỗi khi thực hiện truy vấn:\n{e}")
        finally:
            cursor.close()
            conn.close()

def get_books_details():
    conn = connect_database()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT Sach.TenSach, SUM(Sach.SoLuong) AS TotalBooks, 
                       SUM(CASE WHEN MuonTra.NgayTra IS NULL THEN 1 ELSE 0 END) AS BooksBorrowed
                FROM Sach
                LEFT JOIN MuonTra ON Sach.MaSach = MuonTra.MaSach
                GROUP BY Sach.TenSach
            """)
            books_details = cursor.fetchall()

            # Xóa các mục cũ trong bảng
            for item in tree_books_details.get_children():
                tree_books_details.delete(item)

            for book, total, borrowed in books_details:
                remaining = total - borrowed  # Số sách còn lại
                tree_books_details.insert("", tk.END, values=(book, total, borrowed, remaining))

        except Exception as e:
            messagebox.showerror("Query Error", f"Lỗi khi thực hiện truy vấn:\n{e}")
        finally:
            cursor.close()
            conn.close()

def export_to_excel():
    file_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return

    try:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Thống kê thư viện"

        sheet["A1"] = "Thống kê thư viện"
        sheet["A3"] = "Tổng số lượng sách:"
        sheet["B3"] = lbl_total_books.cget("text")

        sheet["A4"] = "Tổng số độc giả:"
        sheet["B4"] = lbl_total_readers.cget("text")

        sheet["A5"] = "Số sách còn lại trong thư viện:"
        sheet["B5"] = lbl_remaining_books.cget("text")

        sheet["A6"] = "Tỉ lệ trả sách đúng hạn:"
        sheet["B6"] = lbl_return_rate.cget("text")

        sheet["A7"] = "Tên sách được mượn nhiều nhất:"
        sheet["B7"] = lbl_most_borrowed_book_val.cget("text")

        sheet["A8"] = "Độc giả tích cực nhất:"
        sheet["B8"] = lbl_most_active_reader_val.cget("text")

        sheet["A9"] = "Số lượng sách chưa trả:"
        sheet["B9"] = lbl_books_not_returned_count.cget("text").replace("Số lượng: ", "")

        sheet["A10"] = "Số lượng sách đến hẹn chưa trả:"
        sheet["B10"] = lbl_books_due_not_returned_count.cget("text").replace("Số lượng: ", "")

        workbook.save(file_path)
        messagebox.showinfo("Export thành công", f"File Excel đã được lưu tại: {file_path}")
    except Exception as e:
        messagebox.showerror("Export thất bại", f"Có lỗi khi xuất file Excel:\n{e}")

# Setup GUI
root = tk.Tk()
root.title("Thống kê sách")

btn_back = tk.Button(root, text="Trở về", command=root.quit)
btn_back.grid(row=0, column=0, padx=10, pady=10, sticky="w")

lbl_title = tk.Label(root, text="THỐNG KÊ", font=("Arial", 14, "bold"))
lbl_title.grid(row=0, column=0, columnspan=4, pady=(10, 20), sticky="n")

lbl_total_books = tk.Label(root, text="Tổng số lượng sách:", font=("Arial", 10, "bold"))
lbl_total_books.grid(row=1, column=0, sticky="w", padx=10, pady=(10, 10))
lbl_total_books = tk.Label(root, text="", font=("Arial", 10))
lbl_total_books.grid(row=1, column=1, sticky="w", padx=10)

lbl_total_readers = tk.Label(root, text="Tổng số độc giả:", font=("Arial", 10, "bold"))
lbl_total_readers.grid(row=1, column=2, sticky="w", padx=10, pady=(10, 10))
lbl_total_readers = tk.Label(root, text="", font=("Arial", 10))
lbl_total_readers.grid(row=1, column=3, sticky="w", padx=10)

lbl_remaining_books = tk.Label(root, text="Số sách còn lại trong thư viện:", font=("Arial", 10, "bold"))
lbl_remaining_books.grid(row=2, column=0, sticky="w", padx=10)
lbl_remaining_books = tk.Label(root, text="", font=("Arial", 10))
lbl_remaining_books.grid(row=2, column=1, sticky="w", padx=10)

lbl_return_rate = tk.Label(root, text="Tỉ lệ trả sách đúng hạn:", font=("Arial", 10, "bold"))
lbl_return_rate.grid(row=2, column=2, sticky="w", padx=10)
lbl_return_rate = tk.Label(root, text="", font=("Arial", 10))
lbl_return_rate.grid(row=2, column=3, sticky="w", padx=10)

lbl_most_borrowed_book = tk.Label(root, text="Tên sách được mượn nhiều nhất:", font=("Arial", 10, "bold"))
lbl_most_borrowed_book.grid(row=3, column=0, sticky="w", padx=10, pady=(10, 10))
lbl_most_borrowed_book_val = tk.Label(root, text="", font=("Arial", 10))
lbl_most_borrowed_book_val.grid(row=3, column=1, sticky="w", padx=10)

lbl_most_active_reader = tk.Label(root, text="Độc giả tích cực nhất:", font=("Arial", 10, "bold"))
lbl_most_active_reader.grid(row=3, column=2, sticky="w", padx=10, pady=(10, 10))
lbl_most_active_reader_val = tk.Label(root, text="", font=("Arial", 10))
lbl_most_active_reader_val.grid(row=3, column=3, sticky="w", padx=10)

lbl_books_not_returned = tk.Label(root, text="Sách chưa trả:", font=("Arial", 10, "bold"))
lbl_books_not_returned.grid(row=4, column=0, sticky="w", padx=10)

lbl_books_not_returned_count = tk.Label(root, text="Số lượng: 0", font=("Arial", 10))
lbl_books_not_returned_count.grid(row=5, column=0, sticky="w", padx=10)

tree_books_not_returned = Treeview(root, columns=("Sách", "Người mượn", "Ngày mượn", "Ngày trả dự kiến"), show="headings", height=5)
tree_books_not_returned.grid(row=6, column=0, columnspan=4, padx=10, pady=(10, 10))
tree_books_not_returned.heading("Sách", text="Tên sách")
tree_books_not_returned.heading("Người mượn", text="Người mượn")
tree_books_not_returned.heading("Ngày mượn", text="Ngày mượn")
tree_books_not_returned.heading("Ngày trả dự kiến", text="Ngày trả dự kiến")

tree_books_not_returned.column("Ngày mượn", anchor="center")
tree_books_not_returned.column("Ngày trả dự kiến", anchor="center")

lbl_books_due_not_returned = tk.Label(root, text="Sách đến hẹn mà chưa trả:", font=("Arial", 10, "bold"))
lbl_books_due_not_returned.grid(row=7, column=0, sticky="w", padx=10)

lbl_books_due_not_returned_count = tk.Label(root, text="Số lượng: 0", font=("Arial", 10))
lbl_books_due_not_returned_count.grid(row=8, column=0, sticky="w", padx=10)

tree_books_due_not_returned = Treeview(root, columns=("Sách", "Người mượn", "Ngày mượn", "Ngày trả dự kiến"), show="headings", height=5)
tree_books_due_not_returned.grid(row=9, column=0, columnspan=4, padx=10, pady=(10, 10))
tree_books_due_not_returned.heading("Sách", text="Tên sách")
tree_books_due_not_returned.heading("Người mượn", text="Người mượn")
tree_books_due_not_returned.heading("Ngày mượn", text="Ngày mượn")
tree_books_due_not_returned.heading("Ngày trả dự kiến", text="Ngày trả dự kiến")

tree_books_due_not_returned.column("Ngày mượn", anchor="center")
tree_books_due_not_returned.column("Ngày trả dự kiến", anchor="center")

lbl_books_details = tk.Label(root, text="Chi tiết số lượng sách:", font=("Arial", 10, "bold"))
lbl_books_details.grid(row=10, column=0, sticky="w", padx=10)

tree_books_details = Treeview(root, columns=("Sách", "Số lượng", "Đang mượn", "Còn lại"), show="headings", height=5)
tree_books_details.grid(row=11, column=0, columnspan=4, padx=10, pady=(10, 10))
tree_books_details.heading("Sách", text="Tên sách")
tree_books_details.heading("Số lượng", text="Số lượng")
tree_books_details.heading("Đang mượn", text="Đang mượn")
tree_books_details.heading("Còn lại", text="Còn lại")

tree_books_details.column("Sách", anchor="w")
tree_books_details.column("Số lượng", anchor="center")
tree_books_details.column("Đang mượn", anchor="center")
tree_books_details.column("Còn lại", anchor="center")


btn_export_excel = tk.Button(root, text="Export to Excel", command=export_to_excel)
btn_export_excel.grid(row=12, column=0, columnspan=4, pady=(10, 20), sticky="n")

get_statistics()
get_books_details()

root.mainloop()
