# main.py

import tkinter as tk
from tkinter import messagebox
# Import các thành phần từ cấu trúc MVC của bạn
from app.views.main_window import MainWindow
from app.controllers.employee_controller import EmployeeController
from app.database.connection import create_connection

def check_database_connection():
    """Kiểm tra kết nối DB trước khi chạy app."""
    print("Đang kiểm tra kết nối database...")
    conn = create_connection()
    if conn and conn.is_connected():
        print("✅ Kết nối database thành công.")
        conn.close()
        return True
    else:
        print("❌ LỖI: Không thể kết nối đến database. Vui lòng kiểm tra file .env")
        return False

def main():
    """
    Điểm khởi đầu của ứng dụng.
    """
    # 1. Kiểm tra kết nối DB trước
    if not check_database_connection():
        # Hiển thị lỗi bằng một cửa sổ Tkinter đơn giản
        root = tk.Tk()
        root.withdraw() # Ẩn cửa sổ root chính
        messagebox.showerror("Lỗi Kết nối", 
                             "Không thể kết nối đến Database.\nVui lòng kiểm tra file .env và đảm bảo MySQL đang chạy.")
        root.destroy()
        return

    # 2. Khởi tạo Controller (Bộ não logic)
    # Giả sử bạn đã có file này
    try:
        employee_controller = EmployeeController()
    except NameError:
        print("Lỗi: Không tìm thấy 'EmployeeController'.")
        print("Hãy đảm bảo bạn đã tạo file 'app/controllers/employee_controller.py'.")
        # Sử dụng một controller giả để test giao diện
        class FakeController:
            pass
        employee_controller = FakeController()

    
    # 3. Khởi tạo View (Giao diện) và truyền controller vào
    app = MainWindow(controller=employee_controller)
    
    # 4. Chạy vòng lặp chính của Tkinter
    app.mainloop()

if __name__ == "__main__":
    main()

