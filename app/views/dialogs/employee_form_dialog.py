"""
Employee Form Dialog
Dialog để thêm/sửa/xem thông tin nhân viên
"""

import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable
import re
from app.views.components.loading_overlay import LoadingOverlay


class EmployeeFormDialog:
    """Dialog form cho thêm/sửa/xem nhân viên"""
    
    def __init__(
        self,
        parent,
        employee_controller,
        auth_controller,
        mode: str = "add",  # "add", "edit", "view"
        employee_data: Optional[dict] = None,
        on_success: Optional[Callable] = None
    ):
        """
        Args:
            parent: Widget cha (để làm transient)
            employee_controller: Controller xử lý logic nhân viên
            auth_controller: Controller lấy thông tin user hiện tại
            mode: Chế độ - "add" (thêm mới), "edit" (sửa), "view" (xem)
            employee_data: Dữ liệu nhân viên (dùng cho edit/view)
            on_success: Callback khi thành công (để refresh data)
        """
        self.parent = parent
        self.employee_controller = employee_controller
        self.auth_controller = auth_controller
        self.mode = mode
        self.employee_data = employee_data or {}
        self.on_success = on_success
        
        # Tạo dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self._setup_window()
        self._create_ui()
        
        # ⚠️ GỌI grab_set() SAU KHI đã tạo xong UI
        self.dialog.grab_set()
        
    def _setup_window(self):
        """Cấu hình cửa sổ dialog"""
        titles = {
            "add": "Thêm nhân viên mới",
            "edit": "Chỉnh sửa thông tin nhân viên",
            "view": "Xem thông tin nhân viên"
        }
        
        self.dialog.title(titles.get(self.mode, "Nhân viên"))
        self.dialog.geometry("600x750")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (750 // 2)
        self.dialog.geometry(f"600x750+{x}+{y}")
        
        # ⚠️ GỌI grab_set() SAU KHI tạo xong UI
        # Sẽ được gọi trong __init__ sau _create_ui()
        
    def _create_ui(self):
        """Tạo giao diện"""
        try:
            # Header
            icons = {"add": "➕", "edit": "✏️", "view": "👁️"}
            titles = {
                "add": "Thêm nhân viên mới",
                "edit": "Chỉnh sửa nhân viên",
                "view": "Thông tin nhân viên"
            }
            
            header = ctk.CTkLabel(
                self.dialog,
                text=f"{icons.get(self.mode, '')} {titles.get(self.mode, '')}",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            header.pack(pady=20)
            
            # Form container với scroll
            self.form_frame = ctk.CTkScrollableFrame(self.dialog)
            self.form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            # ✅ Enable mouse wheel scroll
            self._enable_mouse_wheel_scroll()
            
            # Tạo các fields
            self._create_form_fields()
            
            # Buttons
            self._create_buttons()
            
        except Exception as e:
            print(f"❌ LỖI trong _create_ui(): {e}")
            import traceback
            traceback.print_exc()
    
    def _enable_mouse_wheel_scroll(self):
        """Kích hoạt scroll bằng chuột cho form"""
        def _on_mousewheel(event):
            # Linux sử dụng Button-4 (scroll up) và Button-5 (scroll down)
            if event.num == 4 or event.delta > 0:
                self.form_frame._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.form_frame._parent_canvas.yview_scroll(1, "units")
        
        # Bind cho dialog window
        self.dialog.bind_all("<Button-4>", _on_mousewheel, add="+")
        self.dialog.bind_all("<Button-5>", _on_mousewheel, add="+")
        self.dialog.bind_all("<MouseWheel>", _on_mousewheel, add="+")  # Windows/Mac
        
        # Unbind khi dialog đóng để tránh memory leak
        def _cleanup():
            try:
                self.dialog.unbind_all("<Button-4>")
                self.dialog.unbind_all("<Button-5>")
                self.dialog.unbind_all("<MouseWheel>")
            except:
                pass
        
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: [_cleanup(), self.dialog.destroy()])
        
    def _create_form_fields(self):
        """Tạo các trường nhập liệu"""
        is_readonly = self.mode == "view"
        
        # Mã nhân viên
        self._create_field(
            "Mã nhân viên",
            "employee_code",
            placeholder="Nhập mã NV (VD: NV001)",
            required=True,
            readonly=is_readonly
        )
        
        # Họ
        self._create_field(
            "Họ",
            "last_name",
            placeholder="Nguyễn Văn",
            required=True,
            readonly=is_readonly
        )
        
        # Tên
        self._create_field(
            "Tên",
            "first_name",
            placeholder="A",
            required=True,
            readonly=is_readonly
        )
        
        # Giới tính
        ctk.CTkLabel(self.form_frame, text="Giới tính:", anchor="w").pack(fill="x", pady=(10, 5))
        self.gender_var = ctk.StringVar(value=self.employee_data.get('gender', 'Male'))
        gender_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        gender_frame.pack(fill="x", pady=(0, 10))
        
        state = "disabled" if is_readonly else "normal"
        ctk.CTkRadioButton(
            gender_frame, text="Nam", variable=self.gender_var, 
            value="Male", state=state
        ).pack(side="left", padx=10)
        ctk.CTkRadioButton(
            gender_frame, text="Nữ", variable=self.gender_var, 
            value="Female", state=state
        ).pack(side="left", padx=10)
        ctk.CTkRadioButton(
            gender_frame, text="Khác", variable=self.gender_var, 
            value="Other", state=state
        ).pack(side="left", padx=10)
        
        # Ngày sinh
        self._create_field(
            "Ngày sinh",
            "date_of_birth",
            placeholder="YYYY-MM-DD (VD: 1990-01-15)",
            required=True,
            readonly=is_readonly
        )
        
        # Email
        self._create_field(
            "Email",
            "email",
            placeholder="email@example.com",
            required=True,
            readonly=is_readonly
        )
        
        # Số điện thoại
        self._create_field(
            "Số điện thoại",
            "phone_number",
            placeholder="0901234567",
            readonly=is_readonly
        )
        
        # Địa chỉ
        self._create_field(
            "Địa chỉ",
            "address",
            placeholder="Nhập địa chỉ",
            readonly=is_readonly
        )
        
        # Ngày vào làm
        self._create_field(
            "Ngày vào làm",
            "hire_date",
            placeholder="YYYY-MM-DD (VD: 2024-01-01)",
            required=True,
            readonly=is_readonly
        )
        
        # Phòng ban
        if self.mode == "add":
            # Khi thêm mới: lấy phòng ban của manager
            user_dept = self.auth_controller.current_user_data.get('department_name', 'Chưa xác định')
            ctk.CTkLabel(self.form_frame, text="Phòng ban:", anchor="w").pack(fill="x", pady=(10, 5))
            dept_label = ctk.CTkLabel(
                self.form_frame,
                text=f"  {user_dept}",
                anchor="w",
                fg_color="#2C3E50",
                corner_radius=5,
                height=35
            )
            dept_label.pack(fill="x", pady=(0, 10))
        else:
            # Khi view/edit: hiển thị phòng ban hiện tại
            dept_name = self.employee_data.get('department_name', 'Chưa xác định')
            self._create_field(
                "Phòng ban",
                "department_name",
                default_value=dept_name,
                readonly=True  # Không cho sửa phòng ban
            )
        
        # Chức vụ - Load từ database
        ctk.CTkLabel(self.form_frame, text="Chức vụ:", anchor="w").pack(fill="x", pady=(10, 5))
        
        # Lấy danh sách positions từ database
        positions_list = []
        self.positions_map = {}  # Khởi tạo trước
        
        try:
            from app.database.employee_queries import EmployeeQueries
            emp_queries = EmployeeQueries()
            positions_data = emp_queries.get_all_positions()
            
            print(f"🔍 DEBUG: Loaded {len(positions_data) if positions_data else 0} positions from DB")
            
            # Tạo dict để map id -> title và list values cho combo
            for pos in positions_data:
                pos_id = pos.get('id')
                pos_title = pos.get('title')
                dept_name = pos.get('department_name', '')
                
                # Format: "Employee (IT Department)"
                display_text = f"{pos_title} ({dept_name})"
                positions_list.append(display_text)
                self.positions_map[pos_id] = display_text
                print(f"🔍 DEBUG: Mapped {pos_id} -> {display_text}")
            
            if not positions_list:
                print("⚠️ DEBUG: positions_list trống, dùng fallback")
                positions_list = ["Employee", "Senior Employee", "Team Lead"]
            else:
                print(f"✅ DEBUG: Loaded {len(positions_list)} positions successfully")
                
        except Exception as e:
            print(f"❌ ERROR: Không load được positions từ DB: {e}")
            import traceback
            traceback.print_exc()
            positions_list = ["Employee", "Senior Employee", "Team Lead", "Manager", "Director"]
            self.positions_map = {}
        
        self.position_combo = ctk.CTkComboBox(
            self.form_frame,
            values=positions_list,
            state="disabled" if is_readonly else "readonly"
        )
        
        # Set giá trị hiện tại
        if self.mode in ["edit", "view"] and self.employee_data:
            # Lấy position_id từ employee_data
            pos_id = self.employee_data.get('position_id')
            if pos_id and pos_id in self.positions_map:
                self.position_combo.set(self.positions_map[pos_id])
            else:
                # Fallback: dùng position_title từ query
                pos_title = self.employee_data.get('position_title', '')
                dept_name = self.employee_data.get('department_name', '')
                if pos_title:
                    display = f"{pos_title} ({dept_name})" if dept_name else pos_title
                    self.position_combo.set(display)
                else:
                    self.position_combo.set(positions_list[0] if positions_list else "Employee")
        else:
            # Mode add: set default
            self.position_combo.set(positions_list[0] if positions_list else "Employee")
            
        self.position_combo.pack(fill="x", pady=(0, 10))
        
        # Trạng thái
        ctk.CTkLabel(self.form_frame, text="Trạng thái:", anchor="w").pack(fill="x", pady=(10, 5))
        statuses = ["Thử việc", "Đang làm việc", "Đã nghỉ việc"]
        self.status_combo = ctk.CTkComboBox(
            self.form_frame,
            values=statuses,
            state="readonly" if is_readonly else "readonly"
        )
        current_status = self.employee_data.get('status', 'Thử việc')
        self.status_combo.set(current_status if current_status in statuses else "Thử việc")
        self.status_combo.pack(fill="x", pady=(0, 10))
        
    def _create_field(
        self, 
        label: str, 
        field_name: str, 
        placeholder: str = "", 
        required: bool = False,
        readonly: bool = False,
        default_value: str = None
    ):
        """Tạo một field input"""
        label_text = f"{label}:{' *' if required else ''}"
        ctk.CTkLabel(self.form_frame, text=label_text, anchor="w").pack(fill="x", pady=(10, 5))
        
        # Lấy giá trị mặc định từ employee_data nếu có
        if default_value is None:
            default_value = self.employee_data.get(field_name, "")
        
        entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text=placeholder,
            state="disabled" if readonly else "normal"
        )
        
        if default_value:
            entry.insert(0, str(default_value))
            
        entry.pack(fill="x", pady=(0, 10))
        
        # Lưu reference để lấy giá trị sau
        setattr(self, f"{field_name}_entry", entry)
        
    def _create_buttons(self):
        """Tạo các nút bấm"""
        buttons_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        if self.mode == "view":
            # Chỉ có nút Đóng
            close_btn = ctk.CTkButton(
                buttons_frame,
                text="✕ Đóng",
                command=self.dialog.destroy,
                fg_color="#95A5A6",
                hover_color="#7F8C8D",
                width=150,
                height=40
            )
            close_btn.pack(pady=10)
        else:
            # Có nút Lưu và Hủy
            save_btn = ctk.CTkButton(
                buttons_frame,
                text="💾 Lưu",
                command=self._save,
                fg_color="#27AE60",
                hover_color="#229954",
                width=150,
                height=40
            )
            save_btn.pack(side="left", padx=(0, 10))
            
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="✕ Hủy",
                command=self.dialog.destroy,
                fg_color="#95A5A6",
                hover_color="#7F8C8D",
                width=150,
                height=40
            )
            cancel_btn.pack(side="left")
            
        # Focus vào field đầu tiên nếu không phải view mode
        if self.mode != "view" and hasattr(self, 'employee_code_entry'):
            self.employee_code_entry.focus()
            
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_date(self, date_str: str) -> bool:
        """Validate date format YYYY-MM-DD"""
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(pattern, date_str) is not None
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate phone number (optional, Vietnamese format)"""
        if not phone:
            return True  # Phone is optional
        pattern = r'^(0|\+84)[0-9]{9,10}$'
        return re.match(pattern, phone) is not None
    
    def _save(self):
        """Lưu dữ liệu"""
        # Lấy dữ liệu từ form
        employee_code = self.employee_code_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        dob = self.date_of_birth_entry.get().strip()
        hire_date = self.hire_date_entry.get().strip()
        phone = self.phone_number_entry.get().strip()
        address = self.address_entry.get().strip()
        
        # Validate required fields
        if not all([employee_code, first_name, last_name, email, dob, hire_date]):
            messagebox.showerror(
                "Lỗi",
                "Vui lòng điền đầy đủ các trường bắt buộc (*)",
                parent=self.dialog
            )
            return
        
        # Validate email
        if not self._validate_email(email):
            messagebox.showerror(
                "Lỗi",
                "Email không hợp lệ!",
                parent=self.dialog
            )
            return
        
        # Validate dates
        if not self._validate_date(dob):
            messagebox.showerror(
                "Lỗi",
                "Ngày sinh không hợp lệ! Định dạng: YYYY-MM-DD",
                parent=self.dialog
            )
            return
            
        if not self._validate_date(hire_date):
            messagebox.showerror(
                "Lỗi",
                "Ngày vào làm không hợp lệ! Định dạng: YYYY-MM-DD",
                parent=self.dialog
            )
            return
        
        # Validate phone (optional)
        if phone and not self._validate_phone(phone):
            messagebox.showerror(
                "Lỗi",
                "Số điện thoại không hợp lệ!",
                parent=self.dialog
            )
            return
        
        # Tạo data dict
        employee_data = {
            'employee_code': employee_code,
            'first_name': first_name,
            'last_name': last_name,
            'gender': self.gender_var.get(),
            'date_of_birth': dob,
            'email': email,
            'phone_number': phone,
            'address': address,
            'hire_date': hire_date,
            'status': self.status_combo.get(),
        }
        
        # Map position_id từ combo selection
        selected_position_display = self.position_combo.get()
        position_id = None
        
        # Tìm position_id từ display text
        for pid, display_text in self.positions_map.items():
            if display_text == selected_position_display:
                position_id = pid
                break
        
        # Nếu không tìm thấy trong map, thử fallback
        if position_id is None:
            print(f"⚠️ Không tìm thấy position_id cho: {selected_position_display}")
            # Fallback: lấy position đầu tiên hoặc mặc định
            if self.positions_map:
                position_id = list(self.positions_map.keys())[0]
            else:
                position_id = 1  # Default fallback
        
        employee_data['position_id'] = position_id
        
        # Thêm các trường khác tùy theo mode
        if self.mode == "add":
            employee_data['department_id'] = self.auth_controller.current_user_data.get('department_id')
            employee_data['manager_id'] = self.auth_controller.current_user_data.get('employee_id')
        elif self.mode == "edit":
            employee_data['employee_id'] = self.employee_data.get('employee_id')
            # Giữ nguyên department_id và manager_id
        
        # Hiển thị loading
        loading = LoadingOverlay(self.dialog, message="Đang lưu thông tin...")
        loading.show()
        
        # Xử lý sau 200ms để UI render
        self.dialog.after(200, lambda: self._process_save(employee_data, loading))
    
    def _process_save(self, employee_data: dict, loading: LoadingOverlay):
        """Xử lý lưu dữ liệu thực tế"""
        try:
            if self.mode == "add":
                message = self.employee_controller.add_employee(employee_data)
            elif self.mode == "edit":
                message = self.employee_controller.update_employee(employee_data)
            else:
                loading.hide()
                return
            
            # Cập nhật loading message
            loading.update_message("Lưu thành công!")
            
            # Delay 1000ms (1 giây) để hiển thị success
            self.dialog.after(1000, lambda: self._complete_save(loading, message))
            
        except Exception as e:
            loading.hide()
            messagebox.showerror(
                "Lỗi",
                f"Không thể lưu thông tin:\n{str(e)}",
                parent=self.dialog
            )
    
    def _complete_save(self, loading: LoadingOverlay, message: str):
        """Hoàn tất quá trình lưu"""
        loading.hide()
        messagebox.showinfo("Thành công", message, parent=self.dialog)
        
        # Gọi callback để refresh data
        if self.on_success:
            self.on_success()
        
        # Đóng dialog
        self.dialog.destroy()

