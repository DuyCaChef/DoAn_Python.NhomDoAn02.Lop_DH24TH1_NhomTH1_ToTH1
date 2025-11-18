# Hướng dẫn Setup Database

## Bước 1: Khởi tạo Database Schema

Chạy script để tạo các bảng trong database:

```bash
python3 init_db.py
```

Script này sẽ tạo các bảng:
- `departments` - Phòng ban
- `positions` - Chức vụ
- `employees` - Nhân viên
- `leave_requests` - Yêu cầu nghỉ phép
- `users` - Tài khoản đăng nhập

## Bước 2: Seed Dữ liệu mẫu

Chạy script để insert dữ liệu mẫu vào database:

```bash
python3 seed_database.py
```

Script này sẽ tạo:
- **6 Departments**: IT, Marketing, Sales, HR, Finance, Operations
- **15 Positions**: Các chức vụ từ Manager đến Junior/Assistant
- **14 Employees**: Bao gồm Director, Managers và Employees (tất cả đều có salary)
- **8 Leave Requests**: Yêu cầu nghỉ phép mẫu với nhiều trạng thái khác nhau

## Bước 3: Đăng nhập ứng dụng

Sau khi seed xong, bạn có thể đăng nhập bằng các tài khoản sau:

### 🔑 Tài khoản Director
- **Username**: `director@company.com`
- **Password**: `123456`
- **Quyền**: Xem tất cả nhân viên, quản lý toàn bộ hệ thống

### 🔑 Tài khoản Manager (IT)
- **Username**: `it_manager@company.com`
- **Password**: `123456`
- **Quyền**: Quản lý nhân viên trong team, duyệt yêu cầu nghỉ phép

### 🔑 Tài khoản Employee
- **Username**: `hai_nguyen@company.com`
- **Password**: `123456`
- **Quyền**: Xem thông tin cá nhân, tạo yêu cầu nghỉ phép

## Dữ liệu đã tạo

### Departments (6)
1. IT - Information Technology
2. Marketing - Marketing Department
3. Sales - Sales Department
4. HR - Human Resources
5. Finance - Finance Department
6. Operations - Operations Department

### Employees (14)
- **1 Director** (Nguyễn Văn An) - Salary: 50,000,000 VNĐ
- **5 Managers** - Salary: 50,000,000 VNĐ mỗi người
- **8 Employees** - Salary: 15,000,000 - 25,000,000 VNĐ

### Leave Requests (8)
- Pending: 5 yêu cầu
- Approved: 2 yêu cầu
- Rejected: 1 yêu cầu

## Lưu ý

- Mật khẩu mặc định cho tất cả tài khoản là: `123456`
- Dữ liệu có thể được reset bất cứ lúc nào bằng cách chạy lại `seed_database.py`
- Script sẽ XÓA dữ liệu cũ và tạo lại từ đầu

## Troubleshooting

Nếu gặp lỗi khi seed database:
1. Kiểm tra kết nối database trong `app/database/db_config.py`
2. Đảm bảo MySQL service đang chạy
3. Kiểm tra user có quyền CREATE, INSERT, DELETE trên database
