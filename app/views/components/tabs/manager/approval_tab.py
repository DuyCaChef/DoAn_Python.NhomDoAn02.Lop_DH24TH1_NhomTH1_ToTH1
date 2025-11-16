"""
Approval Tab - Manager
Tab duyệt yêu cầu nghỉ phép của nhân viên
"""
import customtkinter as ctk
from tkinter import messagebox
from app.views.components.tabs.base_tab import BaseTab


class ApprovalTab(BaseTab):
    """Tab duyệt nghỉ phép - Manager"""
    
    def setup_ui(self):
        """Thiết lập giao diện tab duyệt"""
        # Title
        title = self.create_section_label(self.container, "✅ Duyệt yêu cầu nghỉ phép")
        title.pack(pady=(0, 20))
        
        # Filter bar
        self._create_filter_bar()
        
        # Requests table
        self._create_requests_table()
        
        # Load data
        self.fetch_data()
    
    def _create_filter_bar(self):
        """Tạo thanh lọc yêu cầu"""
        filter_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 15))
        
        # Status filter
        ctk.CTkLabel(filter_frame, text="Trạng thái:").pack(side="left", padx=(0, 10))
        
        self.status_filter = ctk.CTkComboBox(
            filter_frame,
            values=["Tất cả", "Chờ duyệt", "Đã duyệt", "Từ chối"],
            command=lambda _: self.fetch_data(),
            width=150
        )
        self.status_filter.set("Chờ duyệt")
        self.status_filter.pack(side="left", padx=(0, 20))
        
        # Refresh button
        refresh_btn = self.create_button(
            filter_frame,
            "🔄 Làm mới",
            self.fetch_data,
            fg_color="#95A5A6"
        )
        refresh_btn.pack(side="left")
    
    def _create_requests_table(self):
        """Tạo bảng yêu cầu"""
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.container,
            label_text="📋 Danh sách yêu cầu nghỉ phép"
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Header
        self._create_table_header()
    
    def _create_table_header(self):
        """Tạo header bảng"""
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2C3E50", height=40)
        header_frame.pack(fill="x", pady=(0, 2))
        header_frame.pack_propagate(False)
        
        headers = [
            ("Nhân viên", 0.20),
            ("Loại nghỉ", 0.15),
            ("Từ ngày", 0.15),
            ("Đến ngày", 0.15),
            ("Lý do", 0.20),
            ("Thao tác", 0.15)
        ]
        
        x_pos = 0
        for text, width in headers:
            label = ctk.CTkLabel(
                header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white"
            )
            label.place(relx=x_pos, rely=0.5, anchor="w", relwidth=width)
            x_pos += width
    
    def fetch_data(self):
        """Load danh sách yêu cầu nghỉ phép"""
        # Clear existing
        for widget in self.scrollable_frame.winfo_children()[1:]:
            widget.destroy()
        
        # TODO: Fetch từ database
        # Hiện tại hiển thị placeholder
        placeholder = ctk.CTkLabel(
            self.scrollable_frame,
            text="Chưa có yêu cầu nghỉ phép nào",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        placeholder.pack(pady=50)
    
    def approve_request(self, request_id):
        """Duyệt yêu cầu"""
        # TODO: Implement với controller
        messagebox.showinfo("Thành công", "Đã duyệt yêu cầu!", parent=self.container)
        self.fetch_data()
    
    def reject_request(self, request_id):
        """Từ chối yêu cầu"""
        # TODO: Implement với controller
        messagebox.showinfo("Thông báo", "Đã từ chối yêu cầu!", parent=self.container)
        self.fetch_data()
