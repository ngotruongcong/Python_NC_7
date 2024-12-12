import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime
from tkcalendar import DateEntry


# Kết nối CSDL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="qlsach"
    )


# Check date
def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y/%m/%d')
        return True
    except ValueError:
        return False


# Thêm
def add_reader():
    if not (entry_id.get() and entry_name.get() and entry_dob.get() and entry_email.get() and entry_phone.get()):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin")
        return

    if not validate_date(entry_dob.get()):
        messagebox.showwarning("Sai định dạng", "Vui lòng nhập ngày sinh đúng định dạng yyyy/mm/dd")
        return

    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO DocGia (MaDocGia, TenDocGia, NgaySinh, Email, SDT) VALUES (%s, %s, %s, %s, %s)"
    val = (entry_id.get(), entry_name.get(), entry_dob.get(), entry_email.get(), entry_phone.get())
    cursor.execute(sql, val)
    conn.commit()
    conn.close()
    load_data()
    clear_entries()
    messagebox.showinfo("Thành công", "Thêm độc giả thành công")


# Sửa
def update_reader():
    if not (entry_id.get() and entry_name.get() and entry_dob.get() and entry_email.get() and entry_phone.get()):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin")
        return

    if not validate_date(entry_dob.get()):
        messagebox.showwarning("Sai định dạng", "Vui lòng nhập ngày sinh đúng định dạng yyyy/mm/dd")
        return

    dob_formatted = entry_dob.get().replace('/', '-')
    item = tree.selection()[0]
    selected_row = tree.item(item, "values")
    if (entry_id.get() == selected_row[0] and
            entry_name.get() == selected_row[1] and
            dob_formatted == selected_row[2] and
            entry_email.get() == selected_row[3] and
            entry_phone.get() == selected_row[4]):
        clear_entries()
        return

    if messagebox.askyesno("Xác nhận", "Thao tác này sẽ làm thay đổi thông tin. Bạn có chắc không?"):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            sql = "UPDATE DocGia SET TenDocGia=%s, NgaySinh=%s, Email=%s, SDT=%s WHERE MaDocGia=%s"
            dob_str = entry_dob.get_date().strftime('%Y-%m-%d')
            val = (entry_name.get(), dob_str, entry_email.get(), entry_phone.get(), entry_id.get())
            cursor.execute(sql, val)
            conn.commit()
            conn.close()
            load_data()
            clear_entries()
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


# Xóa
def delete_reader():
    if not (entry_id.get() and entry_name.get() and entry_dob.get() and entry_email.get() and entry_phone.get()):
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn độc giả cần xóa")
        return

    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa không?"):
        conn = connect_db()
        cursor = conn.cursor()
        sql = "DELETE FROM DocGia WHERE MaDocGia=%s"
        val = (entry_id.get(),)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        load_data()
        clear_entries()
        messagebox.showinfo("Thành công", "Xóa độc giả thành công")


# Hiển thị dữ liệu vào Treeview
def load_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DocGia")
    rows = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()


def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)


def select_row(event):
    item = tree.selection()[0]
    selected_row = tree.item(item, "values")
    entry_id.delete(0, tk.END)
    entry_id.insert(0, selected_row[0])
    entry_name.delete(0, tk.END)
    entry_name.insert(0, selected_row[1])
    entry_dob.delete(0, tk.END)
    dob_formatted = selected_row[2].replace('-', '/')
    entry_dob.insert(0, dob_formatted)
    entry_email.delete(0, tk.END)
    entry_email.insert(0, selected_row[3])
    entry_phone.delete(0, tk.END)
    entry_phone.insert(0, selected_row[4])


# Tìm kiếm
def search_reader():
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM DocGia WHERE TenDocGia LIKE %s"
    val = ("%" + entry_search.get() + "%",)
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()


# Giao diện
qlDocGia = tk.Tk()
qlDocGia.title("Quản lý độc giả")
qlDocGia.geometry("800x600")

qlDocGia.configure(bg="#babfbb")
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#ffffff",
                foreground="black",
                fieldbackground="#babfbb",
                rowheight=25,
                font=("Arial", 10),
                bordercolor="#d3d3d3",  # Đặt màu viền
                borderwidth=1)  # Đặt độ rộng viền

style.configure("Treeview.Heading",
                background="#555555",
                foreground="white",
                font=("Arial", 10, "bold"),
                bordercolor="#d3d3d3",  # Đặt màu viền
                borderwidth=1)  # Đặt độ rộng viền

style.map("Treeview",
          background=[("selected", "#abe0cd")],
          foreground=[("selected", "black")])

back_button = tk.Button(qlDocGia, text="Trở về", font=("Arial", 10, "bold"), command=lambda: None, bg="#abe0cd",
                        fg="black")
back_button.place(x=20, y=20)

label_width = 100
entry_width = 200
x_label = 250
x_entry = 370

tk.Label(qlDocGia, text="Mã độc giả", font=("Arial", 10, "bold"), bg="#babfbb", fg="black", width=12, anchor='w').place(
    x=x_label, y=80)
entry_id = tk.Entry(qlDocGia, width=30)
entry_id.place(x=x_entry, y=80)

tk.Label(qlDocGia, text="Tên độc giả", font=("Arial", 10, "bold"), bg="#babfbb", fg="black", width=12,
         anchor='w').place(x=x_label, y=120)
entry_name = tk.Entry(qlDocGia, width=30)
entry_name.place(x=x_entry, y=120)

tk.Label(qlDocGia, text="Ngày sinh", font=("Arial", 10, "bold"), bg="#babfbb", fg="black", width=12, anchor='w').place(
    x=x_label, y=160)
entry_dob = DateEntry(qlDocGia, date_pattern='yyyy/mm/dd', showweeknumbers=False, width=28)
entry_dob.place(x=x_entry, y=160)

tk.Label(qlDocGia, text="Email", font=("Arial", 10, "bold"), bg="#babfbb", fg="black", width=12, anchor='w').place(
    x=x_label, y=200)
entry_email = tk.Entry(qlDocGia, width=30)
entry_email.place(x=x_entry, y=200)

tk.Label(qlDocGia, text="Số điện thoại", font=("Arial", 10, "bold"), bg="#babfbb", fg="black", width=12,
         anchor='w').place(x=x_label, y=240)
entry_phone = tk.Entry(qlDocGia, width=30)
entry_phone.place(x=x_entry, y=240)

button_x = 640
button_y = 80
button_width = 10

add_button = tk.Button(qlDocGia, text="Thêm", font=("Arial", 10, "bold"), command=add_reader, bg="#abe0cd", fg="black",
                       width=button_width)
add_button.place(x=button_x, y=button_y)

update_button = tk.Button(qlDocGia, text="Sửa", font=("Arial", 10, "bold"), command=update_reader, bg="#abe0cd",
                          fg="black", width=button_width)
update_button.place(x=button_x, y=button_y + 40)

delete_button = tk.Button(qlDocGia, text="Xóa", font=("Arial", 10, "bold"), command=delete_reader, bg="#abe0cd",
                          fg="black", width=button_width)
delete_button.place(x=button_x, y=button_y + 80)

tk.Label(qlDocGia, text="Tên", font=("Arial", 10, "bold"), bg="#babfbb", fg="black").place(x=20, y=300)
entry_search = tk.Entry(qlDocGia, width=30)
entry_search.place(x=65, y=300)
tk.Button(qlDocGia, text="Tìm kiếm", font=("Arial", 10, "bold"), command=search_reader, bg="#abe0cd", fg="black",
          width=button_width).place(x=270, y=300)

tree = ttk.Treeview(qlDocGia, columns=("MaDocGia", "TenDocGia", "NgaySinh", "Email", "SDT"), show='headings')
tree.heading("MaDocGia", text="ID", anchor='center')
tree.column("MaDocGia", width=30, anchor='center')
tree.heading("TenDocGia", text="Tên độc giả", anchor='center')
tree.column("TenDocGia", width=170, anchor='center')
tree.heading("NgaySinh", text="Ngày sinh", anchor='center')
tree.column("NgaySinh", width=110, anchor='center')
tree.heading("Email", text="Email", anchor='center')
tree.column("Email", width=250, anchor='center')
tree.heading("SDT", text="Số điện thoại", anchor='center')
tree.column("SDT", width=130, anchor='center')
tree.place(x=20, y=350, width=760, height=220)

tree.bind("<ButtonRelease-1>", select_row)

load_data()


def validate_entries(*args):
    if not (entry_id.get() and entry_name.get() and entry_dob.get() and entry_email.get() and entry_phone.get()):
        update_button.config(state=tk.DISABLED)
        delete_button.config(state=tk.DISABLED)
    else:
        update_button.config(state=tk.NORMAL)
        delete_button.config(state=tk.NORMAL)


entry_id.bind("<KeyRelease>", validate_entries)
entry_name.bind("<KeyRelease>", validate_entries)
entry_dob.bind("<KeyRelease>", validate_entries)
entry_email.bind("<KeyRelease>", validate_entries)
entry_phone.bind("<KeyRelease>", validate_entries)

qlDocGia.mainloop()
