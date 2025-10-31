from app.database.auth_queries import AuthQueries # Import class mới
import hashlib

class AuthController:
    """
    Bộ não xử lý logic xác thực người dùng (Logic MỚI).
    """
    def __init__(self):
        self.db = AuthQueries() # Khởi tạo class AuthQueries
        
        # Các vai trò được phép đăng nhập (dựa theo yêu cầu của bạn)
        self.ALLOWED_ROLES = ['Admin', 'HR Manager', 'Team Lead', 'Manager'] 

    def login(self, username, password):
        """
        Kiểm tra thông tin đăng nhập bằng logic 2 bước.
        """
        if not username or not password:
            raise ValueError("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
        
        # Bước 1: Xác thực mật khẩu
        # Thử kết nối vào DB với tư cách user đó
        if not self.db.attempt_login_connection(username, password):
            raise ValueError("Tên đăng nhập hoặc mật khẩu không đúng!")
            
        # Bước 2: Phân quyền
        # Mật khẩu đúng, giờ kiểm tra xem user đó có vai trò gì
        user_role_data = self.db.get_app_role(username)
        
        if not user_role_data:
            raise ValueError(f"User '{username}' không được cấp quyền trong ứng dụng.")
            
        # 3. KIỂM TRA VAI TRÒ
        role_name = user_role_data.get('role_name')
        if role_name not in self.ALLOWED_ROLES:
            raise ValueError(f"Vai trò '{role_name}' không có quyền đăng nhập vào hệ thống này.")
            
        # 4. Đăng nhập thành công
        print(f"Người dùng '{username}' (Vai trò: {role_name}) đã đăng nhập thành công.")
        return True