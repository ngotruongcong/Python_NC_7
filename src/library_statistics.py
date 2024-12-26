import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.ttk import Treeview
from tkinter.filedialog import asksaveasfilename
import mysql.connector
from datetime import datetime
import openpyxl
from database import get_db_connection

class LibraryStatisticsScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Thống kê sách")
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        # Setup UI components
        self.setup_ui()
        self.get_statistics()
        self.get_books_details()

    def setup_ui(self):
        
        self.frame_statics = ttk.Frame(self.root)
        self.frame_statics.grid(row=0, column=0, sticky="nsew")
    
        # Nút trở về
        btn_back = ttk.Button(self.frame_statics, text="← Trở về", command=self.tro_ve)
        btn_back.grid(row=0, column=0, sticky="W", padx=10, pady=10)



        # Labels for statistics display
        self.lbl_total_books = tk.Label(self.frame_statics, text="", font=("Arial", 10))
        self.lbl_total_readers = tk.Label(self.frame_statics, text="", font=("Arial", 10))
        self.lbl_remaining_books = tk.Label(self.frame_statics, text="", font=("Arial", 10))
        self.lbl_return_rate = tk.Label(self.frame_statics, text="", font=("Arial", 10))
        self.lbl_most_borrowed_book_val = tk.Label(self.frame_statics, text="", font=("Arial", 10))
        self.lbl_most_active_reader_val = tk.Label(self.frame_statics, text="", font=("Arial", 10))
        self.lbl_books_not_returned_count = tk.Label(self.frame_statics, text="Số lượng: 0", font=("Arial", 10))
        self.lbl_books_due_not_returned_count = tk.Label(self.frame_statics, text="Số lượng: 0", font=("Arial", 10))

        # Treeviews for books details
        self.tree_books_due_not_returned = Treeview(self.frame_statics, columns=("Sách", "Người mượn", "Ngày mượn", "Ngày trả dự kiến"), show="headings", height=5)
        self.tree_books_not_returned = Treeview(self.frame_statics, columns=("Sách", "Người mượn", "Ngày mượn", "Ngày trả dự kiến"), show="headings", height=5)
        self.tree_books_details = Treeview(self.frame_statics, columns=("Sách", "Số lượng", "Đang mượn", "Còn lại"), show="headings", height=5)

        
        # Title
        tk.Label(self.frame_statics, text="THỐNG KÊ", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=(10, 20), sticky="n")

        # Statistics Labels
        tk.Label(self.frame_statics, text="Tổng số lượng sách:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=10)
        self.lbl_total_books.grid(row=1, column=1, padx=10)

        tk.Label(self.frame_statics, text="Tổng số độc giả:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky="w", padx=10)
        self.lbl_total_readers.grid(row=1, column=3, padx=10)

        tk.Label(self.frame_statics, text="Số sách còn lại trong thư viện:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=10)
        self.lbl_remaining_books.grid(row=2, column=1, padx=10)

        tk.Label(self.frame_statics, text="Tỉ lệ trả sách đúng hạn:", font=("Arial", 10, "bold")).grid(row=2, column=2, sticky="w", padx=10)
        self.lbl_return_rate.grid(row=2, column=3, padx=10)

        tk.Label(self.frame_statics, text="Tên sách được mượn nhiều nhất:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10)
        self.lbl_most_borrowed_book_val.grid(row=3, column=1, padx=10)

        tk.Label(self.frame_statics, text="Độc giả tích cực nhất:", font=("Arial", 10, "bold")).grid(row=3, column=2, sticky="w", padx=10)
        self.lbl_most_active_reader_val.grid(row=3, column=3, padx=10)

        tk.Label(self.frame_statics, text="Sách chưa trả:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", padx=10)
        self.lbl_books_not_returned_count.grid(row=5, column=0, sticky="w", padx=10)

        # Treeview for books not returned
        self.tree_books_not_returned.grid(row=6, column=0, columnspan=4, padx=10, pady=(10, 10))
        self.tree_books_not_returned.heading("Sách", text="Tên sách")
        self.tree_books_not_returned.heading("Người mượn", text="Người mượn")
        self.tree_books_not_returned.heading("Ngày mượn", text="Ngày mượn")
        self.tree_books_not_returned.heading("Ngày trả dự kiến", text="Ngày trả dự kiến")
        self.tree_books_not_returned.column("Ngày mượn", anchor="center")
        self.tree_books_not_returned.column("Ngày trả dự kiến", anchor="center")

        # Treeview for books due but not returned
        tk.Label(self.frame_statics, text="Sách đến hẹn mà chưa trả:", font=("Arial", 10, "bold")).grid(row=7, column=0, sticky="w", padx=10)
        self.lbl_books_due_not_returned_count.grid(row=8, column=0, sticky="w", padx=10)

        self.tree_books_due_not_returned.grid(row=9, column=0, columnspan=4, padx=10, pady=(10, 10))
        self.tree_books_due_not_returned.heading("Sách", text="Tên sách")
        self.tree_books_due_not_returned.heading("Người mượn", text="Người mượn")
        self.tree_books_due_not_returned.heading("Ngày mượn", text="Ngày mượn")
        self.tree_books_due_not_returned.heading("Ngày trả dự kiến", text="Ngày trả dự kiến")
        self.tree_books_due_not_returned.column("Ngày mượn", anchor="center")
        self.tree_books_due_not_returned.column("Ngày trả dự kiến", anchor="center")

        # Treeview for books details
        tk.Label(self.frame_statics, text="Chi tiết số lượng sách:", font=("Arial", 10, "bold")).grid(row=10, column=0, sticky="w", padx=10)
        self.tree_books_details.grid(row=11, column=0, columnspan=4, padx=10, pady=(10, 10))
        self.tree_books_details.heading("Sách", text="Tên sách")
        self.tree_books_details.heading("Số lượng", text="Số lượng")
        self.tree_books_details.heading("Đang mượn", text="Đang mượn")
        self.tree_books_details.heading("Còn lại", text="Còn lại")
        self.tree_books_details.column("Sách", anchor="w")
        self.tree_books_details.column("Số lượng", anchor="center")
        self.tree_books_details.column("Đang mượn", anchor="center")
        self.tree_books_details.column("Còn lại", anchor="center")

        # Export button
        tk.Button(self.frame_statics, text="Export to Excel", command=self.export_to_excel).grid(row=12, column=0, columnspan=4, pady=(10, 20), sticky="n")

    def create_connection(self):
        # Kết nối đến MySQL server và tạo cơ sở dữ liệu nếu chưa tồn tại
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="dong10082003",
            port="3306"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS library")
        self.cursor.execute("USE library")
        
    def get_statistics(self):
        try:
            # Tổng số lượng sách
            self.cursor.execute("SELECT SUM(so_luong) FROM Sach")
            total_books = self.cursor.fetchone()[0] or 0
            self.lbl_total_books.config(text=total_books)

            # Tổng số độc giả
            self.cursor.execute("SELECT COUNT(*) FROM Doc_gia")
            total_readers = self.cursor.fetchone()[0] or 0
            self.lbl_total_readers.config(text=total_readers)

            # Số sách mượn nhưng chưa trả
            self.cursor.execute("SELECT COUNT(*) FROM Muon_tra WHERE ngay_tra IS NULL")
            books_not_returned_count = self.cursor.fetchone()[0] or 0
            remaining_books = total_books - books_not_returned_count
            self.lbl_remaining_books.config(text=remaining_books)

            # Tỉ lệ trả sách đúng hạn
            self.cursor.execute(""" 
                SELECT COUNT(*) FROM Muon_tra WHERE ngay_tra IS NOT NULL AND ngay_tra <= ngay_tra_du_kien
            """)
            on_time_returns = self.cursor.fetchone()[0] or 0
            self.cursor.execute("SELECT COUNT(*) FROM Muon_tra WHERE ngay_tra IS NOT NULL")
            total_returns = self.cursor.fetchone()[0] or 1  # tránh chia cho 0
            return_rate = (on_time_returns / total_returns) * 100
            self.lbl_return_rate.config(text=f"{return_rate:.2f}%")

            # Sách đến hẹn mà chưa trả
            self.cursor.execute(""" 
                SELECT Sach.ten_sach, Doc_gia.ten_doc_gia, Muon_tra.ngay_muon, Muon_tra.ngay_tra_du_kien 
                FROM Muon_tra
                JOIN Sach ON Muon_tra.ma_sach = Sach.ma_sach
                JOIN Doc_gia ON Muon_tra.ma_doc_gia = Doc_gia.ma_doc_gia
                WHERE Muon_tra.ngay_tra IS NULL AND Muon_tra.ngay_tra_du_kien < %s
            """, (datetime.now().strftime('%Y-%m-%d'),))
            books_due_not_returned = self.cursor.fetchall()
            self.update_treeview(self.tree_books_due_not_returned, books_due_not_returned)
            self.lbl_books_due_not_returned_count.config(text=f"Số lượng: {len(books_due_not_returned)}")

            # Sách chưa trả
            self.cursor.execute(""" 
                SELECT Sach.ten_sach, Doc_gia.ten_doc_gia, Muon_tra.ngay_muon, Muon_tra.ngay_tra_du_kien 
                FROM Muon_tra
                JOIN Sach ON Muon_tra.ma_sach = Sach.ma_sach
                JOIN Doc_gia ON Muon_tra.ma_doc_gia = Doc_gia.ma_doc_gia
                WHERE Muon_tra.ngay_tra IS NULL
            """)
            books_not_returned = self.cursor.fetchall()
            self.update_treeview(self.tree_books_not_returned, books_not_returned)
            self.lbl_books_not_returned_count.config(text=f"Số lượng: {len(books_not_returned)}")

            # Sách được mượn nhiều nhất
            self.cursor.execute(""" 
                SELECT ten_sach 
                FROM Sach
                JOIN Muon_tra ON Sach.ma_sach = Muon_tra.ma_sach
                GROUP BY ten_sach
                ORDER BY COUNT(Muon_tra.ma_sach) DESC
                LIMIT 1
            """)
            most_borrowed_book = self.cursor.fetchone()
            self.lbl_most_borrowed_book_val.config(text=most_borrowed_book[0] if most_borrowed_book else "Không có dữ liệu")

            # Độc giả tích cực nhất
            self.cursor.execute(""" 
                SELECT ten_doc_gia 
                FROM Doc_gia
                JOIN Muon_tra ON Doc_gia.ma_doc_gia = Muon_tra.ma_doc_gia
                GROUP BY ten_doc_gia
                ORDER BY COUNT(Muon_tra.ma_doc_gia) DESC
                LIMIT 1
            """)
            most_active_reader = self.cursor.fetchone()
            self.lbl_most_active_reader_val.config(text=most_active_reader[0] if most_active_reader else "Không có dữ liệu")

        except Exception as e:
            messagebox.showerror("Query Error", f"Lỗi khi thực hiện truy vấn:\n{e}")
        # finally:
        #     self.cursor.close()
        #     self.conn.close()
    def get_books_details(self):
        
        try:
            self.cursor.execute("""
                SELECT Sach.ten_sach, SUM(Sach.so_luong) AS total_books, 
                    SUM(CASE WHEN Muon_tra.ngay_tra IS NULL THEN 1 ELSE 0 END) AS books_borrowed
                FROM Sach
                LEFT JOIN Muon_tra ON Sach.ma_sach = Muon_tra.ma_sach
                GROUP BY Sach.ten_sach
            """)
            books_details = self.cursor.fetchall()

            # Xóa các mục cũ trong bảng
            for item in self.tree_books_details.get_children():
                self.tree_books_details.delete(item)

            for book, total, borrowed in books_details:
                remaining = total - borrowed  # Số sách còn lại
                self.tree_books_details.insert("", tk.END, values=(book, total, borrowed, remaining))

        except Exception as e:
            messagebox.showerror("Query Error", f"Lỗi khi thực hiện truy vấn:\n{e}")
        # finally:
        #     self.cursor.close()
        #     self.conn.close()

    def update_treeview(self, treeview, data):
        for item in treeview.get_children():
            treeview.delete(item)
        for row in data:
            treeview.insert("", tk.END, values=row)

    def export_to_excel(self):
        file_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Thống kê thư viện"

            sheet["A1"] = "Thống kê thư viện"
            sheet["A3"] = "Tổng số lượng sách:"
            sheet["B3"] = self.lbl_total_books.cget("text")
            sheet["A4"] = "Tổng số độc giả:"
            sheet["B4"] = self.lbl_total_readers.cget("text")
            sheet["A5"] = "Số sách còn lại:"
            sheet["B5"] = self.lbl_remaining_books.cget("text")
            sheet["A6"] = "Tỉ lệ trả sách đúng hạn:"
            sheet["B6"] = self.lbl_return_rate.cget("text")
            sheet["A7"] = "Sách được mượn nhiều nhất:"
            sheet["B7"] = self.lbl_most_borrowed_book_val.cget("text")
            sheet["A8"] = "Độc giả tích cực nhất:"
            sheet["B8"] = self.lbl_most_active_reader_val.cget("text")

            sheet["A10"] = "Sách chưa trả:"
            self.write_to_excel(sheet, self.tree_books_not_returned, start_row=11)

            sheet["A20"] = "Sách đến hẹn mà chưa trả:"
            self.write_to_excel(sheet, self.tree_books_due_not_returned, start_row=21)

            workbook.save(file_path)
            messagebox.showinfo("Thành công", "Dữ liệu đã được xuất ra file Excel.")

        except Exception as e:
            messagebox.showerror("Error", f"Không thể xuất dữ liệu ra file Excel: {e}")

    def write_to_excel(self, sheet, treeview, start_row):
        for row_idx, item in enumerate(treeview.get_children(), start=start_row):
            values = treeview.item(item, "values")
            for col_idx, value in enumerate(values, start=1):
                sheet.cell(row=row_idx, column=col_idx, value=value)
    def tro_ve(self):
        self.frame_statics.destroy()

        # Quay lại màn hình chính
        from main import LibraryManagementScreen  # Nhập trong hàm để tránh vòng nhập
        main_screen = LibraryManagementScreen(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryStatisticsScreen(root)
    root.mainloop()
