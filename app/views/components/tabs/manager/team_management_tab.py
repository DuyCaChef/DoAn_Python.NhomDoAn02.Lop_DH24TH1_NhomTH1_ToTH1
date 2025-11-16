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
        """Tạo header bảng"""
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2C3E50", height=40)
        header_frame.pack(fill="x", pady=(0, 2))
        header_frame.pack_propagate(False)
        
        headers = [
            ("Mã NV", 0.10),
            ("Họ và tên", 0.20),
            ("Email", 0.20),
            ("SĐT", 0.15),
            ("Chức vụ", 0.15),
            ("Thao tác", 0.20)
        ]
        
        x_pos = 0
        for text, width in headers:
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white"
            )
            label.place(relx=x_pos, rely=0.5, anchor="w", relwidth=width)
            x_pos += width
    
    def fetch_data(self):
        """Load danh sách nhân viên trong phòng"""
        # Clear existing
        for widget in self.scrollable_frame.winfo_children()[1:]:
            widget.destroy()
        
        try:
            # Fetch team members
            employees = self.employee_controller.get_all_employees_for_view()
            
            if not employees:
                no_data = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="Chưa có nhân viên trong phòng",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                no_data.pack(pady=50)
                return
            
            # Display rows
            for idx, emp in enumerate(employees):
                self._create_employee_row(emp, idx)
        except Exception as e:
            print(f"Lỗi khi load dữ liệu: {e}")
            error_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Lỗi: {str(e)}",
                font=ctk.CTkFont(size=14),
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
        
        # Data
        data = [
            (str(employee.get('employee_id', '') or employee.get('id', '')), 0.10),
            (f"{employee.get('first_name', '')} {employee.get('last_name', '')}", 0.20),
            (employee.get('email', ''), 0.20),
            (employee.get('phone', '') or employee.get('phone_number', ''), 0.15),
            (employee.get('role_name', ''), 0.15)
        ]
        
        x_pos = 0
        for text, width in data:
            label = ctk.CTkLabel(
                row_frame,
                text=str(text),
                font=ctk.CTkFont(size=12),
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
            font=ctk.CTkFont(size=12)
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
                font=ctk.CTkFont(size=12)
            )
            edit_btn.pack(side="left", padx=2)
    
    def search_team(self):
        """Tìm kiếm nhân viên"""
        keyword = self.search_entry.get().strip()
        
        for widget in self.scrollable_frame.winfo_children()[1:]:
            widget.destroy()
        
        try:
            employees = self.employee_controller.search_employees('first_name', keyword)
            
            if not employees:
                no_data = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"Không tìm thấy: '{keyword}'",
                    font=ctk.CTkFont(size=14),
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
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(pady=50)
    
    def add_employee(self):
        """Thêm nhân viên mới"""
        # TODO: Implement EmployeeForm
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
    
    def view_employee(self, employee):
        """Xem chi tiết"""
        # TODO: Implement EmployeeForm
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
    
    def edit_employee(self, employee):
        """Sửa thông tin"""
        # TODO: Implement EmployeeForm
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
