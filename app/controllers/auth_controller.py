from typing import Any, Dict
from app.database.auth_queries import AuthQueries 
import hashlib

class AuthController:
    """
    Bộ não xử lý logic xác thực người dùng và phân quyền.
    """
    def __init__(self):
        self.db = AuthQueries() # Khởi tạo class AuthQueries
        
        # Các vai trò được phép đăng nhập (dựa theo yêu cầu của bạn)
        self.ALLOWED_ROLES = ['Admin', 'HR Manager', 'Team Lead', 'Manager']

    def login(self, username, password) -> bool:
        """
        Kiểm tra thông tin đăng nhập và lưu quyền của user.
        """
        if not username or not password:
            raise ValueError("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
        user_data = self.db.get_user_by_username(username)
        # Bước 1: Xác thực mật khẩu bằng MySQL authentication
        if not user_data:
            raise ValueError("Tên đăng nhập hoặc mật khẩu không đúng!")
        # Bước 2: Kiểm tra mật khẩu
        stored_hash = user_data.get('password_hash')
        if not self.db.check_password(password, stored_hash):
            raise ValueError("Tên đăng nhập hoặc mật khẩu không đúng!")
        
            
        # Bước 3: Kiểm tra vai trò
        role_name = user_data.get('role_name')
        if role_name not in self.ALLOWED_ROLES:
            raise ValueError(f"Vai trò '{role_name}' không có quyền đăng nhập vào hệ thống này.")
        
        # Bước 4: Lưu thông tin user và lấy quyền
        print(f"Người dùng '{username}' (Vai trò: {role_name}) đã đăng nhập.")
        self.current_user_data = user_data
        return True
    
    def get_current_user(self):
        """Lấy thông tin user hiện tại"""
        return self.current_user
    
    def get_current_user_employee_id(self) -> int:
        """Trả về ID nhân viên của người đang đăng nhập"""
        if self.current_user_data:
            return self.current_user_data.get('employee_id')    
        return None
    
    def get_current_user_role(self) -> str:
        """Trả về vai trò của người đang đăng nhập"""
        if self.current_user_data:
            return self.current_user_data.get('role_name')
        return None
    
    def can_view_employees(self):
        """Kiểm tra quyền xem nhân viên"""
        return self.permissions.get('can_view_employees', False)
    
    def can_add_employees(self):
        """Kiểm tra quyền thêm nhân viên"""
        return self.permissions.get('can_add_employees', False)
    
    def can_edit_employees(self):
        """Kiểm tra quyền sửa nhân viên"""
        return self.permissions.get('can_edit_employees', False)
    
    def can_delete_employees(self):
        """Kiểm tra quyền xóa nhân viên"""
        return self.permissions.get('can_delete_employees', False)
    
    def can_manage_users(self):
        """Kiểm tra quyền quản lý tài khoản"""
        return self.permissions.get('can_manage_users', False)
    
    def can_view_reports(self):
        """Kiểm tra quyền xem báo cáo"""
        return self.permissions.get('can_view_reports', False)
    
    def logout(self):
        """Đăng xuất - xóa thông tin user hiện tại"""
        self.current_user = None
        self.permissions = {}
        print("Đã đăng xuất thành công.")