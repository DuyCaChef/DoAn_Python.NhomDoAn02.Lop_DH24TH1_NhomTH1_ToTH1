"""
Employee Management Tab - Director
Tab quản lý nhân viên cho Director (xem tất cả nhân viên)
"""
import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from app.views.components.tabs.base_tab import BaseTab
from app.controllers.employee_controller import EmployeeController


class EmployeeManagementTab(BaseTab):
    """Tab quản lý toàn bộ nhân viên - chỉ dành cho Director"""
    
    def __init__(self, parent, auth_controller):
        # Gọi super().__init__() để set parent và auth_controller
        super().__init__(parent, auth_controller)
        
        # Tạo employee_controller SAU KHI đã có auth_controller
        from app.controllers.employee_controller import EmployeeController
        self.employee_controller = EmployeeController(auth_controller)
        
        # Bây giờ mới gọi setup_ui()
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện tab quản lý nhân viên"""
        # Search và Action bar
        self._create_search_and_action_bar()
        
        # Table hiển thị danh sách nhân viên
        self._create_employee_table()
        
        # Load data
        self.fetch_data()
    
    def _create_search_and_action_bar(self):
        """Tạo thanh tìm kiếm và các nút action"""
        action_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        # Left: Search
        search_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True)
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Tìm kiếm:",
            font=ctk.CTkFont(size=13)
        )
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Nhập mã NV, tên, email, SĐT...",
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_employees())
        
        search_btn = self.create_button(
            search_frame,
            text="Tìm kiếm",
            command=self.search_employees,
            fg_color="#3498DB",
            hover_color="#2980B9"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = self.create_button(
            search_frame,
            text="🔄 Làm mới",
            command=self.fetch_data,
            fg_color="#95A5A6",
            hover_color="#7F8C8D"
        )
        refresh_btn.pack(side="left")
        
        # Right: Add button
        add_btn = self.create_button(
            action_frame,
            text="➕ Thêm nhân viên",
            command=self.add_employee,
            fg_color="#27AE60",
            hover_color="#229954"
        )
        add_btn.pack(side="right")
    
    def _create_employee_table(self):
        """Tạo bảng hiển thị danh sách nhân viên"""
        # Table container với scrollbar
        table_container = ctk.CTkFrame(self.container)
        table_container.pack(fill="both", expand=True)
        
        # Scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            table_container,
            label_text="📋 Danh sách nhân viên",
            label_font=ctk.CTkFont(size=15, weight="bold")
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Table header
        self._create_table_header()
    
    def _create_table_header(self):
        """Tạo header cho bảng"""
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2C3E50", height=40)
        header_frame.pack(fill="x", pady=(0, 2))
        header_frame.pack_propagate(False)
        
        headers = [
            ("Mã NV", 0.08),
            ("Họ và tên", 0.15),
            ("Email", 0.15),
            ("SĐT", 0.10),
            ("Phòng ban", 0.12),
            ("Chức vụ", 0.12),
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
        """Lấy và hiển thị dữ liệu nhân viên"""
        # Clear existing rows
        for widget in self.scrollable_frame.winfo_children()[1:]:  # Skip header
            widget.destroy()
        
        try:
            # Fetch employees - không cần truyền user_data
            employees = self.employee_controller.get_all_employees_for_view()
            
            if not employees:
                no_data_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="Không có dữ liệu nhân viên",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                no_data_label.pack(pady=50)
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
        """Tạo một dòng dữ liệu nhân viên"""
        # Màu nền xen kẽ với độ tương phản cao hơn
        row_color = "#34495E" if index % 2 == 0 else "#2C3E50"
        
        row_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=row_color,
            height=50,
            corner_radius=0
        )
        row_frame.pack(fill="x", pady=1)
        row_frame.pack_propagate(False)
        
        # Data cells
        data = [
            (str(employee.get('employee_id', '')), 0.08),
            (f"{employee.get('first_name', '')} {employee.get('last_name', '')}", 0.15),
            (employee.get('email', ''), 0.15),
            (employee.get('phone', '') or employee.get('phone_number', ''), 0.10),
            (employee.get('department_name', ''), 0.12),
            (employee.get('role_name', ''), 0.12),
            (employee.get('employment_status', '') or employee.get('status', ''), 0.10)
        ]
        
        x_pos = 0
        for text, width in data:
            # Màu chữ sáng hơn để dễ đọc
            text_color = "#FFFFFF"  # Mặc định màu trắng
            
            # Màu đặc biệt cho trạng thái
            if "Đang làm việc" in str(text):
                text_color = "#2ECC71"  # Xanh lá sáng
            elif "Đã nghỉ việc" in str(text):
                text_color = "#E74C3C"  # Đỏ sáng
            elif "Thử việc" in str(text):
                text_color = "#F39C12"  # Cam sáng
            
            label = ctk.CTkLabel(
                row_frame,
                text=str(text),
                font=ctk.CTkFont(size=12),
                text_color=text_color,
                anchor="w"
            )
            label.place(relx=x_pos, rely=0.5, anchor="w", relwidth=width)
            x_pos += width
        
        # Action buttons
        self._create_action_buttons(row_frame, employee, x_pos)
    
    def _create_action_buttons(self, parent, employee, x_pos):
        """Tạo các nút thao tác cho mỗi dòng"""
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.place(relx=x_pos, rely=0.5, anchor="w", relwidth=0.18)
        
        # Button Xem
        view_btn = ctk.CTkButton(
            actions_frame,
            text="👁",
            width=35,
            height=28,
            command=lambda e=employee: self.view_employee(e),
            fg_color="#3498DB",
            hover_color="#2980B9",
            font=ctk.CTkFont(size=12)
        )
        view_btn.pack(side="left", padx=2)
        
        # Button Sửa (chỉ nếu có quyền)
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
                hover_color="#E67E22",
                font=ctk.CTkFont(size=12)
            )
            edit_btn.pack(side="left", padx=2)
        
        # Button Xóa (chỉ nếu có quyền)
        if self.employee_controller.can_delete_employee(
            self.auth_controller.current_user_data,
            employee
        ):
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="🗑",
                width=35,
                height=28,
                command=lambda e=employee: self.delete_employee(e),
                fg_color="#E74C3C",
                hover_color="#C0392B",
                font=ctk.CTkFont(size=12)
            )
            delete_btn.pack(side="left", padx=2)
    
    def search_employees(self):
        """Tìm kiếm nhân viên theo keyword"""
        keyword = self.search_entry.get().strip()
        
        # Clear existing rows
        for widget in self.scrollable_frame.winfo_children()[1:]:
            widget.destroy()
        
        try:
            # Search - dùng search_by là 'all' để tìm kiếm tất cả fields
            employees = self.employee_controller.search_employees('first_name', keyword)
            
            if not employees:
                no_data_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"Không tìm thấy nhân viên với từ khóa: '{keyword}'",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                no_data_label.pack(pady=50)
                return
            
            # Display results
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
        """Mở form thêm nhân viên mới"""
        # TODO: Implement EmployeeForm
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
    
    def view_employee(self, employee):
        """Xem chi tiết nhân viên"""
        # TODO: Implement EmployeeForm
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
    
    def edit_employee(self, employee):
        """Sửa thông tin nhân viên"""
        # TODO: Implement EmployeeForm
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
    
    def delete_employee(self, employee):
        """Xóa nhân viên"""
        result = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa nhân viên:\n{employee.get('first_name')} {employee.get('last_name')}?",
            parent=self.container
        )
        
        if result:
            try:
                # Lấy employee_id từ employee dict
                emp_id = employee.get('id') or employee.get('employee_id')
                
                # Gọi controller để xóa
                message = self.employee_controller.delete_employee(emp_id)
                
                messagebox.showinfo("Thành công", message, parent=self.container)
                self.fetch_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa nhân viên: {str(e)}", parent=self.container)
