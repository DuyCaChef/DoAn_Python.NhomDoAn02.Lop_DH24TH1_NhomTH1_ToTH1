# DoAn_Python.NhomDoAn02.Lop_DH24TH1_NhomTH1_ToTH1

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

## 🎯 Mục tiêu đồ án

Xây dựng một **ứng dụng quản lý nhân sự** có giao diện thân thiện bằng **Tkinter**, kết nối với **MySQL** để lưu trữ dữ liệu lâu dài.  
Ứng dụng cho phép người dùng:

- Thêm, sửa, xóa và lưu thông tin nhân viên (CRUD)
- Hiển thị danh sách nhân viên
- Tìm kiếm, chọn, và cập nhật thông tin nhân viên
- Giao diện trực quan, dễ thao tác, dữ liệu không bị mất khi tắt ứng dụng

---

## 🧩 Công nghệ và thư viện sử dụng

| Thành phần         | Công nghệ                              |
| ------------------ | -------------------------------------- |
| Ngôn ngữ lập trình | Python 3.13                            |
| Giao diện          | Tkinter                                |
| Cơ sở dữ liệu      | MySQL                                  |
| Thư viện hỗ trợ    | `mysql-connector-python`, `tkcalendar` |
| IDE khuyến nghị    | Visual Studio Code / PyCharm           |
| Hệ điều hành       | Windows 10 hoặc cao hơn                |

---

## ⚙️ Cài đặt và chạy chương trình

### 1️⃣ Cài đặt môi trường

Clone dự án về máy:

```bash
git clone https://github.com/<ten_tai_khoan>/QL_NhanSu_Python.git
cd QL_NhanSu_Python
```

Tạo môi trường ảo và cài thư viện:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

```


```

Cấu trúc thư mục dự án:
QL_NhanSu_Python/
│
├── main.py # Điểm khởi đầu ứng dụng (chạy Tkinter)
│
├── database/
│ ├── db_config.py # Cấu hình kết nối MySQL
│ ├── db_init.py # Tự tạo CSDL + bảng khi chạy lần đầu
│ └── queries.py # Các hàm truy vấn (thêm, xóa, sửa, tìm kiếm)
│
├── gui/
│ ├── main_window.py # Giao diện chính (Tkinter + Treeview)
│ ├── form_employee.py # Form nhập/sửa nhân viên
│ └── components/ # (Tùy chọn) các widget, popup phụ
│
├── models/
│ └── employee.py # Lớp mô tả đối tượng nhân viên
│
├── assets/
│ ├── icons/ # Ảnh icon nút bấm, logo
│ └── styles/ # file theme, CSS-like style (nếu có)
│
├── utils/
│ ├── validators.py # Hàm kiểm tra dữ liệu nhập vào (mã số, ngày sinh,…)
│ └── helpers.py # Các hàm tiện ích chung
│
├── requirements.txt # Danh sách thư viện cần cài
├── README.md # Mô tả dự án (dùng trên GitHub)
└── .gitignore # Loại bỏ file rác khi commit
