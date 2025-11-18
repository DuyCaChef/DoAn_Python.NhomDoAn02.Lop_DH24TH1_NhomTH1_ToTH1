# 📋 HƯỚNG DẪN TEST - TAB DUYỆT NGHỈ PHÉP (MANAGER)

## ✅ Đã hoàn thành

Tính năng **Duyệt yêu cầu nghỉ phép** cho Manager đã được implement đầy đủ!

---

## 🎯 Chức năng đã implement

### 1. **Tab ApprovalTab - Manager**

#### **Bộ lọc trạng thái:**
- 🔽 ComboBox với 4 lựa chọn:
  - **Tất cả**: Hiển thị tất cả yêu cầu (pending, approved, rejected)
  - **Chờ duyệt**: Chỉ hiển thị yêu cầu pending
  - **Đã duyệt**: Chỉ hiển thị yêu cầu approved
  - **Từ chối**: Chỉ hiển thị yêu cầu rejected
- 🔄 Nút "Làm mới" để reload dữ liệu

#### **Bảng yêu cầu:**
- 📊 Header: Nhân viên | Loại nghỉ | Từ ngày | Đến ngày | Lý do | Thao tác
- 📋 Mỗi hàng hiển thị:
  - Tên nhân viên
  - Loại nghỉ (tiếng Việt)
  - Ngày bắt đầu & kết thúc
  - Lý do (rút gọn 30 ký tự)
  - 3 nút action:
    - ✓ **Duyệt** (màu xanh)
    - ✗ **Từ chối** (màu đỏ)
    - 👁 **Xem chi tiết** (màu xanh dương)

---

### 2. **Duyệt yêu cầu (Approve)**

**Luồng:**
1. Click nút **✓** hoặc **✓ Duyệt** trong dialog
2. Hiện MessageBox xác nhận
3. Click "Yes" → Hiện dialog nhập ghi chú (tùy chọn)
4. Nhập ghi chú (hoặc bỏ qua) → OK
5. Lưu vào database với:
   - `status = 'approved'`
   - `manager_note = ghi chú` (nếu có)
   - `updated_at = NOW()`
6. Hiện thông báo thành công
7. Reload danh sách (yêu cầu biến mất khỏi "Chờ duyệt")

**Validation:**
- ✅ Kiểm tra manager_id hợp lệ
- ✅ Kiểm tra quyền (chỉ manager của yêu cầu đó)

---

### 3. **Từ chối yêu cầu (Reject)**

**Luồng:**
1. Click nút **✗** hoặc **✗ Từ chối** trong dialog
2. Hiện dialog nhập lý do từ chối (BẮT BUỘC)
3. Nhập lý do (≥5 ký tự) → OK
4. Hiện MessageBox xác nhận với lý do
5. Click "Yes" → Lưu vào database:
   - `status = 'rejected'`
   - `manager_note = lý do từ chối`
   - `updated_at = NOW()`
6. Hiện thông báo thành công
7. Reload danh sách

**Validation:**
- ❌ Nếu không nhập lý do → Warning "Vui lòng nhập lý do từ chối!"
- ❌ Nếu lý do < 5 ký tự → Lỗi từ controller

---

### 4. **Xem chi tiết yêu cầu**

**Dialog hiển thị:**
- 📋 **Tiêu đề:** "Chi tiết yêu cầu nghỉ phép"
- 📏 **Kích thước:** 550x650px
- 🔒 **Modal:** Grab set (blocking)

**Thông tin hiển thị:**
- 👤 Nhân viên: Nguyễn Văn A
- 🆔 Mã NV: NV001
- 📋 Loại nghỉ: Nghỉ phép năm
- 📅 Từ ngày: 2025-12-01
- 📅 Đến ngày: 2025-12-05
- 🔢 Số ngày: 5 ngày
- 📆 Ngày gửi: 18/11/2025 10:30
- 💬 Lý do: (Textbox với nội dung đầy đủ, read-only)

**Nút action:**
- ✓ **Duyệt** (xanh lá) → Đóng dialog → Gọi `approve_request()`
- ✗ **Từ chối** (đỏ) → Đóng dialog → Gọi `reject_request()`
- **Đóng** (xám) → Đóng dialog

---

## 🧪 Test Cases

### **Test 1: Hiển thị danh sách yêu cầu**

**Điều kiện:**
- Đăng nhập với tài khoản **Manager**
- Có ít nhất 1 nhân viên thuộc quản lý đã gửi yêu cầu

**Bước test:**
1. Vào tab "Duyệt yêu cầu nghỉ phép"
2. Kiểm tra filter mặc định = "Chờ duyệt"
3. Xem danh sách yêu cầu

**Kết quả mong đợi:**
- ✅ Hiển thị tất cả yêu cầu status = pending
- ✅ Mỗi hàng có đầy đủ thông tin
- ✅ 3 nút action hoạt động

---

### **Test 2: Duyệt yêu cầu (có ghi chú)**

**Bước test:**
1. Click nút ✓ "Duyệt" tại một yêu cầu
2. Confirm "Yes" trong MessageBox
3. Nhập ghi chú: "Đồng ý. Chúc bạn nghỉ ngơi vui vẻ!"
4. Click OK

**Kết quả mong đợi:**
- ✅ Hiện "Thành công" → "Đã duyệt yêu cầu thành công!"
- ✅ Yêu cầu biến mất khỏi danh sách "Chờ duyệt"
- ✅ Database: status = 'approved', manager_note = ghi chú

**Kiểm tra database:**
```sql
SELECT id, status, manager_note, updated_at 
FROM leave_requests 
WHERE id = <request_id>;
```

---

### **Test 3: Duyệt yêu cầu (không ghi chú)**

**Bước test:**
1. Click ✓ "Duyệt"
2. Confirm "Yes"
3. Bỏ qua dialog ghi chú (Cancel hoặc để trống)

**Kết quả mong đợi:**
- ✅ Vẫn duyệt thành công
- ✅ manager_note = NULL hoặc empty

---

### **Test 4: Từ chối yêu cầu**

**Bước test:**
1. Click ✗ "Từ chối"
2. Nhập lý do: "Thời gian này công việc quá bận, vui lòng chọn thời gian khác"
3. Confirm "Yes"

**Kết quả mong đợi:**
- ✅ Hiện "Thành công" → "Đã từ chối yêu cầu thành công!"
- ✅ Database: status = 'rejected', manager_note = lý do

---

### **Test 5: Từ chối yêu cầu (thiếu lý do)**

**Bước test:**
1. Click ✗ "Từ chối"
2. Để trống lý do → OK

**Kết quả mong đợi:**
- ❌ Warning: "Vui lòng nhập lý do từ chối!"
- ❌ Không lưu database

---

### **Test 6: Xem chi tiết yêu cầu**

**Bước test:**
1. Click 👁 "Xem chi tiết"
2. Đọc thông tin
3. Click "Đóng"

**Kết quả mong đợi:**
- ✅ Dialog hiển thị đầy đủ thông tin
- ✅ Lý do hiển thị full (không rút gọn)
- ✅ Có 3 nút: Duyệt, Từ chối, Đóng

---

### **Test 7: Duyệt/Từ chối từ dialog chi tiết**

**Bước test:**
1. Xem chi tiết yêu cầu
2. Click "✓ Duyệt" hoặc "✗ Từ chối"
3. Làm theo flow bình thường

**Kết quả mong đợi:**
- ✅ Dialog đóng tự động
- ✅ Hiện confirm/input theo flow
- ✅ Lưu database thành công

---

### **Test 8: Filter theo trạng thái**

**Bước test:**
1. Chọn filter = "Tất cả" → Xem danh sách
2. Chọn filter = "Đã duyệt" → Xem danh sách
3. Chọn filter = "Từ chối" → Xem danh sách
4. Chọn filter = "Chờ duyệt" → Xem danh sách

**Kết quả mong đợi:**
- ✅ "Tất cả": Hiển thị tất cả (pending + approved + rejected)
- ✅ "Đã duyệt": Chỉ hiển thị approved
- ✅ "Từ chối": Chỉ hiển thị rejected
- ✅ "Chờ duyệt": Chỉ hiển thị pending

---

### **Test 9: Làm mới danh sách**

**Bước test:**
1. Click 🔄 "Làm mới"

**Kết quả mong đợi:**
- ✅ Reload lại danh sách
- ✅ Giữ nguyên filter hiện tại

---

## 📊 Database Schema Check

**Truy vấn kiểm tra:**

```sql
-- Xem tất cả yêu cầu của manager ID = 2
SELECT 
    lr.id,
    CONCAT(e.first_name, ' ', e.last_name) as employee,
    lr.leave_type,
    lr.start_date,
    lr.end_date,
    lr.status,
    lr.manager_note,
    lr.created_at,
    lr.updated_at
FROM leave_requests lr
INNER JOIN employees e ON lr.employee_id = e.id
WHERE lr.manager_id = 2
ORDER BY lr.created_at DESC;
```

---

## 🔗 Files đã sửa/tạo

1. **app/views/components/tabs/manager/approval_tab.py**
   - ✅ Thêm `__init__` với LeaveRequestController
   - ✅ Implement `fetch_data()` với filter
   - ✅ Implement `_create_request_row()` với 3 nút action
   - ✅ Implement `approve_request()` với confirm + note
   - ✅ Implement `reject_request()` với required reason
   - ✅ Implement `_view_request_detail()` với dialog chi tiết

2. **app/database/leave_request_queries.py**
   - ✅ Thêm `get_all_requests_for_manager()` với status filter

3. **app/controllers/leave_request_controller.py**
   - ✅ Thêm `get_all_requests_for_manager()` với mapping

---

## 🎉 Kết luận

**Tính năng đã hoàn thiện 100%:**
- ✅ Hiển thị danh sách yêu cầu
- ✅ Filter theo trạng thái
- ✅ Duyệt yêu cầu (approve)
- ✅ Từ chối yêu cầu (reject)
- ✅ Xem chi tiết yêu cầu
- ✅ Validation đầy đủ
- ✅ Lưu database chính xác
- ✅ UI/UX trực quan

**Hãy test ngay:**
1. Đăng nhập với tài khoản **Manager**
2. Vào tab "Duyệt yêu cầu nghỉ phép"
3. Test tất cả chức năng theo hướng dẫn trên!

---

**Ngày:** 18/11/2025  
**Trạng thái:** ✅ HOÀN THÀNH
