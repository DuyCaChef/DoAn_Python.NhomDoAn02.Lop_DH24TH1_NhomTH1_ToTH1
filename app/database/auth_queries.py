from app.database.connection import create_connection # DÙNG KẾT NỐI HỆ THỐNG
from typing import Dict, Any, Optional
import mysql.connector
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

class AuthQueries:
    """
    Chứa các hàm truy vấn cho logic đăng nhập MỚI.
    """
    def __init__(self):
        # Lấy thông tin host/db từ file .env
        self.db_host = os.getenv("DB_HOST")
        self.db_name = os.getenv("DB_NAME")
    
    def verify_password(self, username: str, password: str) -> bool:
        """
        Xác thực username và password bằng cách so sánh password hash.
        """
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT password_hash, is_active
                FROM users
                WHERE username = %s
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            if not user:
                print(f"User '{username}' không tồn tại")
                return False
            
            if not user['is_active']:
                print(f"User '{username}' đã bị vô hiệu hóa")
                return False
            
            # So sánh password hash
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if password_hash == user['password_hash']:
                return True
            else:
                print(f"Sai mật khẩu cho user '{username}'")
                return False
                
        except Exception as e:
            print(f"Lỗi khi xác thực password: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def attempt_login_connection(self, username, password) -> bool:
        """
        Bước A: Thử kết nối vào DB với tư cách người dùng.
        Đây là cách duy nhất để xác thực caching_sha2_password.
        """
        conn = None
        try:
            conn = mysql.connector.connect(
                host=self.db_host,
                user=username,
                password=password,
                database=self.db_name
            )
            # Nếu kết nối thành công (không ném Exception)
            return True
        except mysql.connector.Error as e:
            # Lỗi 1045 là lỗi sai username/password
            if e.errno == 1045: 
                print("AuthQueries: Sai mật khẩu khi thử kết nối.")
            else:
                print(f"Lỗi kết nối AuthQueries: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()

    def get_app_role(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Bước B: Dùng kết nối HỆ THỐNG để lấy vai trò của user
        từ bảng 'users' của ứng dụng.
        """
        conn = None
        try:
            conn = create_connection() # Dùng kết nối admin (từ .env)
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT u.id, u.username, u.employee_id, r.id as role_id, r.name as role_name 
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.username = %s AND u.is_active = 1
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Lỗi khi lấy vai trò user: {e}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
    
    def get_user_permissions(self, username: str) -> Dict[str, bool]:
        """
        Lấy danh sách quyền cụ thể của user.
        
        Phân quyền:
        - Admin: Có tất cả quyền
        - Manager: Có thể xem, thêm, sửa, XÓA nhân viên và xem báo cáo (KHÔNG quản lý user/tài khoản)
        - User: Chỉ xem thông tin nhân viên (Read-only)
        
        Returns:
            Dict với các quyền:
            - can_view_employees: Xem danh sách nhân viên
            - can_add_employees: Thêm nhân viên mới
            - can_edit_employees: Sửa thông tin nhân viên
            - can_delete_employees: Xóa nhân viên
            - can_manage_users: Quản lý tài khoản user
            - can_view_reports: Xem báo cáo
        """
        user_info = self.get_app_role(username)
        if not user_info:
            return {
                'can_view_employees': False,
                'can_add_employees': False,
                'can_edit_employees': False,
                'can_delete_employees': False,
                'can_manage_users': False,
                'can_view_reports': False
            }
        
        role = user_info['role_name']
        
        # Phân quyền theo role
        permissions = {
            'Admin': {
                'can_view_employees': True,
                'can_add_employees': True,
                'can_edit_employees': True,
                'can_delete_employees': True,
                'can_manage_users': True,
                'can_view_reports': True
            },
            'Manager': {
                'can_view_employees': True,
                'can_add_employees': True,
                'can_edit_employees': True,
                'can_delete_employees': True,    # ✅ Manager CÓ THỂ XÓA user
                'can_manage_users': False,       # ❌ Manager KHÔNG quản lý tài khoản
                'can_view_reports': True
            },
            'User': {
                'can_view_employees': True,
                'can_add_employees': False,
                'can_edit_employees': False,
                'can_delete_employees': False,
                'can_manage_users': False,
                'can_view_reports': False
            }
        }
        
        return permissions.get(role, permissions['User'])