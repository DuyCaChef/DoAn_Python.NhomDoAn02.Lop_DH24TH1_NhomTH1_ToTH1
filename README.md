# DoAn_Python.NhomDoAn02.Lop_DH24TH1_NhomTH1_ToTH1

<!-- Python & tech badges -->
[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)](https://docs.python.org/3/library/tkinter.html)
[![MySQL](https://img.shields.io/badge/Database-MySQL-00758F?logo=mysql&logoColor=white)](https://www.mysql.com/)

# 🧑‍💼 ỨNG DỤNG QUẢN LÝ NHÂN SỰ BẰNG PYTHON, TKINTER VÀ MYSQL

## 🏫 Trường Đại học An Giang

**Khoa Công Nghệ Thông Tin**  
**Môn học:** Chuyên đề Python (COS525)  
**Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Minh

---

## 👨‍💻 Thông tin nhóm thực hiện

| Họ và tên       | MSSV      | Lớp     |
| --------------- | --------- | ------- |
| Phan Khánh Duy  | DTH235632 | DH24TH1 |
| Nguyễn Tuấn Hải | DTH235638 | DH24TH1 |

---

## 📬 Thông tin liên hệ (Contact)

- Phan Khánh Duy (DuyCaChef)
  - Vai trò: Thành viên nhóm
  - GitHub: https://github.com/DuyCaChef
  - Badge: ![Duy GitHub](https://img.shields.io/badge/GitHub-DuyCaChef-181717?logo=github&logoColor=white)

- Nguyễn Tuấn Hải (TuanHaii)
  - Vai trò: Thành viên nhóm
  - GitHub: https://github.com/TuanHaii
  - Badge: ![Tuan GitHub](https://img.shields.io/badge/GitHub-TuanHaii-181717?logo=github&logoColor=white)

## 🎯 Mục tiêu đồ án

Xây dựng một **ứng dụng quản lý nhân sự** có giao diện thân thiện bằng **Tkinter**, kết nối với **MySQL** để lưu trữ dữ liệu lâu dài.  
Ứng dụng cho phép người dùng:

- Thêm, sửa, xóa và lưu thông tin nhân viên (CRUD)
- Hiển thị danh sách nhân viên
- Tìm kiếm, chọn, và cập nhật thông tin nhân viên
- Giao diện trực quan, dễ thao tác, dữ liệu không bị mất khi tắt ứng dụng

---

## 🧩 Công nghệ và thư viện sử dụng

| Thành phần         | Công nghệ                                           |
| ------------------ | --------------------------------------------------- |
| Ngôn ngữ lập trình | Python 3.13                                         |
| Giao diện chính    | **CustomTkinter** (Modern UI Framework)           |
| Giao diện phụ trợ  | Tkinter (Treeview, messagebox)                     |
| Cơ sở dữ liệu      | MySQL 8.0+                                         |
| Kiến trúc         | **MVC Pattern** (Model-View-Controller)            |
| Thư viện chính    | `customtkinter`, `mysql-connector-python`          |
| Thư viện hỗ trợ   | `python-dotenv`, `Pillow`, `tkcalendar`            |
| Báo cáo/Export    | `openpyxl`, `reportlab` (tùy chọn mở rộng)         |
| IDE khuyến nghị   | Visual Studio Code / PyCharm                       |
| Hệ điều hành      | Windows 10+, macOS, Linux Ubuntu 20.04+           |

### 🔧 Thư viện chi tiết

| Thư viện | Phiên bản | Mục đích |
|----------|-----------|----------|
| `customtkinter` | Latest | Giao diện hiện đại, đẹp mắt |
| `mysql-connector-python` | 9.1.0 | Kết nối Python ↔ MySQL |
| `python-dotenv` | 1.1.1 | Quản lý biến môi trường (.env) |
| `Pillow` | Latest | Xử lý hình ảnh (background, icons) |
| `tkcalendar` | 1.6.1 | Widget lịch chọn ngày sinh |
| `openpyxl` | 3.1.5 | Export dữ liệu ra Excel |
| `reportlab` | 4.2.2 | Tạo báo cáo PDF |

---

## ⚙️ Cài đặt và chạy chương trình

### 1️⃣ Yêu cầu hệ thống
- **Python**: 3.9+ (khuyến nghị 3.11+)
- **MySQL Server**: 8.0+ 
- **RAM**: Tối thiểu 4GB
- **Dung lượng**: ~50MB

### 2️⃣ Cài đặt môi trường

**Clone dự án về máy:**
```bash
git clone https://github.com/DuyCaChef/DoAn_Python.NhomDoAn02.Lop_DH24TH1_NhomTH1_ToTH1.git
cd DoAn_Python.NhomDoAn02.Lop_DH24TH1_NhomTH1_ToTH1
```

**Tạo môi trường ảo và cài thư viện:**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Cấu hình Database
**Tạo file `.env` trong thư mục gốc:**
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=employee_management
```

**Khởi tạo database:**
```bash
python init_db.py
```

**Tạo dữ liệu mẫu (tùy chọn):**
```bash
python seed_mock.py
```

### 4️⃣ Chạy ứng dụng
```bash
python main.py
```

### 🔐 Đăng nhập hệ thống
- **Username**: `admin`
- **Password**: `admin123`

*(Hoặc tài khoản bạn đã tạo trong quá trình seed data)*

## 🧱 Cấu trúc thư mục dự án

```
├── 📁 app/                              # Thư mục chính chứa mã nguồn ứng dụng
│   ├── 📁 controllers/                  # Tầng Controller (MVC Pattern)
│   │   ├── auth_controller.py           # Xử lý logic đăng nhập/xác thực
│   │   ├── employee_controller.py       # Xử lý logic CRUD nhân viên
│   │   └── __init__.py
│   │
│   ├── 📁 database/                     # Tầng kết nối và truy vấn Database
│   │   ├── connection.py                # Quản lý kết nối MySQL
│   │   ├── db_config.py                 # Cấu hình database
│   │   ├── db_init.py                   # Khởi tạo database và bảng
│   │   ├── auth_queries.py              # Truy vấn liên quan đến xác thực
│   │   ├── employee_queries.py          # Truy vấn CRUD nhân viên
│   │   ├── queries.py                   # Truy vấn tổng quát
│   │   └── __init__.py
│   │
│   ├── 📁 models/                       # Tầng Model (MVC Pattern)
│   │   ├── employee.py                  # Định nghĩa class Employee
│   │   └── __init__.py
│   │
│   ├── 📁 views/                        # Tầng View - Giao diện người dùng
│   │   ├── login_window.py              # Cửa sổ đăng nhập (CustomTkinter)
│   │   ├── main_window.py               # Giao diện chính (CustomTkinter)
│   │   ├── employee_form.py             # Form thêm/sửa nhân viên
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── 📁 assets/                           # Tài nguyên tĩnh
│   ├── 📁 images/                       # Hình ảnh, icon cho ứng dụng
│   │   ├── bg_login.jpg                 # Background đăng nhập
│   │   └── Header.jpg                   # Header image
│   └── 📁 image/                        # (Legacy folder - sẽ được dọn dẹp)
│
├── 📄 main.py                           # 🚀 Entry point - Điểm khởi chạy chính
├── 📄 init_db.py                        # Script khởi tạo database
├── 📄 seed_mock.py                      # Script tạo dữ liệu mẫu
├── 📄 requirements.txt                  # Danh sách thư viện Python cần thiết
├── 📄 README.md                         # Tài liệu hướng dẫn dự án
└── 📄 .gitignore                        # Danh sách file/folder bỏ qua trong Git
```

### 📋 Mô tả chi tiết các thư mục

| Thư mục/File | Mô tả |
|--------------|-------|
| **`app/`** | Thư mục chính chứa toàn bộ mã nguồn theo kiến trúc MVC |
| **`controllers/`** | Xử lý logic nghiệp vụ, kết nối giữa View và Model |
| **`database/`** | Quản lý kết nối MySQL và các truy vấn SQL |
| **`models/`** | Định nghĩa cấu trúc dữ liệu (Employee class) |
| **`views/`** | Giao diện người dùng với CustomTkinter hiện đại |
| **`assets/images/`** | Lưu trữ ảnh nền, icon và tài nguyên giao diện |
| **`main.py`** | File chính để chạy ứng dụng |
| **`init_db.py`** | Tự động tạo database và bảng MySQL |
| **`seed_mock.py`** | Tạo dữ liệu mẫu để test |

### 🏗️ Kiến trúc MVC (Model-View-Controller)

- **Model (`models/`)**: Quản lý dữ liệu và logic nghiệp vụ
- **View (`views/`)**: Giao diện người dùng (CustomTkinter)
- **Controller (`controllers/`)**: Điều phối giữa Model và View
- **Database (`database/`)**: Tầng truy cập dữ liệu MySQL
