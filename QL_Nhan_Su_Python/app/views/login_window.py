import customtkinter as ctk
import os
from PIL import Image
import tkinter as tk
from tkinter import messagebox
from typing import Callable
# SỬA: Import controller
from app.controllers.auth_controller import AuthController

# TÊN CLASS PHẢI LÀ 'LoginWindow'
class LoginWindow(ctk.CTk):
    
    # SỬA: __init__ nhận controller và callback
    def __init__(self, auth_controller: AuthController, on_login_success: Callable[[], None]):
        super().__init__()
        
        self.controller = auth_controller
        self.on_login_success = on_login_success # Hàm sẽ gọi khi thành công

        # --- GIỮ NGUYÊN GIAO DIỆN CỦA BẠN ---
        self.geometry('930x478')
        self.resizable(0, 0)
        self.title('Đăng nhập hệ thống')
        self.config(bg='white')

        try:
            current_dir = os.path.dirname(__file__)
            # SỬA: Đường dẫn tương đối từ 'app/views' ra thư mục gốc rồi vào 'assets/images'
            image_path = os.path.join(current_dir, '..', '..', 'assets', 'images', 'bg_login.jpg')
            image_path = os.path.abspath(image_path)
            if os.path.exists(image_path):
                image = ctk.CTkImage(light_image=Image.open(image_path), size=(500, 500))
                imageLabel = ctk.CTkLabel(self, image=image, text='')
                imageLabel.image = image
                imageLabel.place(x=380, y=0)
            else:
                print(f"Không tìm thấy ảnh tại: {image_path}")
        except Exception as e:
            print(f"Không thể tải ảnh: {e}")

        headingLabel = ctk.CTkLabel(self, text='Đăng nhập hệ thống', font=('Goudy Old Style', 30, 'bold'), bg_color='white', text_color='#0A3871')
        headingLabel.place(x=65, y=50)

        usernameLabel = ctk.CTkLabel(self, text='Tên đăng nhập', font=('Goudy Old Style', 17, 'italic'), bg_color='white', text_color='#0A3871')
        usernameLabel.place(x=80, y=120)
        self.usernameEntry = ctk.CTkEntry(self, placeholder_text='Nhập tên đăng nhập', font=('Goudy Old Style', 15), bg_color='white', width=250)
        self.usernameEntry.place(x=80, y=150)

        passwordLabel = ctk.CTkLabel(self, text='Mật khẩu', font=('Goudy Old Style', 17, 'italic'), bg_color='white', text_color='#0A3871')
        passwordLabel.place(x=80, y=200)
        self.passwordEntry = ctk.CTkEntry(self, placeholder_text='Nhập mật khẩu', font=('Goudy Old Style', 15), bg_color='white', width=250, show='*')
        self.passwordEntry.place(x=80, y=230)

        
        self.show_var = tk.BooleanVar(value=False)
        
        def on_show_var_changed():
            self.passwordEntry.configure(show='' if self.show_var.get() else '*')
        show_checkbox = ctk.CTkCheckBox(self, text='Hiện mật khẩu', font=('Goudy Old Style', 13, 'italic'), command=on_show_var_changed, variable=self.show_var, fg_color="#2b82e4", bg_color='white', text_color='#0A3871', checkbox_height=18, checkbox_width=18)
        show_checkbox.place(x=80, y=265)

        loginButton = ctk.CTkButton(self, text='Đăng nhập', font=('Goudy Old Style', 20), fg_color='#0A3871', bg_color='white', text_color='white', cursor='hand2', corner_radius=10, height=35, command=self._on_login)
        loginButton.place(x=130, y=310)
        self.usernameEntry.focus_set()
        self.bind('<Return>', self._on_login)

        # Hiển thị giữa màn hình
        self._center_window()


    def _on_login(self, event=None):
        """
        SỬA: Hàm này giờ sẽ gọi Controller.
        """
        username = self.usernameEntry.get().strip()
        password = self.passwordEntry.get().strip()
        
        try:
            # 1. GỌI CONTROLLER (dùng logic caching_sha2_password)
            success = self.controller.login(username, password)
            
            if success:
                messagebox.showinfo('Đăng nhập thành công', 'Chào mừng đến với hệ thống!')
                self.destroy() # Đóng cửa sổ login
                if callable(self.on_login_success):
                    self.on_login_success() # 2. Gọi callback để mở app chính
            
        except Exception as e:
            # 3. Bắt lỗi từ Controller
            messagebox.showerror('Lỗi đăng nhập', str(e))
            self.passwordEntry.delete(0, tk.END)
            self.passwordEntry.focus_set()

    def _center_window(self) -> None:
        self.update_idletasks()
        
        # Lấy kích thước đã thiết lập từ geometry ban đầu
        try:
            geom = self.geometry().split('+')[0]
            w_str, h_str = geom.split('x')
            w, h = int(w_str), int(h_str)
        except Exception:
            # Fallback nếu không parse được
            w, h = 930, 478

        # Tính toán vị trí giữa màn hình
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        
        # Chỉ thay đổi vị trí, giữ nguyên kích thước
        self.geometry(f"+{x}+{y}")
if __name__ == '__main__':
    win = LoginWindow()
    win.mainloop()

