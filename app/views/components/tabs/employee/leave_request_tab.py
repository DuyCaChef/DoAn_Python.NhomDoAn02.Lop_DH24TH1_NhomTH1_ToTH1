"""
Leave Request Tab - Employee
Tab gửi yêu cầu nghỉ phép
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
from app.views.components.tabs.base_tab import BaseTab


class LeaveRequestTab(BaseTab):
    """Tab yêu cầu nghỉ phép - Employee"""
    
    def setup_ui(self):
        """Thiết lập giao diện tab nghỉ phép"""
        # Title
        title = self.create_section_label(self.container, "📝 Yêu cầu nghỉ phép")
        title.pack(pady=(0, 20))
        
        # Main content với 2 phần: Form và History
        content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Left: Request Form
        form_frame = ctk.CTkFrame(content_frame)
        form_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self._create_request_form(form_frame)
        
        # Right: Request History
        history_frame = ctk.CTkFrame(content_frame)
        history_frame.pack(side="right", fill="both", expand=True)
        
        self._create_request_history(history_frame)
        
        # Load history
        self.fetch_data()
    
    def _create_request_form(self, parent):
        """Tạo form gửi yêu cầu nghỉ phép"""
        # Header
        header = self.create_section_label(parent, "✉️ Gửi yêu cầu mới")
        header.pack(pady=15)
        
        # Form content
        form_content = ctk.CTkFrame(parent, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Leave type
        type_label = ctk.CTkLabel(form_content, text="Loại nghỉ phép:", anchor="w")
        type_label.pack(fill="x", pady=(0, 5))
        
        self.leave_type = ctk.CTkComboBox(
            form_content,
            values=["Nghỉ phép năm", "Nghỉ ốm", "Nghỉ việc riêng", "Nghỉ không lương"],
            state="readonly"
        )
        self.leave_type.set("Nghỉ phép năm")
        self.leave_type.pack(fill="x", pady=(0, 15))
        
        # Start date
        start_label = ctk.CTkLabel(form_content, text="Từ ngày:", anchor="w")
        start_label.pack(fill="x", pady=(0, 5))
        
        self.start_date = self.create_input_field(form_content, "YYYY-MM-DD")
        self.start_date.pack(fill="x", pady=(0, 15))
        
        # End date
        end_label = ctk.CTkLabel(form_content, text="Đến ngày:", anchor="w")
        end_label.pack(fill="x", pady=(0, 5))
        
        self.end_date = self.create_input_field(form_content, "YYYY-MM-DD")
        self.end_date.pack(fill="x", pady=(0, 15))
        
        # Reason
        reason_label = ctk.CTkLabel(form_content, text="Lý do:", anchor="w")
        reason_label.pack(fill="x", pady=(0, 5))
        
        self.reason_text = ctk.CTkTextbox(form_content, height=100)
        self.reason_text.pack(fill="x", pady=(0, 15))
        
        # Submit button
        submit_btn = self.create_button(
            form_content,
            "📨 Gửi yêu cầu",
            self.submit_request,
            fg_color="#27AE60",
            hover_color="#229954"
        )
        submit_btn.pack(fill="x")
    
    def _create_request_history(self, parent):
        """Tạo lịch sử yêu cầu"""
        # Header
        header = self.create_section_label(parent, "📜 Lịch sử yêu cầu")
        header.pack(pady=15)
        
        # Scrollable list
        self.history_frame = ctk.CTkScrollableFrame(parent)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def fetch_data(self):
        """Load lịch sử yêu cầu"""
        # Clear existing
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # TODO: Fetch từ database
        # Placeholder
        placeholder = ctk.CTkLabel(
            self.history_frame,
            text="Chưa có yêu cầu nào",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        placeholder.pack(pady=30)
    
    def submit_request(self):
        """Gửi yêu cầu nghỉ phép"""
        leave_type = self.leave_type.get()
        start = self.start_date.get().strip()
        end = self.end_date.get().strip()
        reason = self.reason_text.get("1.0", "end-1c").strip()
        
        # Validation
        if not all([start, end, reason]):
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin!", parent=self.container)
            return
        
        # Validate date format
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            
            if start_date > end_date:
                messagebox.showerror("Lỗi", "Ngày bắt đầu phải trước ngày kết thúc!", parent=self.container)
                return
            
            if start_date < date.today():
                messagebox.showwarning("Cảnh báo", "Ngày bắt đầu nên từ hôm nay trở đi!", parent=self.container)
                return
        
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ! (YYYY-MM-DD)", parent=self.container)
            return
        
        # TODO: Submit với controller
        messagebox.showinfo("Thành công", "Đã gửi yêu cầu nghỉ phép!", parent=self.container)
        
        # Clear form
        self.start_date.delete(0, 'end')
        self.end_date.delete(0, 'end')
        self.reason_text.delete("1.0", 'end')
        
        # Reload history
        self.fetch_data()
