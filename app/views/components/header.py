"""
Header Component
Component hiển thị header với thông tin user và action buttons
"""
import customtkinter as ctk
from tkinter import messagebox
from app.views.change_password_dialog import ChangePasswordDialog


class HeaderComponent:
    """Component quản lý header của ứng dụng"""
    
    def __init__(self, parent, auth_controller, on_logout_callback):
        """
        Args:
            parent: Widget cha
            auth_controller: Controller xử lý authentication
            on_logout_callback: Callback khi logout
        """
        self.parent = parent
        self.auth_controller = auth_controller
        self.on_logout_callback = on_logout_callback
        
        self.header_frame = None
        self.welcome_label = None
        self.role_label = None
        
        self.create_header()
    
    def create_header(self):
        """Tạo header với thông tin user và các button actions"""
        # Header frame với gradient background
        self.header_frame = ctk.CTkFrame(
            self.parent, 
            height=80, 
            fg_color=("#3B8ED0", "#1F6AA5")
        )
        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.header_frame.pack_propagate(False)
        
        # Container cho nội dung header
        header_content = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # === LEFT SIDE: User Info ===
        self._create_user_info(header_content)
        
        # === RIGHT SIDE: Action Buttons ===
        self._create_action_buttons(header_content)
    
    def _create_user_info(self, parent):
        """Tạo phần hiển thị thông tin user bên trái"""
        left_frame = ctk.CTkFrame(parent, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        # Welcome label với tên user
        self.welcome_label = ctk.CTkLabel(
            left_frame,
            text="Xin chào, User!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.welcome_label.pack(anchor="w", pady=(5, 0))
        
        # Role label
        self.role_label = ctk.CTkLabel(
            left_frame,
            text="Nhân viên",
            font=ctk.CTkFont(size=14),
            text_color=("#E0E0E0", "#B0B0B0")
        )
        self.role_label.pack(anchor="w", pady=(2, 0))
    
    def _create_action_buttons(self, parent):
        """Tạo các action buttons bên phải"""
        right_frame = ctk.CTkFrame(parent, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        # Buttons container
        buttons_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        buttons_container.pack(anchor="e", expand=True)
        
        # Button Đổi mật khẩu
        change_password_button = ctk.CTkButton(
            buttons_container,
            text="🔐 Đổi mật khẩu",
            width=140,
            height=35,
            font=ctk.CTkFont(size=13),
            fg_color=("#4A90D9", "#2E5A8C"),
            hover_color=("#3A7FC9", "#1E4A7C"),
            command=self.open_change_password_dialog
        )
        change_password_button.pack(side="left", padx=(0, 10))
        
        # Button Đăng xuất
        logout_button = ctk.CTkButton(
            buttons_container,
            text="🚪 Đăng xuất",
            width=120,
            height=35,
            font=ctk.CTkFont(size=13),
            fg_color=("#E74C3C", "#C0392B"),
            hover_color=("#D63C2C", "#A0291B"),
            command=self.logout
        )
        logout_button.pack(side="left")
    
    def update_user_info(self):
        """Cập nhật thông tin user từ auth controller"""
        if self.auth_controller and hasattr(self.auth_controller, 'current_user_data'):
            user_data = self.auth_controller.current_user_data
            
            if user_data:
                # Lấy tên
                first_name = user_data.get('first_name', '')
                last_name = user_data.get('last_name', '')
                full_name = f"{first_name} {last_name}".strip()
                
                if not full_name:
                    full_name = user_data.get('username', 'User')
                
                # Cập nhật welcome label
                self.welcome_label.configure(text=f"Xin chào, {full_name}!")
                
                # Cập nhật role label với màu sắc
                role = user_data.get('role_name', 'Employee')
                role_text, role_color = self._get_role_display(role)
                self.role_label.configure(text=role_text, text_color=role_color)
    
    def _get_role_display(self, role):
        """Lấy text và màu hiển thị cho role"""
        role_config = {
            'Director': ("🏢 Giám đốc", "#FFD700"),
            'Manager': ("👔 Trưởng phòng", "#87CEEB"),
            'Employee': ("👤 Nhân viên", "#E0E0E0")
        }
        return role_config.get(role, ("👤 Nhân viên", "#E0E0E0"))
    
    def open_change_password_dialog(self):
        """Mở dialog đổi mật khẩu với implementation đầy đủ"""
        try:
            # Sử dụng dialog mới với đầy đủ tính năng
            dialog = ChangePasswordDialog(
                parent=self.parent,
                auth_controller=self.auth_controller,
                on_success=lambda: print("✅ Password changed successfully!")
            )
        except Exception as e:
            print(f"❌ Error opening change password dialog: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                "Lỗi",
                f"Không thể mở dialog đổi mật khẩu: {str(e)}",
                parent=self.parent
            )
    
    def logout(self):
        """Đăng xuất khỏi hệ thống"""
        result = messagebox.askyesno(
            "Xác nhận đăng xuất",
            "Bạn có chắc chắn muốn đăng xuất?",
            parent=self.parent
        )
        
        if result and self.on_logout_callback:
            self.on_logout_callback()
