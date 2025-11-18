"""
Employee Form Dialog
Dialog để thêm/sửa/xem thông tin nhân viên
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable
import re

class EmployeeFormDialog(ctk.CTkToplevel):
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
        super().__init__(parent)
        
        self.parent = parent
        self.employee_controller = employee_controller
        self.auth_controller = auth_controller
        self.mode = mode
        self.employee_data = employee_data or {}
        self.on_success = on_success
        
        # DEBUG: Print employee data
        print(f"\n{'='*60}")
        print(f"📋 EmployeeFormDialog initialized with mode: {mode}")
        print(f"📋 Employee data received: {self.employee_data}")
        print(f"{'='*60}\n")
        
        # Cấu hình cửa sổ
        self._setup_window()
        
        # Set protocol để bắt sự kiện đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Force window update để đảm bảo sẵn sàng
        self.update_idletasks()
        
        # CRITICAL: Delay UI creation 500ms để CTkToplevel được thiết lập HOÀN TOÀN
        # CustomTkinter 5.2.2 + Python 3.13 cần thời gian dài hơn để khởi tạo font system
        self.after(500, self._delayed_init)
        
    def _setup_window(self):
        """Cấu hình cửa sổ dialog"""
        titles = {
            "add": "Thêm nhân viên mới",
            "edit": "Chỉnh sửa thông tin nhân viên",
            "view": "Xem thông tin nhân viên"
        }
        
        self.title(titles.get(self.mode, "Nhân viên"))
        self.geometry("600x750")
        self.resizable(False, False)
        
        # Đặt dialog là con của parent
        if self.parent:
            self.transient(self.parent)
            
        # Center dialog
        self.update_idletasks()
        try:
            # Cố gắng lấy vị trí tương đối so với cửa sổ cha
            x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (600 // 2)
            y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (750 // 2)
            self.geometry(f"+{x}+{y}")
        except:
            # Fallback nếu không lấy được
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = (screen_width - 600) // 2
            y = (screen_height - 750) // 2
            self.geometry(f"+{x}+{y}")
    
    def _delayed_init(self):
        """Khởi tạo UI sau khi dialog đã sẵn sàng (tránh lỗi font)"""
        # Kiểm tra window còn tồn tại không
        try:
            if not self.winfo_exists():
                print("Window không còn tồn tại, bỏ qua _delayed_init")
                return
        except:
            print("Không thể kiểm tra window, bỏ qua _delayed_init")
            return
            
        try:
            # Tạo UI
            self._create_ui()
            
            # Modal: Chặn tương tác với cửa sổ chính
            self.grab_set()
            self.focus_set()
        except Exception as e:
            print(f"ERROR in _delayed_init: {e}")
            import traceback
            traceback.print_exc()
            self._on_close()
        
    def _create_ui(self):
        """Tạo giao diện form nhập liệu SỬ DỤNG CTkScrollableFrame"""
        # Kiểm tra window còn tồn tại
        try:
            if not self.winfo_exists():
                print("Window không tồn tại, không thể tạo UI")
                return
        except:
            print("Lỗi kiểm tra window existence")
            return
            
        try:
            # SỬ DỤNG CTkScrollableFrame - TỰ ĐỘNG XỬ LÝ SCROLL
            self.form_container = ctk.CTkScrollableFrame(
                self,
                fg_color="transparent"
            )
            self.form_container.pack(fill="both", expand=True, padx=20, pady=20)

            # Tạo các trường nhập liệu
            self._create_form_fields()

            # Nút hành động
            self._create_action_buttons()

        except Exception as e:
            print(f"ERROR in _create_ui: {e}")
            import traceback
            traceback.print_exc()

    def _create_form_fields(self):
        """Tạo các trường nhập liệu"""
        is_readonly = self.mode == "view"
        
        # Hàm helper để tạo label + entry nhanh
        # CRITICAL: Dùng tk.Label thay vì CTkLabel để tránh lỗi font
        def create_entry_field(label, key, placeholder="", required=False):
            label_text = f"{label}:{' *' if required else ''}"
            
            # SỬ DỤNG tk.Label thay vì ctk.CTkLabel
            label_widget = tk.Label(
                self.form_container,
                text=label_text,
                anchor="w",
                bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]),
                fg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
                font=("Arial", 12)
            )
            label_widget.pack(fill="x", pady=(10, 5), padx=5)
            
            default_value = self.employee_data.get(key, "")
            
            # DEBUG: Print field values
            print(f"  Field '{key}': '{default_value}'")
            
            # CRITICAL: Truyền font tuple để tránh CTkFont() auto-creation
            # IMPORTANT: Insert value BEFORE setting disabled state
            entry = ctk.CTkEntry(
                self.form_container,
                placeholder_text=placeholder,
                font=("Arial", 12)
            )
            
            # Insert value first
            if default_value:
                entry.insert(0, str(default_value))
            
            # Then set state to disabled if in view mode
            if is_readonly:
                entry.configure(state="disabled")
                
            entry.pack(fill="x", pady=(0, 10), padx=5)
            # Lưu reference
            setattr(self, f"{key}_entry", entry)

        # 1. Mã nhân viên
        create_entry_field("Mã nhân viên", "employee_code", "VD: NV001", required=True)
        
        # 2. Họ & Tên
        create_entry_field("Họ", "last_name", "Nguyễn", required=True)
        create_entry_field("Tên", "first_name", "Văn A", required=True)
        
        # 3. Giới tính (Radio Buttons)
        tk.Label(
            self.form_container,
            text="Giới tính:",
            anchor="w",
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]),
            fg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            font=("Arial", 12)
        ).pack(fill="x", pady=(10, 5), padx=5)
        
        self.gender_var = ctk.StringVar(master=self, value=self.employee_data.get('gender', 'Male'))
        gender_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        gender_frame.pack(fill="x", pady=(0, 10), padx=5)
        
        state = "disabled" if is_readonly else "normal"
        ctk.CTkRadioButton(gender_frame, text="Nam", variable=self.gender_var, value="Male", state=state, font=("Arial", 12)).pack(side="left", padx=10)
        ctk.CTkRadioButton(gender_frame, text="Nữ", variable=self.gender_var, value="Female", state=state, font=("Arial", 12)).pack(side="left", padx=10)
        ctk.CTkRadioButton(gender_frame, text="Khác", variable=self.gender_var, value="Other", state=state, font=("Arial", 12)).pack(side="left", padx=10)
        
        # 4. Các thông tin khác
        create_entry_field("Ngày sinh", "date_of_birth", "YYYY-MM-DD", required=True)
        create_entry_field("Email", "email", "email@example.com", required=True)
        create_entry_field("Số điện thoại", "phone_number", "090...")
        create_entry_field("Địa chỉ", "address", "...")
        create_entry_field("Ngày vào làm", "hire_date", "YYYY-MM-DD", required=True)
        
        # 5. Phòng ban (Combobox) - Load từ database
        tk.Label(
            self.form_container,
            text="Phòng ban: *",
            anchor="w",
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]),
            fg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            font=("Arial", 12)
        ).pack(fill="x", pady=(10, 5), padx=5)
        
        self._load_departments()  # Load dữ liệu phòng ban
        
        dept_names = [name for _, name in self.departments]
        print(f"📋 Department names for combobox: {dept_names}")
        
        self.department_combo = ctk.CTkComboBox(
            self.form_container,
            values=dept_names,
            command=self._on_department_change,
            font=("Arial", 12),
            dropdown_font=("Arial", 12)  # CRITICAL: Fix DropdownMenu font error
        )
        # Set giá trị mặc định
        current_dept = self.employee_data.get('department_name', '') or self.employee_data.get('department', '')
        print(f"🏢 Current department from employee_data: '{current_dept}'")
        if current_dept:
            self.department_combo.set(current_dept)
        elif self.departments:
            self.department_combo.set(self.departments[0][1])
            print(f"✅ Set default department: {self.departments[0][1]}")
        
        # Set state after setting value
        if is_readonly:
            self.department_combo.configure(state="disabled")
            
        self.department_combo.pack(fill="x", pady=(0, 10), padx=5)
        
        # 6. Chức vụ (Combobox) - Load dựa vào phòng ban đã chọn
        tk.Label(
            self.form_container,
            text="Chức vụ: *",
            anchor="w",
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]),
            fg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            font=("Arial", 12)
        ).pack(fill="x", pady=(10, 5), padx=5)
        
        self._load_positions()  # Load dữ liệu chức vụ dựa vào dept đã chọn
        self.position_combo = ctk.CTkComboBox(
            self.form_container,
            values=[name for _, name in self.positions],
            font=("Arial", 12),
            dropdown_font=("Arial", 12)  # CRITICAL: Fix DropdownMenu font error
        )
        current_pos = self.employee_data.get('position_title', '') or self.employee_data.get('position', '')
        if current_pos:
            self.position_combo.set(current_pos)
        elif self.positions:
            self.position_combo.set(self.positions[0][1])
        
        # Set state after setting value
        if is_readonly:
            self.position_combo.configure(state="disabled")
            
        self.position_combo.pack(fill="x", pady=(0, 10), padx=5)
        
        # 7. Trạng thái (Combobox)
        tk.Label(
            self.form_container,
            text="Trạng thái:",
            anchor="w",
            bg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"]),
            fg=self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"]),
            font=("Arial", 12)
        ).pack(fill="x", pady=(10, 5), padx=5)
        
        self.status_combo = ctk.CTkComboBox(
            self.form_container,
            values=["Probation", "Active", "Resigned"],
            font=("Arial", 12),
            dropdown_font=("Arial", 12)  # CRITICAL: Fix DropdownMenu font error
        )
        current_status = self.employee_data.get('employment_status', '') or self.employee_data.get('status', 'Active')
        self.status_combo.set(current_status)
        
        # Set state after setting value
        if is_readonly:
            self.status_combo.configure(state="disabled")
            
        self.status_combo.pack(fill="x", pady=(0, 10), padx=5)

    def _load_departments(self):
        """Load danh sách phòng ban từ database"""
        try:
            self.departments = self.employee_controller.get_all_departments_for_view()
            print(f"✅ Loaded {len(self.departments)} departments: {self.departments}")
        except Exception as e:
            print(f"❌ ERROR loading departments: {e}")
            import traceback
            traceback.print_exc()
            self.departments = []

    def _load_positions(self):
        """Load danh sách chức vụ dựa vào phòng ban đang chọn"""
        try:
            # Lấy department_id từ department đã chọn hoặc từ employee_data
            selected_dept_name = self.department_combo.get()
            
            # If combo is empty, try to get from employee_data directly
            if not selected_dept_name:
                selected_dept_name = self.employee_data.get('department_name', '') or self.employee_data.get('department', '')
            
            dept_id = None
            
            # Try to find dept_id from department name
            for did, dname in self.departments:
                if dname == selected_dept_name:
                    dept_id = did
                    break
            
            # If still no dept_id, try to get it directly from employee_data
            if not dept_id and self.employee_data.get('department_id'):
                dept_id = self.employee_data.get('department_id')
            
            print(f"🔍 Loading positions for dept: '{selected_dept_name}' (ID: {dept_id})")
            
            if dept_id:
                self.positions = self.employee_controller.get_positions_by_department_id_for_view(dept_id)
                print(f"✅ Loaded {len(self.positions)} positions: {self.positions}")
            else:
                print(f"⚠️ No dept_id found for '{selected_dept_name}'")
                self.positions = []
        except Exception as e:
            print(f"❌ ERROR loading positions: {e}")
            import traceback
            traceback.print_exc()
            self.positions = []

    def _on_department_change(self, selected_dept_name):
        """Callback khi thay đổi phòng ban - cập nhật danh sách chức vụ"""
        self._load_positions()
        # Cập nhật combobox chức vụ
        self.position_combo.configure(values=[name for _, name in self.positions])
        if self.positions:
            self.position_combo.set(self.positions[0][1])

    def _create_action_buttons(self):
        """Tạo các nút hành động"""
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        if self.mode != "view":
            save_btn = ctk.CTkButton(
                buttons_frame,
                text="💾 Lưu",
                command=self._save,
                fg_color="#27AE60",
                hover_color="#229954",
                width=150,
                height=40,
                font=("Arial", 12)
            )
            save_btn.pack(side="left", padx=(0, 10))
            
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="✕ Hủy",
                command=self._on_close,
                fg_color="#95A5A6",
                hover_color="#7F8C8D",
                width=150,
                height=40,
                font=("Arial", 12)
            )
            cancel_btn.pack(side="left")
        else:
            close_btn = ctk.CTkButton(
                buttons_frame,
                text="✕ Đóng",
                command=self._on_close,
                fg_color="#95A5A6",
                hover_color="#7F8C8D",
                width=150,
                height=40,
                font=("Arial", 12)
            )
            close_btn.pack(pady=10)
            
    def _validate_data(self, data):
        """Kiểm tra dữ liệu"""
        if not data["employee_code"] or not data["first_name"] or not data["last_name"]:
            return False, "Vui lòng nhập đầy đủ Mã NV và Họ Tên."
        # Thêm các validate khác (ngày tháng, email...) nếu cần
        return True, ""

    def _save(self):
        """Lưu dữ liệu"""
        try:
            # Thu thập dữ liệu
            data = {
                "employee_code": self.employee_code_entry.get().strip(),
                "first_name": self.first_name_entry.get().strip(),
                "last_name": self.last_name_entry.get().strip(),
                "gender": self.gender_var.get(),
                "date_of_birth": self.date_of_birth_entry.get().strip(),
                "email": self.email_entry.get().strip(),
                "phone_number": self.phone_number_entry.get().strip(),
                "address": self.address_entry.get().strip(),
                "hire_date": self.hire_date_entry.get().strip(),
                "status": self.status_combo.get()
            }
            
            # Validate
            is_valid, error_msg = self._validate_data(data)
            if not is_valid:
                messagebox.showerror("Lỗi", error_msg, parent=self)
                return

            # Lấy department_id và position_id từ combobox
            selected_dept_name = self.department_combo.get()
            dept_id = None
            for did, dname in self.departments:
                if dname == selected_dept_name:
                    dept_id = did
                    break
            
            selected_pos_name = self.position_combo.get()
            pos_id = None
            for pid, pname in self.positions:
                if pname == selected_pos_name:
                    pos_id = pid
                    break

            data['department_id'] = dept_id if dept_id else 1
            data['position_id'] = pos_id if pos_id else 1

            # Gọi Controller
            if self.mode == "add":
                message = self.employee_controller.add_employee(data)
            elif self.mode == "edit":
                message = self.employee_controller.update_employee(self.employee_data.get('id'), data)
            else:
                return

            messagebox.showinfo("Thành công", message, parent=self)
            
            # Refresh list bên ngoài
            if self.on_success:
                self.on_success()
            
            self._on_close()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {str(e)}", parent=self)
            print(f"Error saving: {e}")

    def _on_close(self):
        """Đóng dialog và giải phóng grab một cách an toàn"""
        try:
            # Giải phóng grab nếu có
            self.grab_release()
        except:
            pass
            
        try:
            # Giải phóng grab nếu có
            self.grab_release()
        except:
            pass
        
        try:
            # Withdraw trước để ẩn window
            self.withdraw()
        except:
            pass
        
        # Delay destroy để tránh lỗi AttributeError với widgets chưa init xong
        try:
            self.after(50, self._safe_destroy)
        except:
            # Nếu after fail, destroy trực tiếp
            self._safe_destroy()
    
    def _safe_destroy(self):
        """Destroy an toàn, bỏ qua mọi lỗi"""
        try:
            self.destroy()
        except Exception as e:
            # Bỏ qua tất cả lỗi khi destroy (AttributeError, etc.)
            print(f"Warning: Error during destroy (ignored): {e}")
            # Force quit bằng cách destroy parent reference
            try:
                import tkinter
                tkinter.Toplevel.destroy(self)
            except:
                pass