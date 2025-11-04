from app.database.auth_queries import AuthQueries # Import class mới
import hashlib

class AuthController:
    """
    Bộ não xử lý logic xác thực người dùng và phân quyền.
    """
    def __init__(self):
        self.db = AuthQueries() # Khởi tạo class AuthQueries
        
        # Các vai trò được phép đăng nhập
        self.ALLOWED_ROLES = ['Admin', 'Manager', 'User'] 
        
        # Lưu thông tin user hiện tại
        self.current_user = None
        self.permissions = {}

    def login(self, username, password):
        """
        Kiểm tra thông tin đăng nhập và lưu quyền của user.
        """
        if not username or not password:
            raise ValueError("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
        
        # Bước 1: Xác thực mật khẩu bằng MySQL authentication
        if not self.db.attempt_login_connection(username, password):
            raise ValueError("Tên đăng nhập hoặc mật khẩu không đúng!")
            
        # Bước 2: Lấy thông tin user và role
        user_role_data = self.db.get_app_role(username)
        
        if not user_role_data:
            raise ValueError(f"User '{username}' không được cấp quyền trong ứng dụng.")
            
        # Bước 3: Kiểm tra vai trò
        role_name = user_role_data.get('role_name')
        if role_name not in self.ALLOWED_ROLES:
            raise ValueError(f"Vai trò '{role_name}' không có quyền đăng nhập vào hệ thống này.")
        
        # Bước 4: Lưu thông tin user và lấy quyền
        self.current_user = user_role_data
        self.permissions = self.db.get_user_permissions(username)
            
        # Bước 5: Đăng nhập thành công
        print(f"Người dùng '{username}' (Vai trò: {role_name}) đã đăng nhập thành công.")
        print(f"Quyền: {self.permissions}")
        return True
    
    def get_current_user(self):
        """Lấy thông tin user hiện tại"""
        return self.current_user
    
    def get_current_role(self):
        """Lấy role của user hiện tại"""
        if self.current_user:
            return self.current_user.get('role_name')
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