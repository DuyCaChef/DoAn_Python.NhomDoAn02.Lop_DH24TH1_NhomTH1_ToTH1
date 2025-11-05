from typing import Any, Dict
from app.database.auth_queries import AuthQueries 
import hashlib

class AuthController:
    """
    Bộ não xử lý logic xác thực người dùng và phân quyền.
    """
    def __init__(self):
        self.db = AuthQueries() # Khởi tạo class AuthQueries
        
        # Các vai trò được phép đăng nhập
        self.ALLOWED_ROLES = ['Admin', 'Manager', 'Employee'] 
        self.current_user_data: Dict[str, Any] = None

    def login(self, username, password) -> bool:
        """
        Kiểm tra thông tin đăng nhập bằng cách SELECT và So sánh Hash.
        """
        if not username or not password:
            raise ValueError("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
        
        user_data = self.db.get_user_by_username(username)
        
        if not user_data:
            raise ValueError("Tên đăng nhập hoặc mật khẩu không đúng!")
            
        stored_hash = user_data.get('password_hash')
        if not self.db.check_password(password, stored_hash): 
            raise ValueError("Tên đăng nhập hoặc mật khẩu không đúng!")
            
        role_name = user_data.get('role_name')
        if role_name not in self.ALLOWED_ROLES:
            raise ValueError(f"Vai trò '{role_name}' không có quyền đăng nhập.")
            
        print(f"Người dùng '{username}' (Vai trò: {role_name}) đã đăng nhập.")
        self.current_user_data = user_data
        return True
    
    def get_current_user_role(self) -> str:
        """Trả về vai trò của người đang đăng nhập"""
        if self.current_user_data:
            return self.current_user_data.get('role_name')
        return None
    
    def get_current_user_employee_id(self) -> int:
        """Trả về ID nhân viên của người đang đăng nhập"""
        if self.current_user_data:
            return self.current_user_data.get('employee_id')    
        return None
        
    # --- CÁC HÀM PHÂN QUYỀN MỚI ---
    
    def get_current_role(self) -> str:
        """Hàm rút gọn (tên khác)"""
        return self.get_current_user_role()

    def can_add_employees(self) -> bool:
        """Kiểm tra xem user có quyền Thêm NV không"""
        role = self.get_current_role()
        return role in ['Admin', 'Manager']

    def can_edit_employees(self) -> bool:
        """Kiểm tra xem user có quyền Sửa NV không"""
        role = self.get_current_role()
        # Employee chỉ được sửa mình, logic đó sẽ
        # được xử lý ở EmployeeController.
        # Ở đây, chúng ta cho phép nút bấm được bật.
        return role in ['Admin', 'Manager', 'Employee']

    def can_delete_employees(self) -> bool:
        """Kiểm tra xem user có quyền Xóa NV không"""
        role = self.get_current_role()
        return role in ['Admin'] # Chỉ Admin được xóa
    
    def can_view_employees(self) -> bool:
        """Kiểm tra quyền xem nhân viên"""
        role = self.get_current_role()
        return role in ['Admin', 'Manager', 'Employee']
    
    def can_manage_users(self) -> bool:
        """Kiểm tra quyền quản lý tài khoản"""
        role = self.get_current_role()
        return role in ['Admin']
    
    def can_view_reports(self) -> bool:
        """Kiểm tra quyền xem báo cáo"""
        role = self.get_current_role()
        return role in ['Admin', 'Manager']
    
    def logout(self):
        """Đăng xuất - xóa thông tin user hiện tại"""
        self.current_user_data = None
        print("Đã đăng xuất thành công.")