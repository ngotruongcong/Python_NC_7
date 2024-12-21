import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter.filedialog import asksaveasfilename
import mysql.connector
from datetime import datetime
import openpyxl


class LibraryStatistics:
    def __init__(self, root):
        self.root = root
        self.root.title("Thống kê sách")

        # Labels for statistics display
        self.lbl_total_books = tk.Label(root, text="", font=("Arial", 10))
        self.lbl_total_readers = tk.Label(root, text="", font=("Arial", 10))
        self.lbl_remaining_books = tk.Label(root, text="", font=("Arial", 10))
        self.lbl_return_rate = tk.Label(root, text="", font=("Arial", 10))
        self.lbl_most_borrowed_book_val = tk.Label(root, text="", font=("Arial", 10))
        self.lbl_most_active_reader_val = tk.Label(root, text="", font=("Arial", 10))
        self.lbl_books_not_returned_count = tk.Label(root, text="Số lượng: 0", font=("Arial", 10))
        self.lbl_books_due_not_returned_count = tk.Label(root, text="Số lượng: 0", font=("Arial", 10))

        # Treeviews for books details
        self.tree_books_due_not_returned = Treeview(root, columns=("Sách", "Người mượn", "Ngày mượn", "Ngày trả dự kiến"), show="headings", height=5)
        self.tree_books_not_returned = Treeview(root, columns=("Sách", "Người mượn", "Ngày mượn", "Ngày trả dự kiến"), show="headings", height=5)
        self.tree_books_details = Treeview(root, columns=("Sách", "Số lượng", "Đang mượn", "Còn lại"), show="headings", height=5)

        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        # Button Back
        tk.Button(self.root, text="Trở về", command=self.root.quit).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Title
        tk.Label(self.root, text="THỐNG KÊ", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=(10, 20), sticky="n")

        # Statistics Labels
        tk.Label(self.root, text="Tổng số lượng sách:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=10)
        self.lbl_total_books.grid(row=1, column=1, padx=10)

        tk.Label(self.root, text="Tổng số độc giả:", font=("Arial", 10, "bold")).grid(row=1, column=2, sticky="w", padx=10)
        self.lbl_total_readers.grid(row=1, column=3, padx=10)

        tk.Label(self.root, text="Số sách còn lại trong thư viện:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=10)
        self.lbl_remaining_books.grid(row=2, column=1, padx=10)

        tk.Label(self.root, text="Tỉ lệ trả sách đúng hạn:", font=("Arial", 10, "bold")).grid(row=2, column=2, sticky="w", padx=10)
        self.lbl_return_rate.grid(row=2, column=3, padx=10)

        tk.Label(self.root, text="Tên sách được mượn nhiều nhất:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10)
        self.lbl_most_borrowed_book_val.grid(row=3, column=1, padx=10)

        tk.Label(self.root, text="Độc giả tích cực nhất:", font=("Arial", 10, "bold")).grid(row=3, column=2, sticky="w", padx=10)
        self.lbl_most_active_reader_val.grid(row=3, column=3, padx=10)

        tk.Label(self.root, text="Sách chưa trả:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", padx=10)
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
        tk.Label(self.root, text="Sách đến hẹn mà chưa trả:", font=("Arial", 10, "bold")).grid(row=7, column=0, sticky="w", padx=10)
        self.lbl_books_due_not_returned_count.grid(row=8, column=0, sticky="w", padx=10)

        self.tree_books_due_not_returned.grid(row=9, column=0, columnspan=4, padx=10, pady=(10, 10))
        self.tree_books_due_not_returned.heading("Sách", text="Tên sách")
        self.tree_books_due_not_returned.heading("Người mượn", text="Người mượn")
        self.tree_books_due_not_returned.heading("Ngày mượn", text="Ngày mượn")
        self.tree_books_due_not_returned.heading("Ngày trả dự kiến", text="Ngày trả dự kiến")
        self.tree_books_due_not_returned.column("Ngày mượn", anchor="center")
        self.tree_books_due_not_returned.column("Ngày trả dự kiến", anchor="center")

        # Treeview for books details
        tk.Label(self.root, text="Chi tiết số lượng sách:", font=("Arial", 10, "bold")).grid(row=10, column=0, sticky="w", padx=10)
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
        tk.Button(self.root, text="Export to Excel", command=lambda: print("Export to Excel")).grid(row=12, column=0, columnspan=4, pady=(10, 20), sticky="n")

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
        conn = self.create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Tổng số lượng sách
                cursor.execute("SELECT SUM(SoLuong) FROM Sach")
                total_books = cursor.fetchone()[0] or 0
                self.lbl_total_books.config(text=total_books)

                # Tổng số độc giả
                cursor.execute("SELECT COUNT(*) FROM DocGia")
                total_readers = cursor.fetchone()[0] or 0
                self.lbl_total_readers.config(text=total_readers)

                # Số sách mượn nhưng chưa trả
                cursor.execute("SELECT COUNT(*) FROM MuonTra WHERE NgayTra IS NULL")
                books_not_returned_count = cursor.fetchone()[0] or 0
                remaining_books = total_books - books_not_returned_count
                self.lbl_remaining_books.config(text=remaining_books)

                # Tỉ lệ trả sách đúng hạn
                cursor.execute(""" 
                    SELECT COUNT(*) FROM MuonTra WHERE NgayTra IS NOT NULL AND NgayTra <= NgayTraDuKien
                """)
                on_time_returns = cursor.fetchone()[0] or 0
                cursor.execute("SELECT COUNT(*) FROM MuonTra WHERE NgayTra IS NOT NULL")
                total_returns = cursor.fetchone()[0] or 1  # tránh chia cho 0
                return_rate = (on_time_returns / total_returns) * 100
                self.lbl_return_rate.config(text=f"{return_rate:.2f}%")

                # Sách đến hẹn mà chưa trả
                cursor.execute(""" 
                    SELECT Sach.TenSach, DocGia.TenDocGia, MuonTra.NgayMuon, MuonTra.NgayTraDuKien 
                    FROM MuonTra
                    JOIN Sach ON MuonTra.MaSach = Sach.MaSach
                    JOIN DocGia ON MuonTra.MaDocGia = DocGia.MaDocGia
                    WHERE MuonTra.NgayTra IS NULL AND MuonTra.NgayTraDuKien < %s
                """, (datetime.now().strftime('%Y-%m-%d'),))
                books_due_not_returned = cursor.fetchall()
                self.update_treeview(self.tree_books_due_not_returned, books_due_not_returned)
                self.lbl_books_due_not_returned_count.config(text=f"Số lượng: {len(books_due_not_returned)}")

                # Sách chưa trả
                cursor.execute(""" 
                    SELECT Sach.TenSach, DocGia.TenDocGia, MuonTra.NgayMuon, MuonTra.NgayTraDuKien 
                    FROM MuonTra
                    JOIN Sach ON MuonTra.MaSach = Sach.MaSach
                    JOIN DocGia ON MuonTra.MaDocGia = DocGia.MaDocGia
                    WHERE MuonTra.NgayTra IS NULL
                """)
                books_not_returned = cursor.fetchall()
                self.update_treeview(self.tree_books_not_returned, books_not_returned)
                self.lbl_books_not_returned_count.config(text=f"Số lượng: {len(books_not_returned)}")

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
                self.lbl_most_borrowed_book_val.config(text=most_borrowed_book[0] if most_borrowed_book else "Không có dữ liệu")

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
                self.lbl_most_active_reader_val.config(text=most_active_reader[0] if most_active_reader else "Không có dữ liệu")

            except Exception as e:
                messagebox.showerror("Query Error", f"Lỗi khi thực hiện truy vấn:\n{e}")
            finally:
                cursor.close()
                conn.close()

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


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryStatistics(root)
    app.get_statistics()
    root.mainloop()
