"""
Main Window - Refactored với Component-based Architecture
Cửa sổ chính của ứng dụng với giao diện động theo vai trò
"""
import customtkinter as ctk
from tkinter import messagebox

# Import components
from app.views.components.header import HeaderComponent
from app.views.components.tabs.director.employee_management_tab import EmployeeManagementTab
from app.views.components.tabs.director.account_management_tab import AccountManagementTab
from app.views.components.tabs.director.system_data_tab import SystemDataTab
from app.views.components.tabs.manager.team_management_tab import TeamManagementTab
from app.views.components.tabs.manager.approval_tab import ApprovalTab
from app.views.components.tabs.employee.profile_tab import ProfileTab
from app.views.components.tabs.employee.leave_request_tab import LeaveRequestTab


class MainWindow(ctk.CTk):
    """
    Cửa sổ chính của ứng dụng - Hỗ trợ giao diện động theo vai trò (Role-based UI)
    
    Architecture: Component-based
    - Header component: Hiển thị thông tin user và action buttons
    - Tab components: Mỗi tab là 1 component độc lập
    """
    
    def __init__(self, auth_controller, on_logout_callback=None):
        super().__init__()
        
        # Lưu auth controller và logout callback
        self.auth_controller = auth_controller
        self.on_logout_callback = on_logout_callback
        
        # Cấu hình cửa sổ - FULLSCREEN
        self.title("Hệ thống quản lý nhân sự")
        
        # Set fullscreen
        self.attributes('-fullscreen', True)
        
        # Thêm phím ESC để thoát fullscreen (tùy chọn)
        self.bind('<Escape>', lambda e: self.attributes('-topmost', False))
        self.bind('<F11>', lambda e: self.attributes('-fullscreen', True))
        
        # Tạo Header Component
        self.header = HeaderComponent(
            self,
            self.auth_controller,
            on_logout_callback=self.logout
        )
        
        # Tạo TabView chính
        self.tab_view = ctk.CTkTabview(self, width=1260, height=720)
        self.tab_view.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        
        # Setup UI theo role
        self.setup_ui_for_role()
        
        # Update header với thông tin user
        self.header.update_user_info()
        
        # Không cần center window vì đã fullscreen
        # self._center_window()
    
    def setup_ui_for_role(self):
        """Thiết lập giao diện dựa trên vai trò người dùng"""
        if not self.auth_controller or not self.auth_controller.current_user_data:
            messagebox.showerror("Lỗi", "Không thể xác định vai trò người dùng!")
            self.logout()
            return
        
        role = self.auth_controller.current_user_data.get('role_name', 'Employee')
        
        # Clear existing tabs
        for tab_name in list(self.tab_view._tab_dict.keys()):
            self.tab_view.delete(tab_name)
        
        # Create tabs theo role
        if role == 'Director':
            self._create_director_tabs()
        elif role == 'Manager':
            self._create_manager_tabs()
        elif role == 'Employee':
            self._create_employee_tabs()
        else:
            messagebox.showerror("Lỗi", f"Vai trò không xác định: {role}")
            self.logout()
    
    def _create_director_tabs(self):
        """Tạo tabs cho Director (Giám đốc)"""
        # Tab 1: Quản lý nhân viên
        self.tab_view.add("Quản lý nhân viên")
        employee_tab = EmployeeManagementTab(
            self.tab_view.tab("Quản lý nhân viên"),
            self.auth_controller
        )
        
        # Tab 2: Quản lý tài khoản
        self.tab_view.add("Quản lý tài khoản")
        account_tab = AccountManagementTab(
            self.tab_view.tab("Quản lý tài khoản"),
            self.auth_controller
        )
        
        # Tab 3: Dữ liệu hệ thống
        self.tab_view.add("Dữ liệu hệ thống")
        system_tab = SystemDataTab(
            self.tab_view.tab("Dữ liệu hệ thống"),
            self.auth_controller
        )
        
        # Set default tab
        self.tab_view.set("Quản lý nhân viên")
    
    def _create_manager_tabs(self):
        """Tạo tabs cho Manager (Trưởng phòng)"""
        # Tab 1: Quản lý nhân viên phòng
        self.tab_view.add("Quản lý nhân viên")
        team_tab = TeamManagementTab(
            self.tab_view.tab("Quản lý nhân viên"),
            self.auth_controller
        )
        
        # Tab 2: Duyệt nghỉ phép
        self.tab_view.add("Duyệt nghỉ phép")
        approval_tab = ApprovalTab(
            self.tab_view.tab("Duyệt nghỉ phép"),
            self.auth_controller
        )
        
        # Set default tab
        self.tab_view.set("Quản lý nhân viên")
    
    def _create_employee_tabs(self):
        """Tạo tabs cho Employee (Nhân viên)"""
        # Tab 1: Thông tin cá nhân
        self.tab_view.add("Thông tin cá nhân")
        profile_tab = ProfileTab(
            self.tab_view.tab("Thông tin cá nhân"),
            self.auth_controller
        )
        
        # Tab 2: Yêu cầu nghỉ phép
        self.tab_view.add("Yêu cầu nghỉ phép")
        leave_tab = LeaveRequestTab(
            self.tab_view.tab("Yêu cầu nghỉ phép"),
            self.auth_controller
        )
        
        # Set default tab
        self.tab_view.set("Thông tin cá nhân")
    
    def logout(self):
        """Đăng xuất khỏi hệ thống và THOÁT ỨNG DỤNG"""
        # Xác nhận trước khi thoát
        confirm = messagebox.askyesno(
            "Xác nhận đăng xuất",
            "Bạn có chắc chắn muốn đăng xuất?\nỨng dụng sẽ được đóng.",
            parent=self
        )
        
        if not confirm:
            return  # User hủy, không làm gì
        
        # Đăng xuất
        if self.auth_controller:
            self.auth_controller.logout()
        
        # Destroy main window
        self.destroy()
        
        # Thoát ứng dụng hoàn toàn
        import sys
        sys.exit(0)
    
    def _center_window(self):
        """Hiển thị cửa sổ ở giữa màn hình"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
