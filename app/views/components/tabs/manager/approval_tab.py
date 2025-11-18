"""
Approval Tab - Manager
Tab duyệt yêu cầu nghỉ phép của nhân viên
"""
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from app.views.components.tabs.base_tab import BaseTab
from app.controllers.leave_request_controller import LeaveRequestController


class ApprovalTab(BaseTab):
    """Tab duyệt nghỉ phép - Manager"""
    
    def __init__(self, parent, auth_controller):
        self.leave_controller = LeaveRequestController()
        super().__init__(parent, auth_controller)
        
        # Define colors
        self.colors = {
            'primary': '#2C3E50',
            'success': '#27AE60',
            'danger': '#E74C3C',
            'warning': '#F39C12',
            'surface': '#ECF0F1'
        }
        
        self.setup_ui()
    
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
        """Tạo bảng danh sách yêu cầu"""
        table_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # Scrollable frame chứa rows
        self.scrollable_frame = ctk.CTkScrollableFrame(
            table_frame,
            fg_color=self.colors['surface']
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=self.colors['primary'],
            height=45
        )
        header_frame.pack(fill="x", padx=2, pady=2)
        header_frame.pack_propagate(False)
        
        # Column configs: (header, width)
        columns = [         
            ("ID", 60),
            ("Nhân viên", 180),
            ("Loại nghỉ", 140),
            ("Từ ngày", 120),
            ("Đến ngày", 120),
            ("Số ngày", 100),
            ("Lý do", 240),
            ("Trạng thái", 150),
            ("Thao tác", 260)
        ]
        
        for header, width in columns:
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 14, "bold"),
                text_color="white",
                width=width,
                anchor="center"
            )
            label.pack(side="left", padx=2)
    
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
        # Clear existing rows (giữ header)
        for widget in self.scrollable_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Get manager ID
        manager_id = self.auth_controller.get_current_user_employee_id()
        
        if not manager_id:
            placeholder = ctk.CTkLabel(
                self.scrollable_frame,
                text="Không tìm thấy thông tin quản lý",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            placeholder.pack(pady=50)
            return
        
        # Get filter status
        status_filter = self.status_filter.get()
        
        # Fetch requests
        if status_filter == "Tất cả":
            requests = self.leave_controller.get_all_requests_for_manager(manager_id)
        elif status_filter == "Chờ duyệt":
            requests = self.leave_controller.get_pending_requests_for_approval(manager_id)
        else:
            # Filter by specific status
            requests = self.leave_controller.get_all_requests_for_manager(manager_id, status_filter)
        
        if not requests:
            placeholder = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Không có yêu cầu nào ({status_filter.lower()})",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            placeholder.pack(pady=50)
            return
        
        # Display requests
        for req in requests:
            self._create_request_row(req)
    
    def _create_request_row(self, request):
        """Tạo 1 row cho request"""
        row_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="white",  # Nền trắng để chữ rõ hơn
            height=75
        )
        row_frame.pack(fill="x", padx=2, pady=2)
        row_frame.pack_propagate(False)
        
        # Map status to Vietnamese
        status_map = {
            'pending': 'Chờ duyệt',
            'approved': 'Đã duyệt',
            'rejected': 'Từ chối'
        }
        status_display = status_map.get(request['status'], request['status'])
        
        # Status colors
        status_colors = {
            "Chờ duyệt": "#FFA500",
            "Đã duyệt": "#27AE60",
            "Từ chối": "#E74C3C"
        }
        
        # ID
        id_label = ctk.CTkLabel(
            row_frame,
            text=str(request['id']),
            font=("Arial", 15, "bold"),
            text_color="#000000",
            width=60,
            anchor="center"
        )
        id_label.pack(side="left", padx=2)
        
        # Employee name - CENTER
        name_label = ctk.CTkLabel(
            row_frame,
            text=request['employee_name'],
            font=("Arial", 15, "bold"),
            text_color="#000000",
            width=180,
            anchor="center"
        )
        name_label.pack(side="left", padx=2)
        
        # Leave type - CENTER
        type_label = ctk.CTkLabel(
            row_frame,
            text=request['leave_type_display'],
            font=("Arial", 15, "bold"),
            text_color="#2C3E50",
            width=140,
            anchor="center"
        )
        type_label.pack(side="left", padx=2)
        
        # Start date
        start_date = str(request['start_date'])
        start_label = ctk.CTkLabel(
            row_frame,
            text=start_date,
            font=("Arial", 14, "bold"),
            text_color="#000000",
            width=120,
            anchor="center"
        )
        start_label.pack(side="left", padx=2)
        
        # End date
        end_date = str(request['end_date'])
        end_label = ctk.CTkLabel(
            row_frame,
            text=end_date,
            font=("Arial", 14, "bold"),
            text_color="#000000",
            width=120,
            anchor="center"
        )
        end_label.pack(side="left", padx=2)
        
        # Total days
        days_label = ctk.CTkLabel(
            row_frame,
            text=str(request['total_days']),
            font=("Arial", 16, "bold"),
            text_color="#E74C3C",
            width=100,
            anchor="center"
        )
        days_label.pack(side="left", padx=2)
        
        # Reason - CENTER
        reason = request.get('reason', '')
        if len(reason) > 35:
            reason = reason[:32] + "..."
        reason_label = ctk.CTkLabel(
            row_frame,
            text=reason,
            font=("Arial", 14, "bold"),
            text_color="#34495E",
            width=240,
            anchor="center"
        )
        reason_label.pack(side="left", padx=2)
        
        # Status
        status_label = ctk.CTkLabel(
            row_frame,
            text=status_display,
            font=("Arial", 15, "bold"),
            text_color=status_colors.get(status_display, "gray"),
            width=150,
            anchor="center"
        )
        status_label.pack(side="left", padx=2)
        
        # Actions - ONLY approve/reject buttons
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=260)
        action_frame.pack(side="left", padx=2)
        action_frame.pack_propagate(False)
        
        button_font = ("Arial", 13)
        
        # Show approve/reject only for pending requests
        if request['status'] == 'pending':
            approve_btn = ctk.CTkButton(
                action_frame,
                text="✅ Duyệt",
                font=button_font,
                width=90,
                height=32,
                fg_color="#27AE60",
                hover_color="#229954",
                command=lambda: self.approve_request(request['id'])
            )
            approve_btn.pack(side="left", padx=3)
            
            reject_btn = ctk.CTkButton(
                action_frame,
                text="❌ Từ chối",
                font=button_font,
                width=90,
                height=32,
                fg_color="#E74C3C",
                hover_color="#C0392B",
                command=lambda: self.reject_request(request['id'])
            )
            reject_btn.pack(side="left", padx=3)
        else:
            # For approved/rejected, show note if exists
            if request.get('manager_note'):
                note_label = ctk.CTkLabel(
                    action_frame,
                    text=f"Ghi chú: {request['manager_note'][:30]}...",
                    font=("Arial", 12, "italic"),
                    text_color="gray",
                    anchor="w"
                )
                note_label.pack(side="left", fill="both", expand=True, padx=5)
    
    def approve_request(self, request_id):
        """Duyệt yêu cầu"""
        # Confirm
        confirm = messagebox.askyesno(
            "Xác nhận duyệt",
            "Bạn có chắc muốn duyệt yêu cầu nghỉ phép này?",
            parent=self.container
        )
        
        if not confirm:
            return
        
        # Optional note
        note = simpledialog.askstring(
            "Ghi chú (tùy chọn)",
            "Nhập ghi chú cho nhân viên:",
            parent=self.container
        )
        
        # Get manager ID
        manager_id = self.auth_controller.get_current_user_employee_id()
        
        # Approve
        success, message = self.leave_controller.approve_request(
            request_id=request_id,
            manager_id=manager_id,
            note=note
        )
        
        if success:
            messagebox.showinfo("Thành công", message, parent=self.container)
            self.fetch_data()
        else:
            messagebox.showerror("Lỗi", message, parent=self.container)
    
    def reject_request(self, request_id):
        """Từ chối yêu cầu"""
        # Get reason (required)
        reason = simpledialog.askstring(
            "Lý do từ chối",
            "Nhập lý do từ chối (bắt buộc):",
            parent=self.container
        )
        
        if not reason:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập lý do từ chối!", parent=self.container)
            return
        
        # Confirm
        confirm = messagebox.askyesno(
            "Xác nhận từ chối",
            f"Bạn có chắc muốn từ chối yêu cầu này?\n\nLý do: {reason}",
            parent=self.container
        )
        
        if not confirm:
            return
        
        # Get manager ID
        manager_id = self.auth_controller.get_current_user_employee_id()
        
        # Reject
        success, message = self.leave_controller.reject_request(
            request_id=request_id,
            manager_id=manager_id,
            note=reason
        )
        
        if success:
            messagebox.showinfo("Thành công", message, parent=self.container)
            self.fetch_data()
        else:
            messagebox.showerror("Lỗi", message, parent=self.container)
    
    
    
    def _create_detail_field(self, parent, label_text, value):
        """Tạo field hiển thị thông tin"""
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=5)
        
        label = ctk.CTkLabel(
            field_frame,
            text=label_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
            width=120
        )
        label.pack(side="left", padx=(0, 10))
        
        value_label = ctk.CTkLabel(
            field_frame,
            text=str(value),
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        value_label.pack(side="left", fill="x", expand=True)
