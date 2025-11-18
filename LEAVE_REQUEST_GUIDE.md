# 📋 HƯỚNG DẪN TÍNH NĂNG YÊU CẦU NGHỈ PHÉP

## ✅ Đã hoàn thành

Tính năng **Yêu cầu nghỉ phép** đã được tích hợp hoàn chỉnh vào hệ thống quản lý nhân sự.

---

## 🗂️ Cấu trúc Database

### Bảng `leave_requests`

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| `id` | INT (PK) | ID yêu cầu |
| `employee_id` | INT (FK) | ID nhân viên gửi yêu cầu |
| `manager_id` | INT (FK) | ID quản lý phê duyệt |
| `leave_type` | ENUM | Loại nghỉ: `annual`, `sick`, `personal`, `unpaid` |
| `start_date` | DATE | Ngày bắt đầu nghỉ |
| `end_date` | DATE | Ngày kết thúc nghỉ |
| `total_days` | INT | Tổng số ngày nghỉ |
| `reason` | TEXT | Lý do nghỉ |
| `status` | ENUM | Trạng thái: `pending`, `approved`, `rejected` |
| `manager_note` | TEXT | Ghi chú của quản lý |
| `created_at` | TIMESTAMP | Ngày tạo |
| `updated_at` | TIMESTAMP | Ngày cập nhật |

---

## 📁 Files đã tạo/sửa

### 1. **Database Layer** - `app/database/leave_request_queries.py`

**Chức năng:**
- ✅ `create_leave_request()` - Tạo yêu cầu nghỉ phép mới
- ✅ `get_leave_requests_by_employee()` - Lấy danh sách yêu cầu của nhân viên
- ✅ `get_pending_requests_for_manager()` - Lấy yêu cầu chờ duyệt (cho Manager)
- ✅ `update_request_status()` - Duyệt/từ chối yêu cầu
- ✅ `get_request_by_id()` - Lấy chi tiết yêu cầu

**Đặc điểm:**
- Map loại nghỉ tiếng Việt ↔ Enum database
- Map trạng thái tiếng Việt (`Chờ duyệt`, `Đã duyệt`, `Đã từ chối`)
- Tự động lấy `manager_id` từ thông tin nhân viên

---

### 2. **Business Logic Layer** - `app/controllers/leave_request_controller.py`

**Chức năng:**
- ✅ `create_request()` - Tạo yêu cầu với validation đầy đủ
- ✅ `get_my_requests()` - Lấy yêu cầu của nhân viên
- ✅ `get_pending_requests_for_approval()` - Lấy yêu cầu chờ duyệt
- ✅ `approve_request()` - Duyệt yêu cầu
- ✅ `reject_request()` - Từ chối yêu cầu
- ✅ `get_request_detail()` - Xem chi tiết
- ✅ `can_edit_request()` - Kiểm tra quyền sửa/xóa

**Validation:**
- ✅ Kiểm tra đầy đủ thông tin
- ✅ Lý do tối thiểu 10 ký tự
- ✅ Định dạng ngày hợp lệ (YYYY-MM-DD)
- ✅ Ngày bắt đầu ≤ Ngày kết thúc
- ✅ Không được chọn ngày quá khứ
- ✅ Tối đa 30 ngày/lần
- ✅ Tự động tính `total_days`

---

### 3. **View Layer** - `app/views/components/tabs/employee/leave_request_tab.py`

**Giao diện:**

#### **Bên trái: Form gửi yêu cầu**
- 🔽 Loại nghỉ phép (ComboBox)
  - Nghỉ phép năm
  - Nghỉ ốm
  - Nghỉ việc riêng
  - Nghỉ không lương
- 📅 Từ ngày (Entry - YYYY-MM-DD)
- 📅 Đến ngày (Entry - YYYY-MM-DD)
- 💬 Lý do (Textbox)
- 📨 Nút "Gửi yêu cầu"

#### **Bên phải: Lịch sử yêu cầu**
- 📜 Danh sách các yêu cầu đã gửi
- Mỗi yêu cầu hiển thị:
  - 📋 Loại nghỉ phép
  - 📅 Từ ngày → Đến ngày (X ngày)
  - 💬 Lý do (rút gọn)
  - 🟠🟢🔴 Trạng thái (màu sắc)
  - 🕐 Ngày gửi
  - 👁 Nút "Xem chi tiết"

#### **Dialog chi tiết:**
- Hiển thị đầy đủ thông tin yêu cầu
- Lý do đầy đủ
- Ghi chú của quản lý (nếu có)
- Nút đóng

---

## 🎯 Luồng hoạt động

### **Nhân viên gửi yêu cầu:**

```
1. Nhân viên đăng nhập → Tab "Yêu cầu nghỉ phép"
2. Điền form:
   - Chọn loại nghỉ
   - Nhập từ ngày, đến ngày
   - Nhập lý do (≥10 ký tự)
3. Click "📨 Gửi yêu cầu"
4. Hiện MessageBox xác nhận
5. Click "Yes" → Lưu vào database
6. Form được clear, danh sách tự động reload
7. Yêu cầu mới hiện ở bên phải với status "🟠 Chờ duyệt"
```

### **Kiểm tra dữ liệu trong database:**

```python
# Test query
from app.database.leave_request_queries import LeaveRequestQueries

queries = LeaveRequestQueries()

# Xem yêu cầu của nhân viên ID = 1
requests = queries.get_leave_requests_by_employee(1)
print(requests)
```

Hoặc dùng MySQL:

```sql
-- Xem tất cả yêu cầu
SELECT 
    lr.id,
    CONCAT(e.first_name, ' ', e.last_name) as employee,
    lr.leave_type,
    lr.start_date,
    lr.end_date,
    lr.total_days,
    lr.status,
    lr.created_at
FROM leave_requests lr
INNER JOIN employees e ON lr.employee_id = e.id
ORDER BY lr.created_at DESC;
```

---

## 🧪 Test Case

### **Test 1: Tạo yêu cầu thành công**

**Input:**
- Loại: Nghỉ phép năm
- Từ ngày: 2025-11-20
- Đến ngày: 2025-11-22
- Lý do: "Về quê nghỉ lễ tết"

**Expected:**
- ✅ MessageBox xác nhận
- ✅ Lưu vào DB với status = `pending`
- ✅ Hiển thị trong lịch sử với màu 🟠

---

### **Test 2: Validation lỗi**

**Input:**
- Từ ngày: 2025-11-25
- Đến ngày: 2025-11-20 (nhỏ hơn start_date)

**Expected:**
- ❌ Error: "Ngày bắt đầu phải trước hoặc bằng ngày kết thúc!"

---

### **Test 3: Xem chi tiết**

**Action:**
- Click nút 👁 "Xem" ở một yêu cầu

**Expected:**
- ✅ Hiện dialog với đầy đủ thông tin
- ✅ Hiển thị lý do đầy đủ (không rút gọn)
- ✅ Hiển thị ghi chú manager (nếu có)

---

## 🎨 Màu sắc trạng thái

| Trạng thái | Màu | Hex Code |
|-----------|-----|----------|
| 🟠 Chờ duyệt | Orange | `#FFA500` |
| 🟢 Đã duyệt | Green | `#27AE60` |
| 🔴 Đã từ chối | Red | `#E74C3C` |

---

## 🔧 Troubleshooting

### **Lỗi: "Không tìm thấy thông tin nhân viên"**

**Nguyên nhân:**
- User chưa login hoặc session hết hạn
- User không có `employee_id`

**Giải pháp:**
- Đăng nhập lại
- Kiểm tra bảng `users` có link đến `employees` không

---

### **Lỗi: "Không thể nghỉ quá 30 ngày"**

**Nguyên nhân:**
- Khoảng thời gian quá dài

**Giải pháp:**
- Chia thành nhiều yêu cầu nhỏ hơn

---

### **Dữ liệu không hiển thị**

**Kiểm tra:**

```sql
-- Xem có dữ liệu không
SELECT COUNT(*) FROM leave_requests;

-- Xem yêu cầu của nhân viên cụ thể
SELECT * FROM leave_requests WHERE employee_id = 1;
```

---

## 📝 TODO (Tương lai)

- [ ] Thêm tính năng **Sửa yêu cầu** (chỉ khi status = pending)
- [ ] Thêm tính năng **Hủy yêu cầu**
- [ ] Tab **Manager** để duyệt/từ chối yêu cầu
- [ ] Thống kê số ngày nghỉ còn lại trong năm
- [ ] Email notification khi có yêu cầu mới/được duyệt
- [ ] Export danh sách yêu cầu ra Excel/PDF
- [ ] Calendar view để xem lịch nghỉ

---

## ✨ Tính năng đã implement

✅ **Form gửi yêu cầu nghỉ phép**
✅ **Validation đầy đủ (ngày, lý do, định dạng)**
✅ **Lưu vào database MySQL**
✅ **Hiển thị lịch sử yêu cầu**
✅ **Xem chi tiết từng yêu cầu**
✅ **Màu sắc trạng thái trực quan**
✅ **MessageBox xác nhận trước khi gửi**
✅ **Auto reload sau khi submit**
✅ **Map tiếng Việt ↔ Enum**
✅ **Tự động tính số ngày nghỉ**
✅ **Lấy manager_id từ employee**

---

**Người thực hiện:** GitHub Copilot  
**Ngày:** 18/11/2025  
**Trạng thái:** ✅ Hoàn thành và sẵn sàng sử dụng
