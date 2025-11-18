"""
Leave Request Tab - Employee
Tab gửi yêu cầu nghỉ phép
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
from app.views.components.tabs.base_tab import BaseTab
from app.controllers.leave_request_controller import LeaveRequestController


class LeaveRequestTab(BaseTab):
    """Tab yêu cầu nghỉ phép - Employee"""
    
    def __init__(self, parent, auth_controller):
        self.leave_controller = LeaveRequestController()
        super().__init__(parent, auth_controller)
        self.setup_ui()  # ← QUAN TRỌNG: Phải gọi setup_ui() vì đã override __init__
    
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
        
        # Get employee ID
        employee_id = self.auth_controller.get_current_user_employee_id()
        if not employee_id:
            placeholder = ctk.CTkLabel(
                self.history_frame,
                text="Không tìm thấy thông tin nhân viên",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            placeholder.pack(pady=30)
            return
        
        # Fetch requests từ database
        requests = self.leave_controller.get_my_requests(employee_id)
        
        if not requests:
            placeholder = ctk.CTkLabel(
                self.history_frame,
                text="Chưa có yêu cầu nào",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            placeholder.pack(pady=30)
            return
        
        # Display requests
        for req in requests:
            self._create_request_row(req)
    
    def submit_request(self):
        """Gửi yêu cầu nghỉ phép"""
        leave_type = self.leave_type.get()
        start = self.start_date.get().strip()
        end = self.end_date.get().strip()
        reason = self.reason_text.get("1.0", "end-1c").strip()
        
        # Get employee ID
        employee_id = self.auth_controller.get_current_user_employee_id()
        if not employee_id:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin nhân viên!", parent=self.container)
            return
        
        # Validation cơ bản
        if not all([start, end, reason]):
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin!", parent=self.container)
            return
        
        # Confirm
        confirm = messagebox.askyesno(
            "Xác nhận", 
            f"Bạn có chắc muốn gửi yêu cầu nghỉ phép?\n\n"
            f"Loại: {leave_type}\n"
            f"Từ: {start} → Đến: {end}\n"
            f"Lý do: {reason[:50]}...",
            parent=self.container
        )
        
        if not confirm:
            return
        
        # Submit với controller
        success, message = self.leave_controller.create_request(
            employee_id=employee_id,
            leave_type=leave_type,
            start_date_str=start,
            end_date_str=end,
            reason=reason
        )
        
        if success:
            messagebox.showinfo("Thành công", message, parent=self.container)
            
            # Clear form
            self.start_date.delete(0, 'end')
            self.end_date.delete(0, 'end')
            self.reason_text.delete("1.0", 'end')
            self.leave_type.set("Nghỉ phép năm")
            
            # Reload history
            self.fetch_data()
        else:
            messagebox.showerror("Lỗi", message, parent=self.container)
    
    def _create_request_row(self, request):
        """Tạo một hàng hiển thị yêu cầu"""
        # Row container
        row = ctk.CTkFrame(self.history_frame, fg_color="#2B2B2B", corner_radius=8)
        row.pack(fill="x", padx=5, pady=5)
        
        # Status color
        status_colors = {
            "pending": "#FFA500",  # Orange
            "approved": "#27AE60",  # Green
            "rejected": "#E74C3C"   # Red
        }
        status_color = status_colors.get(request['status'], "gray")
        
        # Content
        content = ctk.CTkFrame(row, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header: Type + Status
        header_frame = ctk.CTkFrame(content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 5))
        
        type_label = ctk.CTkLabel(
            header_frame,
            text=f"📋 {request['leave_type_display']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        type_label.pack(side="left")
        
        status_label = ctk.CTkLabel(
            header_frame,
            text=request['status_display'],
            font=ctk.CTkFont(size=12),
            text_color=status_color,
            anchor="e"
        )
        status_label.pack(side="right")
        
        # Dates
        dates_text = f"📅 {request['start_date']} → {request['end_date']} ({request['total_days']} ngày)"
        dates_label = ctk.CTkLabel(
            content,
            text=dates_text,
            font=ctk.CTkFont(size=11),
            text_color="lightgray",
            anchor="w"
        )
        dates_label.pack(fill="x", pady=2)
        
        # Reason (truncated)
        reason_text = request['reason'][:60] + "..." if len(request['reason']) > 60 else request['reason']
        reason_label = ctk.CTkLabel(
            content,
            text=f"💬 {reason_text}",
            font=ctk.CTkFont(size=11),
            text_color="lightgray",
            anchor="w"
        )
        reason_label.pack(fill="x", pady=2)
        
        # Footer: Created date + Action
        footer_frame = ctk.CTkFrame(content, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(5, 0))
        
        created_label = ctk.CTkLabel(
            footer_frame,
            text=f"🕐 {request['created_at'].strftime('%d/%m/%Y %H:%M')}",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        created_label.pack(side="left")
        
        # View detail button
        view_btn = ctk.CTkButton(
            footer_frame,
            text="👁 Xem",
            width=70,
            height=25,
            font=ctk.CTkFont(size=10),
            command=lambda: self._view_request_detail(request)
        )
        view_btn.pack(side="right")
    
    def _view_request_detail(self, request):
        """Hiển thị chi tiết yêu cầu"""
        detail_window = ctk.CTkToplevel(self.container)
        detail_window.title("Chi tiết yêu cầu nghỉ phép")
        detail_window.geometry("500x600")
        
        # Main frame
        main_frame = ctk.CTkScrollableFrame(detail_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="📋 Chi tiết yêu cầu nghỉ phép",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Info fields
        fields = [
            ("Loại nghỉ phép:", request['leave_type_display']),
            ("Từ ngày:", str(request['start_date'])),
            ("Đến ngày:", str(request['end_date'])),
            ("Tổng số ngày:", f"{request['total_days']} ngày"),
            ("Trạng thái:", request['status_display']),
            ("Ngày gửi:", request['created_at'].strftime('%d/%m/%Y %H:%M')),
        ]
        
        if request.get('manager_name'):
            fields.append(("Quản lý:", request['manager_name']))
        
        for label_text, value in fields:
            self._create_detail_field(main_frame, label_text, value)
        
        # Reason (full)
        reason_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        reason_frame.pack(fill="x", pady=10)
        
        reason_label = ctk.CTkLabel(
            reason_frame,
            text="Lý do:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        reason_label.pack(fill="x", pady=(0, 5))
        
        reason_text = ctk.CTkTextbox(reason_frame, height=100)
        reason_text.insert("1.0", request['reason'])
        reason_text.configure(state="disabled")
        reason_text.pack(fill="x")
        
        # Manager note (if any)
        if request.get('manager_note'):
            note_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            note_frame.pack(fill="x", pady=10)
            
            note_label = ctk.CTkLabel(
                note_frame,
                text="Ghi chú của quản lý:",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            note_label.pack(fill="x", pady=(0, 5))
            
            note_text = ctk.CTkTextbox(note_frame, height=80)
            note_text.insert("1.0", request['manager_note'])
            note_text.configure(state="disabled")
            note_text.pack(fill="x")
        
        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="Đóng",
            command=detail_window.destroy
        )
        close_btn.pack(pady=20)
    
    def _create_detail_field(self, parent, label_text, value):
        """Tạo field hiển thị thông tin"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(
            field_frame,
            text=label_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
            width=150
        )
        label.pack(side="left")
        
        value_label = ctk.CTkLabel(
            field_frame,
            text=str(value),
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        value_label.pack(side="left", fill="x", expand=True)
