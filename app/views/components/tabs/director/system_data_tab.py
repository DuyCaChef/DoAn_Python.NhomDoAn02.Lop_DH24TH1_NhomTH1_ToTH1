"""
System Data Tab - Director
Tab quản lý dữ liệu hệ thống (phòng ban, chức vụ, cấu hình)
"""
import customtkinter as ctk
from tkinter import messagebox
from app.views.components.tabs.base_tab import BaseTab


class SystemDataTab(BaseTab):
    """Tab quản lý dữ liệu hệ thống - Director only"""
    
    def setup_ui(self):
        """Thiết lập giao diện tab dữ liệu hệ thống"""
        # Title
        title = self.create_section_label(self.container, "⚙️ Quản lý dữ liệu hệ thống")
        title.pack(pady=(0, 20))
        
        # Tabs for different data types
        self.data_tabview = ctk.CTkTabview(self.container)
        self.data_tabview.pack(fill="both", expand=True)
        
        # Sub-tabs
        self.data_tabview.add("Phòng ban")
        self.data_tabview.add("Chức vụ")
        self.data_tabview.add("Cấu hình")
        
        # Setup each sub-tab
        self._setup_departments_tab()
        self._setup_roles_tab()
        self._setup_config_tab()
    
    def _setup_departments_tab(self):
        """Thiết lập tab phòng ban"""
        tab = self.data_tabview.tab("Phòng ban")
        
        # Action bar
        action_frame = ctk.CTkFrame(tab, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 10))
        
        add_btn = self.create_button(
            action_frame,
            "➕ Thêm phòng ban",
            lambda: self.add_department(),
            fg_color="#27AE60"
        )
        add_btn.pack(side="left")
        
        # Departments list
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True)
        
        # TODO: Load and display departments
        placeholder = ctk.CTkLabel(
            scroll_frame,
            text="Chức năng đang phát triển...",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        placeholder.pack(pady=50)
    
    def _setup_roles_tab(self):
        """Thiết lập tab chức vụ"""
        tab = self.data_tabview.tab("Chức vụ")
        
        # Action bar
        action_frame = ctk.CTkFrame(tab, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 10))
        
        add_btn = self.create_button(
            action_frame,
            "➕ Thêm chức vụ",
            lambda: self.add_role(),
            fg_color="#27AE60"
        )
        add_btn.pack(side="left")
        
        # Roles list
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True)
        
        # TODO: Load and display roles
        placeholder = ctk.CTkLabel(
            scroll_frame,
            text="Chức năng đang phát triển...",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        placeholder.pack(pady=50)
    
    def _setup_config_tab(self):
        """Thiết lập tab cấu hình hệ thống"""
        tab = self.data_tabview.tab("Cấu hình")
        
        config_frame = ctk.CTkFrame(tab)
        config_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # TODO: System configuration options
        placeholder = ctk.CTkLabel(
            config_frame,
            text="Cấu hình hệ thống đang phát triển...",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        placeholder.pack(pady=50)
    
    def add_department(self):
        """Thêm phòng ban mới"""
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
    
    def add_role(self):
        """Thêm chức vụ mới"""
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển", parent=self.container)
