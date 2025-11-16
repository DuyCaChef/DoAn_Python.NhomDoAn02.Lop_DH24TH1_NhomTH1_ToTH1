"""
Account Management Tab - Director
Tab quản lý tài khoản người dùng (username, password, roles)
"""
import customtkinter as ctk
from tkinter import messagebox
from app.views.components.tabs.base_tab import BaseTab


class AccountManagementTab(BaseTab):
    """Tab quản lý tài khoản - Director only"""
    
    def setup_ui(self):
        """Thiết lập giao diện tab quản lý tài khoản"""
        # Title
        title = self.create_section_label(self.container, "👤 Quản lý tài khoản người dùng")
        title.pack(pady=(0, 20))
        
        # Search bar
        self._create_search_bar()
        
        # Table
        self._create_accounts_table()
        
        # Load data
        self.fetch_data()
    
    def _create_search_bar(self):
        """Tạo thanh tìm kiếm"""
        search_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 15))
        
        self.search_entry = self.create_input_field(
            search_frame,
            "Tìm username, email..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        search_btn = self.create_button(
            search_frame,
            "🔍 Tìm kiếm",
            self.search_accounts,
            fg_color="#3498DB"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        add_btn = self.create_button(
            search_frame,
            "➕ Tạo tài khoản",
            self.add_account,
            fg_color="#27AE60"
        )
        add_btn.pack(side="left")
    
    def _create_accounts_table(self):
        """Tạo bảng tài khoản"""
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.container,
            label_text="📋 Danh sách tài khoản"
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # TODO: Implement table display
        placeholder = ctk.CTkLabel(
            self.scrollable_frame,
            text="Chức năng đang phát triển...",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        placeholder.pack(pady=50)
    
    def fetch_data(self):
        """Load danh sách tài khoản"""
        # TODO: Implement with controller
        pass
    
    def search_accounts(self):
        """Tìm kiếm tài khoản"""
        keyword = self.search_entry.get()
        # TODO: Implement search
        pass
    
    def add_account(self):
        """Thêm tài khoản mới"""
        # TODO: Open account form
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
