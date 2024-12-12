import mysql.connector

# Kết nối đến MySQL
library_db = mysql.connector.connect(
    host="127.0.0.1",
    port="3307",
    user="root",
    password="123456Phu."
)

cursor = library_db.cursor()

# Tên cơ sở dữ liệu
library_database_name = "LibraryDB"

# Tạo cơ sở dữ liệu và sử dụng nó
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {library_database_name}")
cursor.execute(f"USE {library_database_name}")

# Tạo bảng Sach
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sach (
        MaSach INT PRIMARY KEY,
        TenSach NVARCHAR(255) NOT NULL,
        TacGia NVARCHAR(255),
        TheLoai NVARCHAR(255),
        NgayXuatBan DATE,
        SoLuong INT
    )
""")

# Tạo bảng DocGia
cursor.execute("""
    CREATE TABLE IF NOT EXISTS DocGia (
        MaDocGia INT PRIMARY KEY,
        TenDocGia NVARCHAR(255) NOT NULL,
        NgaySinh DATE,
        Email NVARCHAR(255),
        SDT NVARCHAR(15)
    )
""")

# Tạo bảng MuonTra
cursor.execute("""
    CREATE TABLE IF NOT EXISTS MuonTra (
         MaMuonTra INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        MaSach INT NOT NULL,
        MaDocGia INT NOT NULL,
        NgayMuon DATE,
        NgayTra DATE,
        NgayTraDuKien DATE,
        TrangThai BIT,
        CONSTRAINT FK_MuonTra_Sach FOREIGN KEY (MaSach) REFERENCES Sach(MaSach),
        CONSTRAINT FK_MuonTra_DocGia FOREIGN KEY (MaDocGia) REFERENCES DocGia(MaDocGia)
    )
""")

# # Dữ liệu mẫu cho bảng Sach
# books_data = [
#     (1, "Lập Trình Python", "Nguyễn Văn A", "Công Nghệ Thông Tin", "2020-05-01", 10),
#     (2, "Học SQL Cơ Bản", "Trần Văn B", "Công Nghệ Thông Tin", "2019-08-15", 5),
#     (3, "Văn Học Việt Nam", "Phạm Minh C", "Văn Học", "2021-03-20", 7),
#     (4, "Toán Học Cao Cấp", "Hoàng Thị D", "Khoa Học", "2020-11-05", 3),
#     (5, "Lịch Sử Thế Giới", "Lê Văn E", "Lịch Sử", "2018-09-10", 8)
# ]
# cursor.executemany("INSERT INTO Sach (MaSach, TenSach, TacGia, TheLoai, NgayXuatBan, SoLuong) VALUES (%s, %s, %s, %s, %s, %s)", books_data)
#
# # Dữ liệu mẫu cho bảng DocGia
# readers_data = [
#     (1, "Nguyễn Thị A", "2000-01-01", "a.nguyen@example.com", "0987654321"),
#     (2, "Trần Văn B", "1998-05-12", "b.tran@example.com", "0978654321"),
#     (3, "Phạm Thị C", "2002-03-20", "c.pham@example.com", "0967654321"),
#     (4, "Lê Văn D", "1999-07-07", "d.le@example.com", "0957654321"),
#     (5, "Hoàng Minh E", "2001-11-15", "e.hoang@example.com", "0947654321")
# ]
# cursor.executemany("INSERT INTO DocGia (MaDocGia, TenDocGia, NgaySinh, Email, SDT) VALUES (%s, %s, %s, %s, %s)", readers_data)
#
# # Dữ liệu mẫu cho bảng MuonTra
borrow_data = [

    (2, 2, 2, "2023-11-25", "2023-12-05", "2023-11-30", 1),
    (3, 3, 3, "2023-12-03", None, "2023-12-08", 0),
    (4, 4, 4, "2023-11-28", "2023-12-03", "2023-12-02", 1),
    (5, 5, 5, "2023-12-02", None, "2023-12-07", 0)
]
cursor.executemany("INSERT INTO MuonTra (MaMuonTra, MaSach, MaDocGia, NgayMuon, NgayTra, NgayTraDuKien, TrangThai) VALUES (%s, %s, %s, %s, %s, %s, %s)", borrow_data)

# Lưu thay đổi vào cơ sở dữ liệu
library_db.commit()

# Đóng kết nối
cursor.close()
library_db.close()

print("Database Quản lý sách và dữ liệu mẫu đã được tạo thành công.")

