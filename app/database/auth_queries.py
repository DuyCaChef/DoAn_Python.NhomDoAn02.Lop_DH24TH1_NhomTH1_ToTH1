from app.database.connection import create_connection 
from typing import Dict, Any, Optional
import hashlib
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
class AuthQueries:
    def __init__(self):
        # Lấy thông tin host/db từ file .env
        self.db_host = os.getenv("DB_HOST")
        self.db_name = os.getenv("DB_NAME")
    def attempt_login_connection(self, username, password) -> bool:
        """
        Bước A: Thử kết nối vào DB với tư cách người dùng.
        """
        conn = None
        try:
            conn = mysql.connector.connect(
                host=self.db_host,
                user=username,
                password=password,
                database=self.db_name
            )
            return True
        except mysql.connector.Error as e:
            if e.errno == 1045: 
                print("AuthQueries: Sai mật khẩu khi thử kết nối.")
            else:
                print(f"Lỗi kết nối AuthQueries: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()
    
        
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin user (gồm password_hash) VÀ tên vai trò (role_name) 
        VÀ thông tin nhân viên đầy đủ từ bảng employees.
        """
        conn = None
        try:
            conn = create_connection() # Dùng kết nối HỆ THỐNG
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    u.*, 
                    r.name as role_name,
                    e.id as employee_id,
                    e.first_name,
                    e.last_name,
                    e.email,
                    e.phone_number as phone,
                    e.hire_date,
                    e.status as employment_status,
                    e.department_id,
                    d.name as department_name,
                    m.first_name as manager_first_name,
                    m.last_name as manager_last_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                LEFT JOIN employees e ON u.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN employees m ON e.manager_id = m.id
                WHERE u.username = %s AND u.is_active = 1
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Lỗi khi lấy user: {e}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def check_password(self, plain_password: str, stored_hash: str) -> bool:
        """
        Kiểm tra mật khẩu (dùng SHA-256).
        """
        if not plain_password or not stored_hash:
            return False
        
        try:
            password_bytes = plain_password.encode('utf-8')
            hashed_input = hashlib.sha256(password_bytes).hexdigest()
            print(f"Hashed input: {hashed_input}, Stored hash: {stored_hash}")
            return hashed_input == stored_hash
        except Exception as e:
            print(f"Lỗi khi băm mật khẩu: {e}")
            return False
    
    def hash_password(self, plain_password: str) -> str:
        """
        Băm mật khẩu bằng SHA-256.
        """
        password_bytes = plain_password.encode('utf-8')
        return hashlib.sha256(password_bytes).hexdigest()
    
    def update_user_password(self, user_id: int, new_password_hash: str) -> bool:
        """
        Cập nhật mật khẩu cho user trong database.
        """
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor()
            query = """
                UPDATE users 
                SET password_hash = %s 
                WHERE id = %s
            """
            cursor.execute(query, (new_password_hash, user_id))
            conn.commit()
            
            affected = cursor.rowcount
            print(f"✅ Đã cập nhật mật khẩu cho user ID {user_id}")
            return affected > 0
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật mật khẩu: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()