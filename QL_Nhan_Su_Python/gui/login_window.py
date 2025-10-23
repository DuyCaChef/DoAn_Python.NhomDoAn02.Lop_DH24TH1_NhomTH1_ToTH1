from customtkinter import *
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

def LoginWindow(event=None):
    ## Xử lý login. event được hỗ trợ để bind Enter key.
    username = usernameEntry.get().strip()
    password = passwordEntry.get().strip()

    if username == '' or password == '':
        messagebox.showerror('Lỗi đăng nhập', 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!')
        if username == '':
            usernameEntry.focus_set()
        else:
            passwordEntry.focus_set()
        return
    
    elif username == 'admin' and password == 'admin@123':
        messagebox.showinfo('Đăng nhập thành công', 'Chào mừng đến với hệ thống!')
        root.destroy()  # Đóng cửa sổ đăng nhập
        return

    else:
        messagebox.showerror('Lỗi đăng nhập', 'Tên đăng nhập hoặc mật khẩu không đúng!')
        # Xóa mật khẩu và focus lại
        passwordEntry.delete(0, tk.END)
        passwordEntry.focus_set()


root = CTk()
root.geometry('930x478')
root.resizable(0, 0) 
root.title('Đăng nhập hệ thống')
root.config(bg='white')

# Tạo hình nền trang đăng nhập, lấy đường dẫn tuyệt đối đến ảnh
current_dir = os.path.dirname(__file__)   # thư mục hiện tại: gui/
image_path = os.path.join(current_dir, '../assets/image/bg_login.jpg')
image_path = os.path.abspath(image_path)

# 👉 Mở ảnh
image = CTkImage(light_image=Image.open(image_path), size=(500, 500))
imageLabel = CTkLabel(root, image=image, text='')
imageLabel.place(x=380, y=0)

#Phần đăng nhập
headingLabel= CTkLabel(root, text='Đăng nhập hệ thống', font=('Goudy Old Style', 30, 'bold'), bg_color='white',text_color='#0A3871')
headingLabel.place(x=65, y=50)

usernameLabel = CTkLabel(root, text='Tên đăng nhập', font=('Goudy Old Style', 17, 'italic', ), bg_color='white',text_color='#0A3871')
usernameLabel.place(x=80, y=120)
usernameEntry = CTkEntry(root, placeholder_text='Nhập tên đăng nhập', font=('Goudy Old Style', 15), bg_color='white',width=250)
usernameEntry.place(x=80, y=150)

passwordLabel = CTkLabel(root, text='Mật khẩu', font=('Goudy Old Style', 17, 'italic', ), bg_color='white',text_color='#0A3871')
passwordLabel.place(x=80, y=200)
passwordEntry = CTkEntry(root, placeholder_text='Nhập mật khẩu', font=('Goudy Old Style', 15), bg_color='white', width=250, show='*')
passwordEntry.place(x=80, y=230)

# Toggle hiển thị mật khẩu bằng checkbox
show_var = tk.BooleanVar(value=False)
def on_show_var_changed():
    if show_var.get():
        passwordEntry.configure(show='')
    else:
        passwordEntry.configure(show='*')
show_checkbox = CTkCheckBox(root, text='Hiện mật khẩu',font=('Goudy Old Style', 13, 'italic', ), command=on_show_var_changed, variable=show_var, fg_color="#2b82e4", bg_color='white', text_color='#0A3871',checkbox_height=18, checkbox_width=18)
show_checkbox.place(x=80, y=265)

loginButton = CTkButton(root, text='Đăng nhập', font=('Goudy Old Style', 20), fg_color='#0A3871', bg_color='white', text_color='white', cursor='hand2', corner_radius=10,height= 35, command=LoginWindow)
loginButton.place(x=130, y=310)

# Focus ban đầu và bind Enter
usernameEntry.focus_set()
root.bind('<Return>', LoginWindow)

root.mainloop()