import mysql.connector
from tkinter import END
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter.font import Font

# Kết nối đến MySQL server và tạo cơ sở dữ liệu nếu chưa tồn tại
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    port="3305"
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS library")
cursor.execute("USE library")

# Sao lưu dữ liệu từ bảng cũ
cursor.execute("SHOW TABLES LIKE 'Sach'")
if cursor.fetchone():
    cursor.execute("SELECT * FROM Sach")
    data_backup = cursor.fetchall()
else:
    data_backup = []

# Xóa bảng cũ
cursor.execute("DROP TABLE IF EXISTS Sach")

# Tạo bảng mới với cột NgayXuatBan là DATE
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS Sach (
    MaSach INT PRIMARY KEY,
    TenSach VARCHAR(255) NOT NULL,
    TacGia VARCHAR(255),
    TheLoai VARCHAR(255),
    NgayXuatBan DATE,
    SoLuong INT
)
''')

# Phục hồi dữ liệu vào bảng mới
for row in data_backup:
    cursor.execute("INSERT INTO Sach (MaSach, TenSach, TacGia, TheLoai, NgayXuatBan, SoLuong) VALUES (%s, %s, %s, %s, %s, %s)", row)
conn.commit()

# Hàm thêm sách
def them_sach():
    try:
        ma_sach = int(entry_ma_sach.get())
        ten_sach = entry_ten_sach.get()
        tac_gia = entry_tac_gia.get()
        the_loai = entry_the_loai.get()
        ngay_xuat_ban = entry_ngay_xuat_ban.get_date()
        so_luong = int(entry_so_luong.get())

        if not ten_sach:
            raise ValueError("Tên sách không được để trống.")

        cursor.execute("INSERT INTO Sach (MaSach, TenSach, TacGia, TheLoai, NgayXuatBan, SoLuong) VALUES (%s, %s, %s, %s, %s, %s)",
                       (ma_sach, ten_sach, tac_gia, the_loai, ngay_xuat_ban, so_luong))
        conn.commit()
        load_sach()
        messagebox.showinfo("Thành công", "Thêm sách thành công.")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Lỗi", "Mã sách đã tồn tại.")

# Hàm sửa sách
def sua_sach():
    ma_sach = int(entry_ma_sach.get())
    ten_sach = entry_ten_sach.get()
    tac_gia = entry_tac_gia.get()
    the_loai = entry_the_loai.get()
    ngay_xuat_ban = entry_ngay_xuat_ban.get_date()
    so_luong = int(entry_so_luong.get())

    if not ten_sach:
        raise ValueError("Tên sách không được để trống.")

    cursor.execute("UPDATE Sach SET TenSach = %s, TacGia = %s, TheLoai = %s, NgayXuatBan = %s, SoLuong = %s WHERE MaSach = %s",
                   (ten_sach, tac_gia, the_loai, ngay_xuat_ban, so_luong, ma_sach))
    conn.commit()
    load_sach()
    messagebox.showinfo("Thành công", "Sửa sách thành công.")

# Hàm xóa sách
def xoa_sach():
    ma_sach = int(entry_ma_sach.get())
    cursor.execute("DELETE FROM Sach WHERE MaSach = %s", (ma_sach,))
    conn.commit()
    load_sach()
    messagebox.showinfo("Thành công", "Xóa sách thành công.")

# Hàm xử lý khi chọn item trong Treeview
def chon_item(event):
    selected_item = tree.focus()
    values = tree.item(selected_item, 'values')
    if values:
        entry_ma_sach.delete(0, END)
        entry_ma_sach.insert(0, values[0])
        entry_ten_sach.delete(0, END)
        entry_ten_sach.insert(0, values[1])
        entry_tac_gia.delete(0, END)
        entry_tac_gia.insert(0, values[2])
        entry_the_loai.delete(0, END)
        entry_the_loai.insert(0, values[3])
        entry_ngay_xuat_ban.set_date(values[4])
        entry_so_luong.delete(0, END)
        entry_so_luong.insert(0, values[5])

# Hàm tìm kiếm sách
def tim_kiem():
    keyword = entry_tim_kiem.get()
    cursor.execute("SELECT * FROM Sach WHERE TenSach LIKE %s OR TheLoai LIKE %s",
                   (f"%{keyword}%", f"%{keyword}%"))
    rows = cursor.fetchall()
    update_treeview(rows)

# Hàm tải danh sách sách lên Treeview
def load_sach():
    cursor.execute("SELECT * FROM Sach")
    rows = cursor.fetchall()
    update_treeview(rows)

# Cập nhật Treeview
def update_treeview(rows):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', END, values=row)

# Hàm trở về
def tro_ve():
    messagebox.showinfo("Thông báo", "Bạn đã nhấn nút trở về")

# GUI
root = tk.Tk()
root.title("Quản lý sách")
root.configure(bg="#babfbb")

style = ttk.Style()
style.theme_use('clam')

# Cải tiến giao diện Treeview
style.configure("Treeview",
                background="#e6f7ff",
                foreground="black",
                rowheight=25,
                fieldbackground="#e6f7ff")
style.map("Treeview", background=[('selected', '#b3d9ff')])

# Font tùy chỉnh
header_font = Font(family="Arial", size=14, weight="bold")
button_font = Font(family="Arial", size=10)

# Nút trở về
btn_back = ttk.Button(root, text="← Trở về", command=tro_ve)
btn_back.grid(row=0, column=0, sticky="W", padx=10, pady=10)

# Giao diện nhập liệu
frame_inputs = ttk.Frame(root, padding=(10, 10))
frame_inputs.grid(row=1, column=0, sticky="W")

frame_inputs.configure(style=".TFrame")

# Labels và Entries
label_font = Font(family="Arial", size=10)
label_bg_color = "#f7f7f7"  # Màu nền sáng

# Cập nhật các label với font và màu sắc cải tiến
ttk.Label(frame_inputs, text="Mã Sách", background=label_bg_color, font=label_font).grid(row=0, column=0, padx=10, pady=5)
entry_ma_sach = ttk.Entry(frame_inputs)
entry_ma_sach.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame_inputs, text="Tên sách", background=label_bg_color, font=label_font).grid(row=1, column=0, padx=10, pady=5)
entry_ten_sach = ttk.Entry(frame_inputs)
entry_ten_sach.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(frame_inputs, text="Tác giả", background=label_bg_color, font=label_font).grid(row=2, column=0, padx=10, pady=5)
entry_tac_gia = ttk.Entry(frame_inputs)
entry_tac_gia.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(frame_inputs, text="Thể loại", background=label_bg_color, font=label_font).grid(row=3, column=0, padx=10, pady=5)
entry_the_loai = ttk.Entry(frame_inputs)
entry_the_loai.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(frame_inputs, text="Ngày xuất bản", background=label_bg_color, font=label_font).grid(row=4, column=0, padx=10, pady=5)
entry_ngay_xuat_ban = DateEntry(frame_inputs, width=18, background="darkblue", foreground="white", date_pattern='yyyy-mm-dd')
entry_ngay_xuat_ban.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(frame_inputs, text="Số lượng", background=label_bg_color, font=label_font).grid(row=5, column=0, padx=10, pady=5)
entry_so_luong = ttk.Entry(frame_inputs)
entry_so_luong.grid(row=5, column=1, padx=10, pady=5)

ttk.Label(frame_inputs, text="Tìm Kiếm", background=label_bg_color, font=label_font).grid(row=6, column=0, padx=10, pady=5)
entry_tim_kiem = ttk.Entry(frame_inputs)
entry_tim_kiem.grid(row=6, column=1, padx=10, pady=5)

# Các nút
frame_buttons = ttk.Frame(frame_inputs, padding=(10, 10))
frame_buttons.grid(row=7, columnspan=2, pady=(10, 0))

btn_them = ttk.Button(frame_buttons, text="Thêm", command=them_sach, style="TButton")
btn_them.grid(row=0, column=0, padx=5, pady=5, ipadx=10)

btn_sua = ttk.Button(frame_buttons, text="Sửa", command=sua_sach, style="TButton")
btn_sua.grid(row=0, column=1, padx=5, pady=5, ipadx=10)

btn_xoa = ttk.Button(frame_buttons, text="Xóa", command=xoa_sach, style="TButton")
btn_xoa.grid(row=0, column=2, padx=5, pady=5, ipadx=10)

btn_tim_kiem = ttk.Button(frame_buttons, text="Tìm Kiếm", command=tim_kiem, style="TButton")
btn_tim_kiem.grid(row=0, column=3, padx=5, pady=5, ipadx=10)

# Treeview
columns = ("Mã Sách", "Tên Sách", "Tác Giả", "Thể Loại", "Ngày Xuất Bản", "Số Lượng")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Định nghĩa tiêu đề cột
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

# Liên kết sự kiện chọn dòng
tree.bind('<<TreeviewSelect>>', chon_item)

load_sach()
root.mainloop()
conn.close()
