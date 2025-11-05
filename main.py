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
        self.employee_controller = EmployeeController(
            auth_controller=self.auth_controller
        )
        
        self.main_app_window = None
        self.launch_login()

    def launch_login(self):
        login_app = LoginWindow(
            auth_controller=self.auth_controller,
            on_login_success=self.launch_main_app 
        )
        login_app.mainloop()

    def launch_main_app(self):
        role = self.auth_controller.get_current_user_role()
        
        if self.main_app_window is None or not self.main_app_window.winfo_exists():
            self.main_app_window = MainWindow(
                controller=self.employee_controller 
            )
            # (Bạn cần tự triển khai hàm này trong MainWindow)
            # self.main_app_window.setup_ui_for_role(role) 
            
            self.main_app_window.mainloop()
        else:
            self.main_app_window.focus()

if __name__ == "__main__":
    AppManager()