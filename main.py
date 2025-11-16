import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk 

# Import các View
from app.views.login_window import LoginWindow
from app.views.main_window import MainWindow 

# Import các Controller
from app.controllers.auth_controller import AuthController
from app.controllers.employee_controller import EmployeeController

# Import hàm kiểm tra DB
from app.database.connection import create_connection

def check_database_connection():
    """Kiểm tra kết nối DB trước khi chạy app."""
    print("Đang kiểm tra kết nối database...")
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            print("✅ Kết nối database thành công.")
            conn.close()
            return True
    except Exception as e:
        print(f"❌ LỖI KẾT NỐI: {e}")
        messagebox.showerror("Lỗi Kết nối", 
                             "Không thể kết nối đến Database.\nVui lòng kiểm tra file .env và đảm bảo MySQL đang chạy.")
        return False
    return False

class AppManager:
    """
    Quản lý luồng chạy của toàn bộ ứng dụng.
    """
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        if not check_database_connection():
            root = ctk.CTk()
            root.withdraw(); root.destroy()
            return
            
        self.auth_controller = AuthController()
        
        self.main_app_window = None
        self.launch_login()

    def launch_login(self):
        login_app = LoginWindow(
            auth_controller=self.auth_controller,
            on_login_success=self.launch_main_app 
        )
        login_app.mainloop()

    def launch_main_app(self):
        """Khởi chạy cửa sổ chính sau khi login thành công"""
        if self.main_app_window is None or not self.main_app_window.winfo_exists():
            # Tạo cửa sổ chính với auth_controller và logout callback
            # MainWindow mới tự động setup UI dựa trên role trong auth_controller
            self.main_app_window = MainWindow(
                auth_controller=self.auth_controller,
                on_logout_callback=self.on_logout_and_relaunch_login
            )
            
            self.main_app_window.mainloop()
        else:
            self.main_app_window.focus()
    
    def on_logout_and_relaunch_login(self):
        """Callback sau khi logout - hiển thị lại màn hình login"""
        # Delay một chút để main window destroy hoàn toàn
        import time
        time.sleep(0.1)
        
        # Mở lại login window
        self.launch_login()

if __name__ == "__main__":
    AppManager()