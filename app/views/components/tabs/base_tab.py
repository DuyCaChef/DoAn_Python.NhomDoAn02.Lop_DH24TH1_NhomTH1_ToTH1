"""
Base Tab Component
Lớp cơ sở cho tất cả các tab components
"""
import customtkinter as ctk
from abc import ABC, abstractmethod


class BaseTab(ABC):
    """
    Lớp cơ sở trừu tượng cho các tab components
    """
    
    def __init__(self, parent, auth_controller):
        """
        Args:
            parent: Frame cha (tab container)
            auth_controller: AuthController để xử lý authentication
        """
        self.parent = parent
        self.auth_controller = auth_controller
        
        # Tạo container chính cho tab
        self.container = ctk.CTkFrame(parent, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Gọi setup_ui() CHUNG cho các tab không override __init__()
        # Các tab có override __init__() sẽ tự gọi setup_ui() sau khi khởi tạo xong
        if type(self).__init__ == BaseTab.__init__:
            self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """
        Phương thức trừu tượng để tạo giao diện
        Phải được implement bởi các lớp con
        """
        pass
    
    def create_section_label(self, parent, text, **kwargs):
        """Tạo label tiêu đề section"""
        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=18, weight="bold"),
            **kwargs
        )
    
    def create_input_field(self, parent, label_text, placeholder="", **kwargs):
        """Tạo cặp label + entry field"""
        label = ctk.CTkLabel(parent, text=label_text, anchor="w")
        label.pack(fill="x", padx=20, pady=(10, 5))
        
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, **kwargs)
        entry.pack(fill="x", padx=20, pady=(0, 10))
        
        return entry
    
    def create_button(self, parent, text, command, **kwargs):
        """Tạo button với style mặc định"""
        default_style = {
            'height': 35,
            'font': ctk.CTkFont(size=13),
            'fg_color': "#3B8ED0",
            'hover_color': "#2E6FA5"
        }
        default_style.update(kwargs)
        
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            **default_style
        )
