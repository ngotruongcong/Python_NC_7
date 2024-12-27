# Nhóm Python_NC_7
---

# Ứng dụng Quản lý Thư viện 

Link thuyết trình Canva kết thúc môn [link](https://www.canva.com/design/DAGaacWdVLw/hT9ZIZySd107W8ar1JLNhQ/edit)

---
## 🔎 Danh Mục

1. [Giới Thiệu, Demo sản phẩm](#Giới-Thiệu)
2. [Chức Năng Chính](#chức-năng)
3. [Tổng Quan Hệ Thống](#-tổng-quan-hệ-thống)
4. [Cấu Trúc Thư Mục](#cấu-trúc-thư-mục)
5. [Thiết kế Database](#thiết-kế-database)
6. [Hướng Dẫn Cài Đặt](#hướng-dẫn-cài-đặt)
    - [📋 Yêu Cầu - Prerequisites](#yêu-cầu-)
    - [🔨 Cài Đặt](#-cài-đặt)
7. [🙌 Đóng Góp](#-đóng-góp-cho-dự-án)



---
## Thành  viên

-   Phạm Đăng Đông 2021603320 dong10082003@gmail.com
- Ngô Trường Công 2021602766 congn2213@gmail.com
- Nguyễn Kỳ Phương Bắc 2021602778 Bacnguyenky@gmail.com
- Phan Mạnh Duy 2021600289 phanmanhduy2003333@gmail.com
- Nguyễn Quế Phú 2021602920 phungoanhien1@gmail.com

## Giới Thiệu
Đây là Sản phẩm nhóm cuối kỳ cho môn Python Nâng cao với khả năng quản lý sách cho thư viện

# Demo sản phẩm
[![Demo sản phẩm](https://img.youtube.com/vi/1T4EfuHxj2s/0.jpg)](https://youtu.be/1T4EfuHxj2s)

---
## Chức Năng 
Dự án tập trung vào các chức năng chính sau:
- Quản lý sách
- Quản lý mượn sách
- Quản lý đọc giả
- Thống kê

Link màn hình đặc tả [link](https://drive.google.com/file/d/1tbLHGUx5Sit-1N3xWL6jHIfi7APWzmcl/view?usp=sharing)

---

## 👩‍💻 Tổng Quan Hệ Thống

Mô hình hệ thống bao gồm các công nghệ:  
- [Tkinter](https://docs.python.org/3/library/tkinter.html): Thư viện GUI cho Python, sử dụng để xây dựng giao diện người dùng - cho hệ thống quản lý thư viện.
- [Python](https://www.python.org/doc/): Ngôn ngữ lập trình chính sử dụng cho cả logic ứng dụng và kết nối với MySQL.
- [MySQL](https://www.mysql.com/): Hệ quản trị cơ sở dữ liệu để lưu trữ thông tin về sách, độc giả, và việc mượn sách.
- Docker: Containerize các service, bao gồm ứng dụng Tkinter và cơ sở dữ liệu MySQL, giúp dễ dàng triển khai và quản lý hệ thống.

## Cấu trúc thư mục
```bash
│   .dockerignore
│   .gitignore
│   docker-compose.yml
│   Dockerfile
│   README.md
│   requirements.txt
│   
├───.github
│   │   CODE_OF_CONDUCT.md
│   │   CONTRIBUTING.md
│   │   
│   ├───ISSUE_TEMPLATE
│   │       bug_report.md
│   │       custom.md
│   │       feature_request.md
│   │       
│   ├───PULL_REQUEST_TEMPLATE
│   │       pull_request_template.md
│   │       
│   └───workflows
│           commitlint.yml
│
├───docs
│       database.png
└───src
    │   book_manager.py
    │   borrow_manager.py
    │   config.py
    │   database.py
    │   library_statistics.py
    │   main.py
    │   reader_manager.py
 
```

## Thiết kế Database
![alt text](/docs/database.png)

---

## Hướng Dẫn Cài Đặt

### Yêu Cầu 📋
Trước khi cài đặt, bạn cần cài đặt các công cụ sau:

- [Docker](https://www.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python >= 3.10 
### 🔨 Cài Đặt
---
### chạy local
Bước 1: clone dự án về máy của bạn:
```bash
git clone https://github.com/ngotruongcong/Python_NC_7.git
cd Python_NC_7
```
Bước 2: Tạo môi trường ảo
``` bash
python -m venv venv  # Lệnh này sẽ tạo một thư mục venv trong dự án của bạn, chứa môi trường ảo.
```
Bước 3: Kích hoạt môi trường ảo
- ***Trên window***:
```bash
venv\Scripts\activate
```
- ***Trên macOS/Linux***:
```bash
source venv/bin/activate
```
Bước 4: Cài Đặt Các Thư Viện Phụ Thuộc
```bash
pip install -r requirements.txt
```
Di chuyển vào thư mục chứa code:
```bash 
cd src
```
Bước 5: Cấu Hình MySQL  

Ứng dụng sử dụng MySQL làm cơ sở dữ liệu. Đảm bảo rằng bạn đã cài đặt MySQL và tạo một cơ sở dữ liệu với tên library_management. Cấu hình kết nối trong ứng dụng có thể được tìm thấy trong tệp cấu hình (nếu có) hoặc mã nguồn.

Thông tin cơ bản để kết nối MySQL:
```bash
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dong10082003',  # Thay đổi mật khẩu của bạn nếu cần
    'database': 'library_management',
    'port': '3306'    
}
```

Bước 6: Chạy Ứng Dụng  
Sau khi đã cài đặt xong tất cả phụ thuộc và cấu hình cơ sở dữ liệu, bạn có thể chạy ứng dụng bằng lệnh sau:
```bash
python main.py
```
---
## 🙌 Đóng góp cho dự án

<a href="https://github.com/ngotruongcong/Python_NC_7/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=">Bug Report ⚠️
</a>

<a href="https://github.com/ngotruongcong/Python_NC_7/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=">Feature Request 👩‍💻</a>

Nếu bạn muốn đóng góp cho dự án, hãy đọc [CONTRIBUTING.md](.github/CONTRIBUTING.md) để biết thêm chi tiết.

Mọi đóng góp của các bạn đều được trân trọng, đừng ngần ngại gửi pull request cho dự án.


