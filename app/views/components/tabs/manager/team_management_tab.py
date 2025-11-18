"""
Team Management Tab - Manager
Tab quản lý nhân viên trong phòng ban (Manager)
"""
import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.views.components.tabs.base_tab import BaseTab
from app.controllers.employee_controller import EmployeeController
from app.views.dialogs.employee_form_dialog import EmployeeFormDialog


class TeamManagementTab(BaseTab):
    """Tab quản lý nhân viên trong phòng - Manager"""
    
    def __init__(self, parent, auth_controller):
        # Gọi super().__init__() để set parent và auth_controller
        super().__init__(parent, auth_controller)
        
        # Tạo employee_controller SAU KHI đã có auth_controller
        from app.controllers.employee_controller import EmployeeController
        self.employee_controller = EmployeeController(auth_controller)
        
        # Bây giờ mới gọi setup_ui()
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện tab quản lý team"""
        # Title
        dept_name = self.auth_controller.current_user_data.get('department_name', 'Phòng ban')
        title = self.create_section_label(self.container, f"👥 Quản lý nhân viên - {dept_name}")
        title.pack(pady=(0, 20))
        
        # Search và Action bar
        self._create_search_and_action_bar()
        
        # Table
        self._create_team_table()
        
        # Load data
        self.fetch_data()
    
    def _create_search_and_action_bar(self):
        """Tạo thanh tìm kiếm và actions"""
        action_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        # Search
        self.search_entry = ctk.CTkEntry(
            action_frame,
            placeholder_text="Tìm kiếm nhân viên...",
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_team())
        
        search_btn = self.create_button(
            action_frame,
            "🔍 Tìm",
            self.search_team,
            fg_color="#3498DB"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = self.create_button(
            action_frame,
            "🔄 Làm mới",
            self.fetch_data,
            fg_color="#95A5A6"
        )
        refresh_btn.pack(side="left", padx=(0, 10))
        
        # Add button
        add_btn = self.create_button(
            action_frame,
            "➕ Thêm nhân viên",
            self.add_employee,
            fg_color="#27AE60"
        )
        add_btn.pack(side="right")
    
    def _create_team_table(self):
        """Tạo bảng nhân viên"""
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.container,
            label_text="📋 Danh sách nhân viên"
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Header
        self._create_table_header()
    
    def _create_table_header(self):
        """Tạo header cho bảng"""
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2C3E50", height=40)
        header_frame.pack(fill="x", pady=(0, 2))
        header_frame.pack_propagate(False)
        
        headers = [
            ("Mã NV", 0.10),
            ("Họ và tên", 0.15),
            ("Email", 0.15),
            ("SĐT", 0.10),
            ("Chức vụ", 0.12),
            ("Lương", 0.10),
            ("Trạng thái", 0.10),
            ("Thao tác", 0.18)
        ]
        
        for text, width in headers:
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white"
            )
            label.place(relx=sum(h[1] for h in headers[:headers.index((text, width))]), 
                       rely=0.5, anchor="w", relwidth=width)
    
    def fetch_data(self):
        """Load danh sách nhân viên trong phòng"""
        print("🔄 [REFRESH] Button clicked - Starting fetch_data...")
        
        # Clear existing
        try:
            widgets_to_destroy = self.scrollable_frame.winfo_children()[1:]
            print(f"🗑️ Clearing {len(widgets_to_destroy)} existing widgets...")
            for widget in widgets_to_destroy:
                widget.destroy()
        except Exception as e:
            print(f"⚠️ Error clearing widgets: {e}")
        
        try:
            # Fetch team members - CHỈ LẤY NHÂN VIÊN THUỘC TEAM CỦA MANAGER
            print("📡 Calling employee_controller.get_all_employees_for_view()...")
            employees = self.employee_controller.get_all_employees_for_view()
            print(f"✅ Received {len(employees)} employees from controller")
            
            if not employees:
                print("⚠️ No employees found - showing 'no data' message")
                no_data = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="Chưa có nhân viên trong phòng",
                    font=("Arial", 14),
                    text_color="gray"
                )
                no_data.pack(pady=50)
                return
            
            print(f"📋 Displaying {len(employees)} employee rows...")
            # Display rows
            for idx, emp in enumerate(employees):
                print(f"  Row {idx+1}: ID={emp.get('id')}, Name={emp.get('first_name')} {emp.get('last_name')}")
                self._create_employee_row(emp, idx)
            
            print(f"✅ [REFRESH] Successfully displayed {len(employees)} employees!")
            
        except Exception as e:
            print(f"❌ [ERROR] Lỗi khi load dữ liệu: {e}")
            import traceback
            traceback.print_exc()
            
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"❌ Lỗi: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            )
            error_label.pack(pady=50)
    
    def _create_employee_row(self, employee, index):
        """Tạo dòng nhân viên"""
        # Màu nền xen kẽ với độ tương phản cao hơn
        row_color = "#34495E" if index % 2 == 0 else "#2C3E50"
        
        row_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=row_color,
            height=45,
            corner_radius=0
        )
        row_frame.pack(fill="x", pady=1)
        row_frame.pack_propagate(False)
        
        # Format salary
        salary = employee.get('salary', 0) or 0
        salary_formatted = f"{salary:,.0f}" if salary else "0"
        
        # Data
        data = [
            (str(employee.get('employee_id', '') or employee.get('id', '')), 0.10),
            (f"{employee.get('first_name', '')} {employee.get('last_name', '')}", 0.15),
            (employee.get('email', ''), 0.15),
            (employee.get('phone', '') or employee.get('phone_number', ''), 0.10),
            (employee.get('position_title', ''), 0.12),
            (salary_formatted, 0.10),
            (employee.get('status', '') or employee.get('employment_status', ''), 0.10)
        ]
        
        x_pos = 0
        for text, width in data:
            label = ctk.CTkLabel(
                row_frame,
                text=str(text),
                font=("Arial", 12),
                text_color="#FFFFFF",  # Màu trắng để dễ đọc
                anchor="w"
            )
            label.place(relx=x_pos, rely=0.5, anchor="w", relwidth=width)
            x_pos += width
        
        # Actions
        self._create_action_buttons(row_frame, employee, x_pos)
    
    def _create_action_buttons(self, parent, employee, x_pos):
        """Tạo action buttons"""
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.place(relx=x_pos, rely=0.5, anchor="w", relwidth=0.20)
        
        # View
        view_btn = ctk.CTkButton(
            actions_frame,
            text="👁",
            width=35,
            height=28,
            command=lambda e=employee: self.view_employee(e),
            fg_color="#3498DB",
            font=("Arial", 12)
        )
        view_btn.pack(side="left", padx=2)
        
        # Edit (if allowed)
        if self.employee_controller.can_edit_employee(
            self.auth_controller.current_user_data,
            employee
        ):
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="✏",
                width=35,
                height=28,
                command=lambda e=employee: self.edit_employee(e),
                fg_color="#F39C12",
                font=("Arial", 12)
            )
            edit_btn.pack(side="left", padx=2)
    
    def search_team(self):
        """Tìm kiếm nhân viên TRONG TEAM"""
        keyword = self.search_entry.get().strip()
        
        for widget in self.scrollable_frame.winfo_children()[1:]:
            widget.destroy()
        
        try:
            # Search ONLY within team members - không search toàn bộ công ty
            if keyword:
                # Lấy team members trước, rồi filter local
                all_team_members = self.employee_controller.get_all_employees_for_view()
                employees = [
                    emp for emp in all_team_members
                    if keyword.lower() in emp.get('first_name', '').lower()
                    or keyword.lower() in emp.get('last_name', '').lower()
                    or keyword.lower() in emp.get('email', '').lower()
                ]
            else:
                # Nếu không có keyword, load lại team members
                employees = self.employee_controller.get_all_employees_for_view()
            
            if not employees:
                no_data = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"Không tìm thấy: '{keyword}'",
                    font=("Arial", 14),
                    text_color="gray"
                )
                no_data.pack(pady=50)
                return
            
            for idx, emp in enumerate(employees):
                self._create_employee_row(emp, idx)
        except Exception as e:
            print(f"Lỗi khi tìm kiếm: {e}")
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Lỗi: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            )
            error_label.pack(pady=50)
    
    def add_employee(self):
        """Thêm nhân viên mới - Mở form dialog"""
        EmployeeFormDialog(
            parent=self.container,
            employee_controller=self.employee_controller,
            auth_controller=self.auth_controller,
            mode="add",
            on_success=self.fetch_data  # Callback để refresh data sau khi thêm
        )
    
    def view_employee(self, employee):
        """Xem chi tiết nhân viên"""
        print(f"\n🔍 view_employee called with data:")
        print(f"   Employee dict: {employee}")
        print(f"   Keys: {list(employee.keys()) if employee else 'None'}\n")
        
        EmployeeFormDialog(
            parent=self.container,
            employee_controller=self.employee_controller,
            auth_controller=self.auth_controller,
            mode="view",
            employee_data=employee
        )
    
    def edit_employee(self, employee):
        """Sửa thông tin nhân viên"""
        EmployeeFormDialog(
            parent=self.container,
            employee_controller=self.employee_controller,
            auth_controller=self.auth_controller,
            mode="edit",
            employee_data=employee,
            on_success=self.fetch_data  # Callback để refresh data sau khi sửa
        )
