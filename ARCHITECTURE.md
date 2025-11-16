# Kiến trúc Component-Based với Dialogs

## Cấu trúc thư mục

```
app/views/
├── main_window.py                 # Main window (155 lines)
│
├── components/                    # Components chính
│   ├── header.py                  # Header component
│   ├── base_tab.py               # Abstract base class
│   │
│   └── tabs/                      # Tabs theo role
│       ├── director/
│       │   ├── employee_management_tab.py    (289 lines)
│       │   ├── account_management_tab.py
│       │   └── system_data_tab.py
│       │
│       ├── manager/
│       │   ├── team_management_tab.py        (289 lines) 
│       │   └── approval_tab.py
│       │
│       └── employee/
│           ├── profile_tab.py
│           └── leave_request_tab.py
│
└── dialogs/                       # ⭐ NEW: Dialog forms
    ├── __init__.py
    ├── employee_form_dialog.py    (429 lines)
    ├── department_form_dialog.py  (TODO)
    ├── position_form_dialog.py    (TODO)
    └── README.md
```

## Luồng hoạt động

```
┌─────────────────────────────────────────────────────────────┐
│                      MainWindow                              │
│  - Hiển thị header                                          │
│  - Tạo tabs theo role                                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ├─────► Header Component
                   │       - User info
                   │       - Logout button
                   │
                   └─────► Tabs (Director/Manager/Employee)
                           │
                           ├─► EmployeeManagementTab (Director)
                           │   │
                           │   ├─ Fetch data từ DB
                           │   ├─ Hiển thị table
                           │   │
                           │   └─ Actions:
                           │      ├─ Add    ──┐
                           │      ├─ Edit   ──┤
                           │      ├─ View   ──┼──► EmployeeFormDialog
                           │      └─ Delete   │    - mode: add/edit/view
                           │                  │    - validation
                           │                  │    - save to DB
                           └─► TeamManagementTab (Manager)  │    - callback: refresh
                               │                            │
                               ├─ Fetch team data          │
                               ├─ Hiển thị table           │
                               │                            │
                               └─ Actions:                  │
                                  ├─ Add    ──────────────┘
                                  ├─ Edit   ──────────────┘
                                  └─ View   ──────────────┘
```

## So sánh trước và sau

### ❌ Trước khi refactor (Monolithic)

```python
# team_management_tab.py - 459 dòng

class TeamManagementTab:
    def add_employee(self):
        # 200 dòng code tạo dialog
        dialog = ctk.CTkToplevel()
        # ... tạo form fields
        # ... validation
        # ... save logic
        
    def edit_employee(self):
        # 200 dòng code tương tự
        # Duplicate logic với add_employee
        
    def view_employee(self):
        # 150 dòng code tương tự
        # Duplicate logic
```

**Vấn đề:**
- ❌ Code dài, khó đọc
- ❌ Duplicate logic
- ❌ Khó bảo trì
- ❌ Không tái sử dụng được

### ✅ Sau khi refactor (Component-Based)

```python
# team_management_tab.py - 289 dòng

from app.views.dialogs.employee_form_dialog import EmployeeFormDialog

class TeamManagementTab:
    def add_employee(self):
        EmployeeFormDialog(
            parent=self.container,
            employee_controller=self.employee_controller,
            auth_controller=self.auth_controller,
            mode="add",
            on_success=self.fetch_data
        )
        
    def edit_employee(self, employee):
        EmployeeFormDialog(
            parent=self.container,
            employee_controller=self.employee_controller,
            auth_controller=self.auth_controller,
            mode="edit",
            employee_data=employee,
            on_success=self.fetch_data
        )
        
    def view_employee(self, employee):
        EmployeeFormDialog(
            parent=self.container,
            employee_controller=self.employee_controller,
            auth_controller=self.auth_controller,
            mode="view",
            employee_data=employee
        )
```

```python
# employee_form_dialog.py - 429 dòng (RIÊNG BIỆT)

class EmployeeFormDialog:
    """
    Dialog tái sử dụng được cho:
    - Director's EmployeeManagementTab
    - Manager's TeamManagementTab
    - Employee's ProfileTab (view mode)
    """
    
    def __init__(self, parent, employee_controller, auth_controller, 
                 mode="add", employee_data=None, on_success=None):
        # Xử lý 3 modes: add/edit/view
        # Validation đầy đủ
        # Error handling
        # Callback refresh
```

**Lợi ích:**
- ✅ Code ngắn gọn, dễ đọc
- ✅ Không duplicate
- ✅ Dễ bảo trì (sửa 1 chỗ, áp dụng toàn bộ)
- ✅ Tái sử dụng trên nhiều tab
- ✅ Tuân thủ Single Responsibility Principle
- ✅ Dễ test và debug

## Metrics

| Metric | Trước | Sau | Cải thiện |
|--------|-------|-----|-----------|
| Lines/file (tab) | 459 | 289 | **-37%** ⬇️ |
| Duplicate code | Nhiều | Không | **-100%** ⬇️ |
| Reusability | 0% | 100% | **+100%** ⬆️ |
| Maintainability | Khó | Dễ | **+∞** ⬆️ |
| Dialog files | 0 | 1+ | **+∞** ⬆️ |

## Kế hoạch mở rộng

```
dialogs/
├── employee_form_dialog.py   ✅ DONE
├── department_form_dialog.py ⏳ TODO
├── position_form_dialog.py   ⏳ TODO
├── role_form_dialog.py       ⏳ TODO
├── user_form_dialog.py       ⏳ TODO
└── leave_request_dialog.py   ⏳ TODO
```

Mỗi dialog sẽ có:
- 3 modes: add/edit/view
- Validation đầy đủ
- Error handling
- Callback để refresh
- UI nhất quán

---
*Kiến trúc được thiết kế theo nguyên tắc: Separation of Concerns & DRY (Don't Repeat Yourself)*
