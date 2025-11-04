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
            root.withdraw() 
            root.destroy()
            return
            
        self.auth_controller = AuthController()
        self.employee_controller = EmployeeController()
        self.main_app_window = None
        
        self.launch_login()

    def launch_login(self):
        """Mở cửa sổ đăng nhập."""
        login_app = LoginWindow(
            auth_controller=self.auth_controller,
            on_login_success=self.launch_main_app 
        )
        login_app.mainloop()

    def launch_main_app(self):
        """Phân luồng user dựa trên role sau khi đăng nhập."""
        current_role = self.auth_controller.get_current_role()
        
        if current_role in ['Admin', 'Manager']:
            # Admin và Manager vào trang quản lý nhân viên
            if self.main_app_window is None or not self.main_app_window.winfo_exists():
                self.main_app_window = MainWindow(
                    controller=self.employee_controller,
                    auth_controller=self.auth_controller
                )
                self.main_app_window.mainloop()
            else:
                self.main_app_window.focus()
        
        elif current_role == 'User':
            # User vào trang riêng (sẽ phát triển sau)
            self.launch_user_window()
        
        else:
            messagebox.showerror("Lỗi phân quyền", 
                                 f"Vai trò '{current_role}' chưa được hỗ trợ.")
    
    def launch_user_window(self):
        """Mở cửa sổ dành cho User (chưa phát triển)."""
        # Tạm thời hiển thị thông báo
        messagebox.showinfo("Thông báo", 
                            "Trang dành cho User đang được phát triển.\n" + 
                            "Role: User sẽ có giao diện riêng trong phiên bản tiếp theo.")
        print("🚧 User window - Coming soon!")

if __name__ == "__main__":
    AppManager()