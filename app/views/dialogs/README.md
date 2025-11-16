# Dialogs Package

Package chứa các dialog form phụ được gọi từ các tab chính.

## Mục đích
Tách biệt logic UI của các form dialog ra khỏi tab chính để:
- Dễ bảo trì và sửa lỗi
- Tái sử dụng code (1 dialog có thể dùng cho nhiều tab)
- Giảm kích thước file của các tab chính
- Tuân theo nguyên tắc Single Responsibility

## Cấu trúc

```
app/views/dialogs/
├── __init__.py                    # Export các dialog
├── employee_form_dialog.py        # Dialog CRUD nhân viên
├── department_form_dialog.py      # Dialog CRUD phòng ban (TODO)
├── position_form_dialog.py        # Dialog CRUD chức vụ (TODO)
└── README.md                      # File này
```

## Cách sử dụng

### 1. Employee Form Dialog

Dialog đa chức năng cho thêm/sửa/xem nhân viên.

**Import:**
```python
from app.views.dialogs.employee_form_dialog import EmployeeFormDialog
```

**Thêm nhân viên mới:**
```python
EmployeeFormDialog(
    parent=self.container,
    employee_controller=self.employee_controller,
    auth_controller=self.auth_controller,
    mode="add",
    on_success=self.fetch_data  # Callback để refresh data
)
```

**Xem thông tin nhân viên:**
```python
EmployeeFormDialog(
    parent=self.container,
    employee_controller=self.employee_controller,
    auth_controller=self.auth_controller,
    mode="view",
    employee_data=employee_dict  # Dict chứa thông tin nhân viên
)
```

**Sửa thông tin nhân viên:**
```python
EmployeeFormDialog(
    parent=self.container,
    employee_controller=self.employee_controller,
    auth_controller=self.auth_controller,
    mode="edit",
    employee_data=employee_dict,
    on_success=self.fetch_data
)
```

## Các mode hoạt động

| Mode | Mô tả | Read-only | Buttons |
|------|-------|-----------|---------|
| `add` | Thêm nhân viên mới | ❌ | Lưu, Hủy |
| `edit` | Sửa thông tin | ❌ | Lưu, Hủy |
| `view` | Xem chi tiết | ✅ | Đóng |

## Tính năng

### EmployeeFormDialog

✅ **Validation đầy đủ:**
- Required fields: Mã NV, họ, tên, email, ngày sinh, ngày vào làm
- Email format validation (regex)
- Date format validation (YYYY-MM-DD)
- Phone number validation (Vietnamese format)

✅ **Auto-fill thông minh:**
- Phòng ban tự động lấy từ manager (khi thêm mới)
- Manager_id tự động gán manager hiện tại

✅ **Dynamic Data Loading:** 🆕
- **Positions** load từ database (không hardcode)
- Hiển thị format: `"Position Title (Department Name)"`
- Tự động map `position_id` khi save
- Fallback về default positions nếu DB lỗi

✅ **UI/UX tốt:**
- Form scrollable khi content dài
- **Mouse wheel scroll** hỗ trợ đa nền tảng (Linux, Windows, Mac)
- Center screen
- Responsive buttons
- Focus vào field đầu tiên
- Color theme nhất quán

✅ **Error handling:**
- Try-catch để bắt lỗi database
- Hiển thị thông báo rõ ràng
- Parent window để modal đúng vị trí

## Kết quả refactoring

**Trước khi refactor:**
- `team_management_tab.py`: 459 dòng
- Code form trộn lẫn với code tab
- Khó bảo trì và mở rộng

**Sau khi refactor:**
- `team_management_tab.py`: 289 dòng (giảm 37%)
- `employee_form_dialog.py`: 429 dòng (tách riêng)
- Sạch sẽ, dễ bảo trì, tái sử dụng được

## TODO

- [ ] Tạo `DepartmentFormDialog` cho CRUD phòng ban
- [ ] Tạo `PositionFormDialog` cho CRUD chức vụ
- [ ] Tạo `RoleFormDialog` cho CRUD vai trò
- [ ] Tạo `UserFormDialog` cho CRUD tài khoản
- [x] ~~Load position list từ database~~ ✅ DONE (v1.1.0)
- [x] ~~Map position_id từ position_combo~~ ✅ DONE (v1.1.0)
- [ ] Filter positions theo department của user
- [ ] Thêm DatePicker widget cho ngày sinh và ngày vào làm
- [ ] Thêm avatar upload cho nhân viên

## Nguyên tắc khi thêm dialog mới

1. **Kế thừa pattern từ EmployeeFormDialog**
2. **Tuân thủ 3 mode: add/edit/view**
3. **Validation đầy đủ trước khi save**
4. **Sử dụng callback `on_success` để refresh data**
5. **Error handling với try-catch**
6. **UI nhất quán (colors, spacing, buttons)**
7. **Document rõ ràng trong docstring**

---
*Cập nhật lần cuối: 2024-11-16*
