# Python_NC_7
bước 1: thay đổi cấu hình database giống trong  file config 
bước 2: chạy file main

``` bash
library-management/
│
├── Frontend/                     # Giao diện ứng dụng (Tkinter)
│   ├── __init__.py
│   ├── main.py                   # Điểm khởi chạy Frontend
│   ├── views/                    # Định nghĩa giao diện người dùng (Tkinter)
│   │   ├── __init__.py
│   │   ├── main_view.py          # Màn hình chính
│   │   └── add_book_view.py      # Màn hình thêm sách
│   ├── controllers/              # Kết nối GUI với Backend
│   │   ├── __init__.py
│   │   └── library_controller.py # Controller để gọi API
│   └── utils.py                  # Các hàm tiện ích (ví dụ: gọi API)
│
├── Backend/                      # API và xử lý logic backend
│   ├── __init__.py
│   ├── main.py                   # Điểm khởi chạy FastAPI
│   ├── api/                      # Định nghĩa API endpoint
│   │   ├── __init__.py
│   │   ├── routes/               # Các route API
│   │   │   ├── __init__.py
│   │   │   └── books.py          # Endpoint quản lý sách
│   │   └── schemas/              # Request/Response schemas (Pydantic)
│   │       ├── __init__.py
│   │       └── book_schema.py
│   ├── application/              # Logic xử lý API
│   │   ├── __init__.py
│   │   ├── use_cases/            # Các Use Case cụ thể
│   │   │   ├── __init__.py
│   │   │   └── book_use_case.py  # Xử lý nghiệp vụ cho sách
│   │   └── interfaces/           # Các interface (abstract class)
│   │       ├── __init__.py
│   │       └── book_repository.py
│   ├── domain/                   # Core logic
│   │   ├── __init__.py
│   │   ├── models/               # Các model của domain
│   │   │   ├── __init__.py
│   │   │   └── book.py
│   │   └── exceptions.py         # Exception của domain
│   ├── infra/                    # Kết nối cơ sở hạ tầng
│   │   ├── __init__.py
│   │   ├── database/             # Kết nối database (MySQL)
│   │   │   ├── __init__.py
│   │   │   └── db_connection.py
│   │   ├── repositories/         # Implement interface repository
│   │   │   ├── __init__.py
│   │   │   └── book_repo.py
│   │   └── migrations/           # Quản lý migration
│   ├── shared/                   # Code dùng chung
│   │   ├── __init__.py
│   │   ├── utils.py
│   │   └── config.py             # Cấu hình (DB connection, environment)
│   └── tests/                    # Kiểm thử
│       ├── __init__.py
│       ├── unit/
│       └── integration/
│
├── .env                          # File môi trường
├── requirements.txt              # Các thư viện cần thiết
└── README.md                     # Tài liệu dự án
```