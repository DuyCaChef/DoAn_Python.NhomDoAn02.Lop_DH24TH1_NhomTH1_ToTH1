from app.database.connection import create_connection # DÙNG KẾT NỐI HỆ THỐNG
from typing import Dict, Any, Optional
import mysql.connector
import os
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
                SELECT u.username, r.name as role_name 
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