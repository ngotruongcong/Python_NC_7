import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkcalendar import DateEntry
from tkinter.font import Font
class BorrowManagerScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Mượn")
        self.root.configure(bg="#babfbb")
        self.create_connection()
        self.create_gui()
        self.load_muon_tra()
        
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
        
        # Tạo bảng nếu chưa tồn tại
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Muon_tra (
                ma_muon_tra INT PRIMARY KEY,
                ma_sach INT,
                ma_doc_gia INT,
                ngay_muon DATE,
                ngay_tra DATE,
                ngay_tra_du_kien DATE,
                trang_thai BIT DEFAULT 0,
                FOREIGN KEY (ma_sach) REFERENCES Sach(ma_sach),
                FOREIGN KEY (ma_doc_gia) REFERENCES Doc_gia(ma_doc_gia)
            );
        """)
    def create_gui(self):
            # Giao diện nhập liệu
            self.style = ttk.Style()
            self.style.theme_use('clam')
            self.create_fonts()
            
            self.frame_borrow_manager = ttk.Frame(self.root)
            self.frame_borrow_manager.grid(row=0, column=0, sticky="nsew")
              # Nút trở về
            btn_back = ttk.Button(self.frame_borrow_manager, text="← Trở về", command=self.tro_ve)
            btn_back.grid(row=0, column=0, sticky="W", padx=10, pady=10)
            
            self.frame_inputs = ttk.Frame(self.frame_borrow_manager, padding=(10, 10))
            self.frame_inputs.grid(row=1, column=0, sticky="W")
            
            self.create_input_fields()
            self.create_buttons()
            self.create_treeview()
    def create_fonts(self):
        # Font tùy chỉnh
        self.header_font = Font(family="Arial", size=14, weight="bold")
        self.label_font = Font(family="Arial", size=10)
        self.button_font = Font(family="Arial", size=10)
        self.label_bg_color = "#f7f7f7"
    def create_input_fields(self):
        # Tạo các input field với label
        labels = ["Mã mượn trả","Mã Sách", "Mã đọc giả", "Ngày mượn","Ngày trả","Ngày trả dự kiến", "Trạng thái", "Tìm Kiếm"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.frame_inputs, text=label, background=self.label_bg_color, font=self.label_font).grid(row=i, column=0, padx=10, pady=5)
            if label in ["Ngày mượn", "Ngày trả", "Ngày trả dự kiến"]:
                entry = DateEntry(self.frame_inputs, width=18, background="darkblue", foreground="white", date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(self.frame_inputs)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry
    def create_buttons(self):
        # Tạo các nút điều khiển
        frame_buttons = ttk.Frame(self.frame_inputs, padding=(10, 10))
        frame_buttons.grid(row=11, columnspan=2, pady=(10, 0))

        btn_names = [("Thêm", self.them_muon_tra), ("Sửa", self.sua_muon_tra), ("Xóa", self.xoa_muon_tra), ("Tìm Kiếm", self.tim_kiem)]
        for idx, (text, command) in enumerate(btn_names):
            btn = ttk.Button(frame_buttons, text=text, command=command, style="TButton")
            btn.grid(row=0, column=idx, padx=5, pady=5, ipadx=10)
    def create_treeview(self):
        # Tạo Treeview để hiển thị danh sách sách
        columns = ("Mã mượn trả","Mã Sách", "Mã đọc giả", "Ngày mượn","Ngày trả","Ngày trả dự kiến", "Trạng thái")
        self.tree = ttk.Treeview(self.frame_borrow_manager, columns=columns, show="headings", height=15)
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Định nghĩa tiêu đề cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Liên kết sự kiện chọn dòng
        self.tree.bind('<<TreeviewSelect>>', self.chon_item)
    def load_muon_tra(self):
        # Hàm tải danh sách sách lên Treeview
        self.cursor.execute("SELECT * FROM Muon_tra")
        rows = self.cursor.fetchall()
        self.update_treeview(rows)

    def update_treeview(self, rows):
        # Cập nhật Treeview
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', "end", values=row)
            
    def chon_item(self, event):
        selected_item = self.tree.focus()
        values = self.tree.item(selected_item, 'values')
        if values:
            for i, key in enumerate(self.entries.keys()):
                if key == "Tìm Kiếm":  # Bỏ qua ô Tìm Kiếm
                    continue
                self.entries[key].delete(0, "end")
                if key in ["Ngày mượn", "Ngày trả", "Ngày trả dự kiến"]:
                    self.entries[key].set_date(values[i])
                else:
                    self.entries[key].insert(0, values[i])

    def them_muon_tra(self):
        try:
            # Lấy dữ liệu từ giao diện
            ma_muon_tra = int(self.entries["Mã mượn trả"].get())  # Mã sách
            ma_sach = int(self.entries["Mã Sách"].get())  # Mã sách
            ma_doc_gia = int(self.entries["Mã đọc giả"].get())  # Mã độc giả
            ngay_muon = self.entries["Ngày mượn"].get_date()  # Ngày mượn
            ngay_tra = self.entries["Ngày trả"].get_date()  # Ngày mượn
            ngay_tra_du_kien = self.entries["Ngày trả dự kiến"].get_date()  # Ngày trả dự kiến
            trang_thai = 0  # Trạng thái mặc định là 0 (chưa trả)

            # Kiểm tra dữ liệu bắt buộc
            if not ma_sach or not ma_doc_gia or not ngay_muon or not ngay_tra_du_kien:
                raise ValueError("Vui lòng nhập đầy đủ thông tin mượn sách.")
            
            # Thêm thông tin mượn/trả vào bảng Muon_tra
            self.cursor.execute("""
                INSERT INTO Muon_tra (ma_muon_tra, ma_sach, ma_doc_gia, ngay_muon, ngay_tra, ngay_tra_du_kien, trang_thai)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (ma_muon_tra, ma_sach, ma_doc_gia, ngay_muon, ngay_tra, ngay_tra_du_kien, trang_thai))
            
            # Commit thay đổi vào cơ sở dữ liệu
            self.conn.commit()
            
            # Refresh dữ liệu trên giao diện (giả sử bạn có hàm load_muon_tra)
            self.load_muon_tra()
            
            # Thông báo thành công
            messagebox.showinfo("Thành công", "Thêm thông tin mượn sách thành công.")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Lỗi")
        

    def sua_muon_tra(self):
        ma_muon_tra = int(self.entries["Mã Mượn Trả"].get())  # Mã mượn trả
        ma_sach = int(self.entries["Mã Sách"].get())  # Mã sách
        ma_doc_gia = int(self.entries["Mã Độc Giả"].get())  # Mã độc giả
        ngay_muon = self.entries["Ngày Mượn"].get_date()  # Ngày mượn
        ngay_tra = self.entries["Ngày Trả"].get_date() if self.entries["Ngày Trả"].get() else None  # Ngày trả
        ngay_tra_du_kien = self.entries["Ngày Trả Dự Kiến"].get_date()  # Ngày trả dự kiến
        trang_thai = int(self.entries["Trạng Thái"].get())  # Trạng thái: 0 - chưa trả, 1 - đã trả

        # Kiểm tra dữ liệu bắt buộc
        if not ma_sach or not ma_doc_gia or not ngay_muon or not ngay_tra_du_kien:
            raise ValueError("Vui lòng nhập đầy đủ thông tin cần sửa.")


        self.cursor.execute("UPDATE Muon_tra  SET  ma_sach = %s, ma_doc_gia = %s, ngay_muon = %s, ngay_tra = %s , ngay_tra_du_kien=%s, trang_thai=%s WHERE ma_muon_tra = %s",
                           (ma_sach, ma_doc_gia, ngay_muon, ngay_tra,ngay_tra_du_kien, trang_thai,  ma_muon_tra))
        self.conn.commit()
        self.load_muon_tra()
        messagebox.showinfo("Thành công", "Cập nhật thông tin mượn/trả thành công.")
        
    def xoa_muon_tra(self):
        ma_muon_tra = int(self.entries["Mã mượn trả"].get())
        self.cursor.execute("DELETE FROM Muon_tra WHERE ma_muon_tra = %s", (ma_muon_tra,))
        self.conn.commit()
        self.load_muon_tra()
        messagebox.showinfo("Thành công", "Xóa đơn mượn trả thành công.")
        
    def tim_kiem(self):
        keyword = self.entries["Tìm Kiếm"].get()
        # Truy vấn tìm kiếm với JOIN giữa Muon_tra và Doc_gia
        query = """
            SELECT 
                Muon_tra.ma_muon_tra,
                Sach.ten_sach,
                Doc_gia.ten_doc_gia,
                Muon_tra.ngay_muon,
                Muon_tra.ngay_tra,
                Muon_tra.ngay_tra_du_kien,
                Muon_tra.trang_thai
            FROM Muon_tra
            INNER JOIN Doc_gia ON Muon_tra.ma_doc_gia = Doc_gia.ma_doc_gia
            INNER JOIN Sach ON Muon_tra.ma_sach = Sach.ma_sach
            WHERE Doc_gia.ten_doc_gia LIKE %s OR Muon_tra.ngay_muon LIKE %s
        """
        self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        rows = self.cursor.fetchall()
        self.update_treeview(rows)

    def tro_ve(self):
        # Xóa các widget hiện tại của màn hình quản lý sách
        for widget in self.frame_borrow_manager.winfo_children():
            widget.grid_forget()

        # Quay lại màn hình chính
        from main import LibraryManagementScreen  # Nhập trong hàm để tránh vòng nhập
        main_screen = LibraryManagementScreen(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = BorrowManagerScreen(root)
    root.mainloop()
