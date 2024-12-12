import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Kết nối đến MySQL
library_db = mysql.connector.connect(
    host="127.0.0.1",
    port="3307",
    user="root",
    password="123456Phu.",
    database="LibraryDB"
)
cursor = library_db.cursor()

def add_borrow():
    try:
        ma_doc_gia = entry_ma_doc_gia.get()
        ma_sach = entry_ma_sach.get()
        ngay_muon = entry_ngay_muon.get()
        ngay_tra_du_kien = entry_ngay_tra_du_kien.get()

        if not (ma_doc_gia and ma_sach and ngay_muon and ngay_tra_du_kien):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        # Thêm dữ liệu vào bảng MuonTra
        cursor.execute(
            """
            INSERT INTO MuonTra (MaSach, MaDocGia, NgayMuon, NgayTra, NgayTraDuKien, TrangThai)
            VALUES (%s, %s, %s, NULL, %s, 0)
            """,
            (ma_sach, ma_doc_gia, ngay_muon, ngay_tra_du_kien)
        )
        library_db.commit()

        messagebox.showinfo("Thành công", "Thêm thông tin mượn sách thành công.")
        update_borrow_list()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

def update_borrow_list():
    listbox_borrow.delete(0, tk.END)
    cursor.execute("SELECT MaDocGia, MaSach, NgayMuon, NgayTraDuKien FROM MuonTra")
    for row in cursor.fetchall():
        listbox_borrow.insert(tk.END, f"Mã độc giả: {row[0]}, Mã sách: {row[1]}, Ngày mượn: {row[2]}, Ngày trả dự kiến: {row[3]}")

# Tạo cửa sổ giao diện chính
root = tk.Tk()
root.title("Quản lý mượn")
root.geometry("600x400")

# Nút trở về
btn_back = tk.Button(root, text="Trở về", command=root.quit)
btn_back.grid(row=0, column=0, padx=10, pady=10)

# Tiêu đề
label_title = tk.Label(root, text="Quản lý mượn", font=("Arial", 16))
label_title.grid(row=0, column=1, columnspan=2)

# Các nhãn và entry để nhập dữ liệu
label_ma_doc_gia = tk.Label(root, text="Mã độc giả:")
label_ma_doc_gia.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_ma_doc_gia = tk.Entry(root)
entry_ma_doc_gia.grid(row=1, column=1, padx=10, pady=5)

label_ma_sach = tk.Label(root, text="Mã sách:")
label_ma_sach.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_ma_sach = tk.Entry(root)
entry_ma_sach.grid(row=2, column=1, padx=10, pady=5)

label_ngay_muon = tk.Label(root, text="Ngày mượn:")
label_ngay_muon.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_ngay_muon = tk.Entry(root)
entry_ngay_muon.grid(row=3, column=1, padx=10, pady=5)

label_ngay_tra_du_kien = tk.Label(root, text="Ngày trả dự kiến:")
label_ngay_tra_du_kien.grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_ngay_tra_du_kien = tk.Entry(root)
entry_ngay_tra_du_kien.grid(row=4, column=1, padx=10, pady=5)

# Nút xác nhận mượn (Thêm)
btn_add = tk.Button(root, text="Xác nhận mượn (Thêm)", command=add_borrow)
btn_add.grid(row=5, column=1, pady=10)

# Listbox hiển thị danh sách mượn sách
listbox_borrow = tk.Listbox(root, width=100, height=10)
listbox_borrow.grid(row=1, column=2, rowspan=4, padx=10, pady=5)

# Cập nhật danh sách mượn khi khởi động
update_borrow_list()

# Chạy giao diện
root.mainloop()

# Đóng kết nối cơ sở dữ liệu
cursor.close()
library_db.close()
