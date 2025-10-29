import customtkinter as ctk
import os
from PIL import Image
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable

try:
    # relative import within the gui package
    from .form_employee import App as EmployeeApp
except Exception:
    EmployeeApp = None


class LoginWindow(ctk.CTk):
    def __init__(self, on_login_success: Optional[Callable[[], None]] = None):
        super().__init__()
        self.on_login_success = on_login_success

        self.geometry('930x478')
        self.resizable(0, 0)
        self.title('Đăng nhập hệ thống')
        self.config(bg='white')

        # Tạo hình nền trang đăng nhập, lấy đường dẫn tuyệt đối đến ảnh
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, '..', 'assets', 'image', 'bg_login.jpg')
        image_path = os.path.abspath(image_path)

        # Mở ảnh nếu có
        if os.path.exists(image_path):
            image = ctk.CTkImage(light_image=Image.open(image_path), size=(500, 500))
            imageLabel = ctk.CTkLabel(self, image=image, text='')
            imageLabel.image = image
            imageLabel.place(x=380, y=0)

        # Phần đăng nhập
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

        # Toggle hiển thị mật khẩu bằng checkbox
        self.show_var = tk.BooleanVar(value=False)

        def on_show_var_changed():
            if self.show_var.get():
                self.passwordEntry.configure(show='')
            else:
                self.passwordEntry.configure(show='*')

        show_checkbox = ctk.CTkCheckBox(self, text='Hiện mật khẩu', font=('Goudy Old Style', 13, 'italic'), command=on_show_var_changed, variable=self.show_var, fg_color="#2b82e4", bg_color='white', text_color='#0A3871', checkbox_height=18, checkbox_width=18)
        show_checkbox.place(x=80, y=265)

        loginButton = ctk.CTkButton(self, text='Đăng nhập', font=('Goudy Old Style', 20), fg_color='#0A3871', bg_color='white', text_color='white', cursor='hand2', corner_radius=10, height=35, command=self._on_login)
        loginButton.place(x=130, y=310)

        # Focus ban đầu và bind Enter
        self.usernameEntry.focus_set()
        self.bind('<Return>', self._on_login)

        # Hiển thị giữa màn hình
        self._center_window()


    def _on_login(self, event=None):
        username = self.usernameEntry.get().strip()
        password = self.passwordEntry.get().strip()

        if username == '' or password == '':
            messagebox.showerror('Lỗi đăng nhập', 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!')
            if username == '':
                self.usernameEntry.focus_set()
            else:
                self.passwordEntry.focus_set()
            return

        # TODO: Replace with real authentication
        if username == 'admin@gmail.com' and password == 'admin@123':
            messagebox.showinfo('Đăng nhập thành công', 'Chào mừng đến với hệ thống!')
            # Close login window and open main app
            self.destroy()
            if callable(self.on_login_success):
                self.on_login_success()
            else:
                if EmployeeApp:
                    app = EmployeeApp()
                    app.mainloop()
            return

        # Sai thông tin
        messagebox.showerror('Lỗi đăng nhập', 'Tên đăng nhập hoặc mật khẩu không đúng!')
        self.passwordEntry.delete(0, tk.END)
        self.passwordEntry.focus_set()

    def _center_window(self) -> None:
        """Center this window on the primary screen without changing its size."""
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