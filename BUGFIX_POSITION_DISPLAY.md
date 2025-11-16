# Bug Fix: Position không hiển thị trong Table

## 🐛 Vấn đề

Cột "Chức vụ" trong table view (Director và Manager tabs) hiển thị **trống** mặc dù database có đầy đủ dữ liệu positions.

### Screenshot vấn đề:
```
Mã NV | Họ và tên      | Email              | SĐT        | Chức vụ | Thao tác
17    | Nguyễn Văn Hải | hai_nguyen@...     | 0911111111 |         | 👁 ✏
18    | Trần Thị Hoa   | hoa_tran@...       | 0922222222 |         | 👁 ✏
23    | Duy            | duy@gmail.com      |            |         | 👁 ✏
```

Cột "Chức vụ" bị **trống hoàn toàn**!

## 🔍 Root Cause

**File:** `app/views/components/tabs/director/employee_management_tab.py` (dòng 195)
**File:** `app/views/components/tabs/manager/team_management_tab.py` (dòng 177)

Code đang dùng **sai tên field**:

```python
# ❌ SAI - Dùng 'role_name' (không tồn tại trong query)
(employee.get('role_name', ''), 0.12),
```

Nhưng trong query `get_all_employees()` (file `employee_queries.py`), field trả về là:

```sql
SELECT 
    ...
    p.title as position_title,  -- ✅ Đây mới đúng!
    ...
FROM employees e
LEFT JOIN positions p ON e.position_id = p.id
```

## ✅ Giải pháp

Đổi `role_name` thành `position_title`:

### employee_management_tab.py (Director)
```python
# TRƯỚC:
data = [
    ...
    (employee.get('role_name', ''), 0.12),  # ❌ SAI
    ...
]

# SAU:
data = [
    ...
    (employee.get('position_title', ''), 0.12),  # ✅ ĐÚNG
    ...
]
```

### team_management_tab.py (Manager)
```python
# TRƯỚC:
data = [
    ...
    (employee.get('role_name', ''), 0.15),  # ❌ SAI
]

# SAU:
data = [
    ...
    (employee.get('position_title', ''), 0.15),  # ✅ ĐÚNG
]
```

## 🎯 Kết quả sau khi fix

```
Mã NV | Họ và tên      | Email              | SĐT        | Chức vụ        | Thao tác
17    | Nguyễn Văn Hải | hai_nguyen@...     | 0911111111 | IT Manager     | 👁 ✏
18    | Trần Thị Hoa   | hoa_tran@...       | 0922222222 | HR Specialist  | 👁 ✏
23    | Duy            | duy@gmail.com      |            | Employee       | 👁 ✏
```

Cột "Chức vụ" giờ hiển thị **đầy đủ**! ✅

## 📋 Files đã sửa

1. `app/views/components/tabs/director/employee_management_tab.py` - Line 195
2. `app/views/components/tabs/manager/team_management_tab.py` - Line 177

## 🧪 Test Cases

- [x] Director tab → Cột "Chức vụ" hiển thị positions
- [x] Manager tab → Cột "Chức vụ" hiển thị positions
- [x] View employee → Position hiển thị đúng
- [x] Edit employee → Position combo load đúng
- [x] Add employee → Position combo load đúng

## ⚠️ Lưu ý

**Confusion về naming:**
- `role_name` → Vai trò hệ thống (Director, Manager, Employee) - từ bảng `roles`
- `position_title` → Chức vụ công việc (IT Manager, HR Specialist, etc.) - từ bảng `positions`

**Mapping trong database:**
```
users → roles: "Director", "Manager", "Employee" (vai trò đăng nhập)
employees → positions: "IT Manager", "HR Specialist", etc. (chức danh công việc)
```

Không nên nhầm lẫn 2 khái niệm này!

## 🚀 Next Steps

- [ ] Thống nhất naming convention trong toàn bộ codebase
- [ ] Thêm type hints để tránh nhầm lẫn field names
- [ ] Document rõ sự khác biệt giữa `role` vs `position`

---
*Fixed: 2024-11-16*
*Bug found by: User testing*
*Impact: HIGH - Ảnh hưởng đến tất cả table views*
