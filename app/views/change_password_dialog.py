"""
Dialog đổi mật khẩu cho user hiện tại.
Sử dụng CustomTkinter với font cố định để tránh lỗi "Too early to use font".
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Callable


class ChangePasswordDialog(ctk.CTkToplevel):
    """Dialog đổi mật khẩu với validation và error handling"""
    
    def __init__(self, parent, auth_controller, on_success: Callable = None):
        """
        Khởi tạo dialog đổi mật khẩu.
        
        Args:
            parent: Parent window
            auth_controller: AuthController instance để xử lý đổi mật khẩu
            on_success: Callback function khi đổi mật khẩu thành công
        """
        super().__init__(parent)
        
        self.auth_controller = auth_controller
        self.on_success_callback = on_success
        
        # Setup window
        self._setup_window()
        
        # Delay UI creation để tránh font errors (500ms như employee_form_dialog)
        self.after(500, self._delayed_init)
    
    def _setup_window(self):
        """Cấu hình window properties"""
        self.title("🔐 Đổi mật khẩu")
        self.geometry("500x500")  # Tăng chiều cao để chứa đủ buttons
        self.resizable(False, False)
        
        # Center window
        self.update_idletasks()
        width = 500
        height = 500
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Set modal behavior (will be applied after UI creation)
        self.transient(self.master)
        
    def _delayed_init(self):
        """Khởi tạo UI sau delay để tránh font errors"""
        if not self.winfo_exists():
            return
        
        self._create_ui()
        self.grab_set()  # Modal sau khi UI đã ready
        
    def _create_ui(self):
        """Tạo giao diện dialog"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🔐 Đổi mật khẩu",
            font=("Arial", 20, "bold"),
            text_color="#2C3E50"
        )
        title.pack(pady=(0, 20))
        
        # Form fields
        self._create_form_fields(main_frame)
        
        # Show password checkbox
        self._create_show_password_checkbox(main_frame)
        
        # Buttons - QUAN TRỌNG: Đảm bảo buttons được tạo
        self._create_buttons(main_frame)
        
        # Focus on first field
        if hasattr(self, 'old_password_entry'):
            self.old_password_entry.focus_set()
    
    def _create_form_fields(self, parent):
        """Tạo các trường nhập liệu"""
        # Old password
        old_pwd_label = ctk.CTkLabel(
            parent,
            text="Mật khẩu cũ:",
            font=("Arial", 14),
            text_color="#34495E",
            anchor="w"
        )
        old_pwd_label.pack(fill="x", pady=(0, 5))
        
        self.old_password_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Nhập mật khẩu cũ",
            font=("Arial", 13),
            height=40,
            show="●"
        )
        self.old_password_entry.pack(fill="x", pady=(0, 15))
        
        # New password
        new_pwd_label = ctk.CTkLabel(
            parent,
            text="Mật khẩu mới:",
            font=("Arial", 14),
            text_color="#34495E",
            anchor="w"
        )
        new_pwd_label.pack(fill="x", pady=(0, 5))
        
        self.new_password_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Nhập mật khẩu mới (tối thiểu 6 ký tự)",
            font=("Arial", 13),
            height=40,
            show="●"
        )
        self.new_password_entry.pack(fill="x", pady=(0, 15))
        
        # Confirm password
        confirm_pwd_label = ctk.CTkLabel(
            parent,
            text="Xác nhận mật khẩu mới:",
            font=("Arial", 14),
            text_color="#34495E",
            anchor="w"
        )
        confirm_pwd_label.pack(fill="x", pady=(0, 5))
        
        self.confirm_password_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Nhập lại mật khẩu mới",
            font=("Arial", 13),
            height=40,
            show="●"
        )
        self.confirm_password_entry.pack(fill="x", pady=(0, 5))
        
        # Bind Enter key
        self.old_password_entry.bind("<Return>", lambda e: self.new_password_entry.focus_set())
        self.new_password_entry.bind("<Return>", lambda e: self.confirm_password_entry.focus_set())
        self.confirm_password_entry.bind("<Return>", lambda e: self._on_change_password())
    
    def _create_show_password_checkbox(self, parent):
        """Tạo checkbox hiện/ẩn mật khẩu"""
        self.show_password_var = ctk.BooleanVar(master=self, value=False)
        
        show_password_cb = ctk.CTkCheckBox(
            parent,
            text="Hiện mật khẩu",
            font=("Arial", 12),
            variable=self.show_password_var,
            command=self._toggle_password_visibility
        )
        show_password_cb.pack(pady=(5, 15))
    
    def _toggle_password_visibility(self):
        """Toggle hiện/ẩn mật khẩu"""
        show = "" if self.show_password_var.get() else "●"
        self.old_password_entry.configure(show=show)
        self.new_password_entry.configure(show=show)
        self.confirm_password_entry.configure(show=show)
    
    def _create_buttons(self, parent):
        """Tạo các nút action"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Hủy",
            font=("Arial", 14, "bold"),
            height=45,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
            command=self._on_close
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Save/Change password button
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Lưu",
            font=("Arial", 14, "bold"),
            height=45,
            fg_color="#27AE60",
            hover_color="#229954",
            command=self._on_change_password
        )
        save_btn.pack(side="left", fill="x", expand=True)
    
    def _on_change_password(self):
        """Xử lý khi nhấn nút Đổi mật khẩu"""
        try:
            # Get values
            old_password = self.old_password_entry.get().strip()
            new_password = self.new_password_entry.get().strip()
            confirm_password = self.confirm_password_entry.get().strip()
            
            # Validate
            if not old_password:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập mật khẩu cũ!")
                self.old_password_entry.focus_set()
                return
            
            if not new_password:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập mật khẩu mới!")
                self.new_password_entry.focus_set()
                return
            
            if not confirm_password:
                messagebox.showwarning("Cảnh báo", "Vui lòng xác nhận mật khẩu mới!")
                self.confirm_password_entry.focus_set()
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận mật khẩu không khớp!")
                self.confirm_password_entry.delete(0, 'end')
                self.confirm_password_entry.focus_set()
                return
            
            # Call controller
            success = self.auth_controller.change_password(old_password, new_password)
            
            if success:
                messagebox.showinfo(
                    "Thành công",
                    "Đổi mật khẩu thành công!\nVui lòng sử dụng mật khẩu mới cho lần đăng nhập tiếp theo."
                )
                
                # Call success callback
                if self.on_success_callback:
                    self.on_success_callback()
                
                # Close dialog
                self._on_close()
            
        except ValueError as e:
            # Validation errors từ controller
            messagebox.showerror("Lỗi", str(e))
            # Clear passwords và focus lại
            if "Mật khẩu cũ không đúng" in str(e):
                self.old_password_entry.delete(0, 'end')
                self.old_password_entry.focus_set()
            elif "Mật khẩu mới phải có ít nhất" in str(e):
                self.new_password_entry.delete(0, 'end')
                self.confirm_password_entry.delete(0, 'end')
                self.new_password_entry.focus_set()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            print(f"❌ Error in change password: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_close(self):
        """Xử lý khi đóng dialog"""
        try:
            self.grab_release()
            self.withdraw()
            self.after(50, self._safe_destroy)
        except Exception as e:
            print(f"Error closing dialog: {e}")
    
    def _safe_destroy(self):
        """Destroy dialog an toàn"""
        try:
            if self.winfo_exists():
                self.destroy()
        except:
            pass
