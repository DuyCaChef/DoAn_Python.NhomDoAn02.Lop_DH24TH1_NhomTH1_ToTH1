"""
Profile Tab - Employee
Tab xem và chỉnh sửa thông tin cá nhân
"""
import customtkinter as ctk
from tkinter import messagebox
from app.views.components.tabs.base_tab import BaseTab


class ProfileTab(BaseTab):
    """Tab thông tin cá nhân - Employee"""
    
    def setup_ui(self):
        """Thiết lập giao diện profile"""
        # Title
        title = self.create_section_label(self.container, "👤 Thông tin cá nhân")
        title.pack(pady=(0, 20))
        
        # Profile form
        self._create_profile_form()
        
        # Load data
        self.fetch_data()
    
    def _create_profile_form(self):
        """Tạo form thông tin cá nhân"""
        form_container = ctk.CTkScrollableFrame(self.container)
        form_container.pack(fill="both", expand=True)
        
        # Form content
        content_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Personal Info Section
        self.create_section_label(content_frame, "📝 Thông tin cơ bản").pack(anchor="w", pady=(0, 15))
        
        # Employee ID (readonly)
        id_label = ctk.CTkLabel(content_frame, text="Mã nhân viên:", anchor="w")
        id_label.pack(fill="x", pady=(0, 5))
        self.emp_id_entry = self.create_input_field(content_frame, "")
        self.emp_id_entry.configure(state="disabled")
        self.emp_id_entry.pack(fill="x", pady=(0, 15))
        
        # First Name
        fname_label = ctk.CTkLabel(content_frame, text="Tên:", anchor="w")
        fname_label.pack(fill="x", pady=(0, 5))
        self.first_name_entry = self.create_input_field(content_frame, "Nhập tên")
        self.first_name_entry.pack(fill="x", pady=(0, 15))
        
        # Last Name
        lname_label = ctk.CTkLabel(content_frame, text="Họ và tên đệm:", anchor="w")
        lname_label.pack(fill="x", pady=(0, 5))
        self.last_name_entry = self.create_input_field(content_frame, "Nhập họ và tên đệm")
        self.last_name_entry.pack(fill="x", pady=(0, 15))
        
        # Email (readonly)
        email_label = ctk.CTkLabel(content_frame, text="Email:", anchor="w")
        email_label.pack(fill="x", pady=(0, 5))
        self.email_entry = self.create_input_field(content_frame, "")
        self.email_entry.configure(state="disabled")
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        # Phone
        phone_label = ctk.CTkLabel(content_frame, text="Số điện thoại:", anchor="w")
        phone_label.pack(fill="x", pady=(0, 5))
        self.phone_entry = self.create_input_field(content_frame, "Nhập SĐT")
        self.phone_entry.pack(fill="x", pady=(0, 15))
        
        # Separator
        separator = ctk.CTkFrame(content_frame, height=2, fg_color="gray")
        separator.pack(fill="x", pady=20)
        
        # Work Info Section (readonly)
        self.create_section_label(content_frame, "💼 Thông tin công việc").pack(anchor="w", pady=(0, 15))
        
        # Department
        dept_label = ctk.CTkLabel(content_frame, text="Phòng ban:", anchor="w")
        dept_label.pack(fill="x", pady=(0, 5))
        self.dept_entry = self.create_input_field(content_frame, "")
        self.dept_entry.configure(state="disabled")
        self.dept_entry.pack(fill="x", pady=(0, 15))
        
        # Role
        role_label = ctk.CTkLabel(content_frame, text="Chức vụ:", anchor="w")
        role_label.pack(fill="x", pady=(0, 5))
        self.role_entry = self.create_input_field(content_frame, "")
        self.role_entry.configure(state="disabled")
        self.role_entry.pack(fill="x", pady=(0, 15))
        
        # Status
        status_label = ctk.CTkLabel(content_frame, text="Trạng thái:", anchor="w")
        status_label.pack(fill="x", pady=(0, 5))
        self.status_entry = self.create_input_field(content_frame, "")
        self.status_entry.configure(state="disabled")
        self.status_entry.pack(fill="x", pady=(0, 15))
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        save_btn = self.create_button(
            buttons_frame,
            "💾 Lưu thay đổi",
            self.save_profile,
            fg_color="#27AE60",
            hover_color="#229954"
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        reset_btn = self.create_button(
            buttons_frame,
            "↺ Khôi phục",
            self.fetch_data,
            fg_color="#95A5A6",
            hover_color="#7F8C8D"
        )
        reset_btn.pack(side="left")
    
    def fetch_data(self):
        """Load thông tin cá nhân"""
        if not self.auth_controller or not self.auth_controller.current_user_data:
            return
        
        user_data = self.auth_controller.current_user_data
        
        # Enable fields temporarily to update
        self.emp_id_entry.configure(state="normal")
        self.email_entry.configure(state="normal")
        self.dept_entry.configure(state="normal")
        self.role_entry.configure(state="normal")
        self.status_entry.configure(state="normal")
        
        # Clear existing values
        for entry in [self.emp_id_entry, self.first_name_entry, self.last_name_entry,
                     self.email_entry, self.phone_entry, self.dept_entry,
                     self.role_entry, self.status_entry]:
            entry.delete(0, 'end')
        
        # Fill data
        self.emp_id_entry.insert(0, str(user_data.get('employee_id', '')))
        self.first_name_entry.insert(0, user_data.get('first_name', ''))
        self.last_name_entry.insert(0, user_data.get('last_name', ''))
        self.email_entry.insert(0, user_data.get('email', ''))
        self.phone_entry.insert(0, user_data.get('phone', ''))
        self.dept_entry.insert(0, user_data.get('department_name', ''))
        self.role_entry.insert(0, user_data.get('role_name', ''))
        self.status_entry.insert(0, user_data.get('employment_status', ''))
        
        # Disable readonly fields
        self.emp_id_entry.configure(state="disabled")
        self.email_entry.configure(state="disabled")
        self.dept_entry.configure(state="disabled")
        self.role_entry.configure(state="disabled")
        self.status_entry.configure(state="disabled")
    
    def save_profile(self):
        """Lưu thay đổi profile"""
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not all([first_name, last_name, phone]):
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin!", parent=self.container)
            return
        
        # TODO: Implement với controller
        messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!", parent=self.container)
