import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
# SỬA: Không import database ở đây

# SỬA: Đổi tên class thành 'MainWindow' và kế thừa từ ctk.CTk
class MainWindow(ctk.CTk):
    
    # SỬA: Hàm __init__ nhận 'controller' và 'auth_controller'
    def __init__(self, controller, auth_controller=None): 
        super().__init__() # Khởi tạo ctk.CTk
        self.controller = controller # LƯU LẠI "BỘ NÃO"
        self.auth_controller = auth_controller # LƯU AUTH CONTROLLER

        # --- CẬP NHẬT UI/UX HIỆN ĐẠI ---
        self.title("Employee Management System")
        self.geometry("1280x800")  # Đặt kích thước cửa sổ
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Cấu hình grid layout cho cửa sổ chính ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Tạo các thành phần giao diện ---
        self.create_header()
        self.create_left_panel()
        self.create_right_panel()

        # Khởi tạo positions cho department mặc định
        self.on_department_changed("Marketing")

        # Áp dụng quyền cho các button
        self.apply_permissions()

        # Hiển thị giữa màn hình
        self._center_window()

        # Tải dữ liệu lần đầu
        self.fetch_data()

    def create_header(self):
        """Tạo khung header màu tím ở trên cùng"""
        header_frame = ctk.CTkFrame(self, height=80, fg_color="#5D3FD3", corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_frame.pack_propagate(False)

        # Container để chứa title và role
        header_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_container.pack(fill="both", expand=True, padx=20)

        title_label = ctk.CTkLabel(
            header_container, 
            text="Employee Management System", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(15, 2), anchor="w") 

        # Hiển thị role của user
        role_text = "Manage your team efficiently"
        if self.auth_controller:
            current_role = self.auth_controller.get_current_role()
            current_user = self.auth_controller.get_current_user()
            username = current_user.get('username', 'Unknown') if current_user else 'Unknown'
            role_text = f"Logged in as: {username} ({current_role})"
        
        subtitle_label = ctk.CTkLabel(
            header_container, 
            text=role_text, 
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 15), anchor="w")

    def create_left_panel(self):
        """Tạo khung nhập liệu bên trái"""
        # Frame chứa - cố định width
        left_container = ctk.CTkFrame(self, width=320, fg_color="#2B2B2B")
        left_container.grid(row=1, column=0, sticky="nsw", padx=(10, 5), pady=10)
        left_container.grid_propagate(False)
        left_container.grid_rowconfigure(0, weight=1)
        left_container.grid_columnconfigure(0, weight=1)
        
        # Scrollable frame bên trong
        left_panel = ctk.CTkScrollableFrame(left_container, fg_color="#2B2B2B")
        left_panel.grid(row=0, column=0, sticky="nsew")

        details_label = ctk.CTkLabel(
            left_panel, 
            text="Employee Details", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        details_label.pack(pady=20, padx=20, anchor="w")

        # --- Form Fields ---
        # Employee Code
        id_label = ctk.CTkLabel(left_panel, text="Employee Code", anchor="w")
        id_label.pack(fill="x", padx=20, pady=(0, 5))
        self.txt_id = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter employee code"
        )
        self.txt_id.pack(fill="x", padx=20, pady=(0, 15))

        # Name
        name_label = ctk.CTkLabel(left_panel, text="Name", anchor="w")
        name_label.pack(fill="x", padx=20, pady=(0, 5))
        self.txt_name = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter name"
        )
        self.txt_name.pack(fill="x", padx=20, pady=(0, 15))

        # Gender
        gender_label = ctk.CTkLabel(left_panel, text="Gender", anchor="w")
        gender_label.pack(fill="x", padx=20, pady=(0, 5))
        self.combo_gender = ctk.CTkComboBox(
            left_panel, 
            values=["Nam", "Nữ", "Khác"]
        )
        self.combo_gender.set("Nam")
        self.combo_gender.pack(fill="x", padx=20, pady=(0, 15))

        # Email
        email_label = ctk.CTkLabel(left_panel, text="Email", anchor="w")
        email_label.pack(fill="x", padx=20, pady=(0, 5))
        self.txt_email = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter email"
        )
        self.txt_email.pack(fill="x", padx=20, pady=(0, 15))

        # Phone
        phone_label = ctk.CTkLabel(left_panel, text="Phone", anchor="w")
        phone_label.pack(fill="x", padx=20, pady=(0, 5))
        self.txt_phone = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter phone"
        )
        self.txt_phone.pack(fill="x", padx=20, pady=(0, 15))

        # Address
        address_label = ctk.CTkLabel(left_panel, text="Address", anchor="w")
        address_label.pack(fill="x", padx=20, pady=(0, 5))
        self.txt_address = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter address"
        )
        self.txt_address.pack(fill="x", padx=20, pady=(0, 15))

        # Department - ComboBox với 4 phòng ban
        department_label = ctk.CTkLabel(left_panel, text="Department", anchor="w")
        department_label.pack(fill="x", padx=20, pady=(0, 5))
        self.combo_department = ctk.CTkComboBox(
            left_panel,
            values=["Marketing", "IT", "Finance", "HR"],
            command=self.on_department_changed  # Event khi đổi department
        )
        self.combo_department.set("Marketing")  # Giá trị mặc định
        self.combo_department.pack(fill="x", padx=20, pady=(0, 15))

        # Position - ComboBox liên kết với Department
        position_label = ctk.CTkLabel(left_panel, text="Position", anchor="w")
        position_label.pack(fill="x", padx=20, pady=(0, 5))
        self.combo_position = ctk.CTkComboBox(
            left_panel,
            values=[],  # Sẽ được cập nhật động
            command=self.on_position_changed  # Event khi đổi position
        )
        self.combo_position.pack(fill="x", padx=20, pady=(0, 15))

        # Buttons frame
        buttons_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Add button - LƯU VÀO INSTANCE VARIABLE
        self.add_button = ctk.CTkButton(
            buttons_frame,
            text="Add Employee",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28A745",
            hover_color="#218838",
            command=self.add_employee
        )
        self.add_button.pack(fill="x", pady=(0, 10))

        # Buttons row - Grid layout để đều nhau
        button_row = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        button_row.pack(fill="x", pady=(0, 10))
        
        # Cấu hình 3 cột đều nhau
        button_row.grid_columnconfigure(0, weight=1, uniform="button")
        button_row.grid_columnconfigure(1, weight=1, uniform="button")
        button_row.grid_columnconfigure(2, weight=1, uniform="button")
        
        self.update_button = ctk.CTkButton(
            button_row,
            text="Update",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.update_employee
        )
        self.update_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.delete_button = ctk.CTkButton(
            button_row,
            text="Delete",
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.delete_employee
        )
        self.delete_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        clear_button = ctk.CTkButton(
            button_row,
            text="Clear",
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=self.clear_form
        )
        clear_button.grid(row=0, column=2, padx=5, sticky="ew")

    def create_right_panel(self):
        """Tạo khung hiển thị dữ liệu bên phải"""
        right_panel = ctk.CTkFrame(self, fg_color="#343638")
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # --- Search Bar ---
        self.create_search_bar(right_panel)

        # --- Table ---
        self.create_table(right_panel)

    def create_search_bar(self, parent):
        """Tạo thanh tìm kiếm và lọc"""
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.combo_search = ctk.CTkComboBox(
            search_frame, 
            values=["employee_code", "first_name", "phone_number", "email"],
            width=150
        )
        self.combo_search.set("employee_code")
        self.combo_search.pack(side="left", padx=(0, 10))

        self.txt_search = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Search..."
        )
        self.txt_search.pack(side="left", fill="x", expand=True, padx=10)

        search_button = ctk.CTkButton(
            search_frame, 
            text="Search", 
            width=100, 
            fg_color="#5D3FD3", 
            hover_color="#4A2F9D",
            command=self.search_data
        )
        search_button.pack(side="left", padx=10)

        show_all_button = ctk.CTkButton(
            search_frame, 
            text="Show All", 
            width=100, 
            fg_color="#5D3FD3", 
            hover_color="#4A2F9D",
            command=self.fetch_data
        )
        show_all_button.pack(side="left", padx=(0, 10))

    def create_table(self, parent):
        """Tạo bảng dữ liệu với Treeview"""
        table_frame = tk.Frame(parent, bg="#343638")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        # Treeview - Thêm cột Department
        self.tree_columns = ('ID', 'Code', 'Full Name', 'Email', 'Phone', 'Gender', 'Address', 'Department', 'Position')
        self.tree = ttk.Treeview(table_frame, columns=self.tree_columns, 
                                 xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.grid(row=1, column=0, sticky="ew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Code', text='Emp. Code')
        self.tree.heading('Full Name', text='Full Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Address', text='Address')
        self.tree.heading('Department', text='Department')
        self.tree.heading('Position', text='Position')
        self.tree['show'] = 'headings'
        
        self.tree.column('ID', width=50)
        self.tree.column('Code', width=100)
        self.tree.column('Full Name', width=150)
        self.tree.column('Email', width=180)
        self.tree.column('Phone', width=120)
        self.tree.column('Gender', width=80)
        self.tree.column('Address', width=200)
        self.tree.column('Department', width=100)
        self.tree.column('Position', width=150)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<ButtonRelease-1>", self.get_cursor)

    # --- CÁC HÀM ĐÃ ĐƯỢC "NỐI" LẠI (REWIRED) ---

    def fetch_data(self):
        """SỬA: Gọi Controller để lấy dữ liệu."""
        self.tree.delete(*self.tree.get_children())
        try:
            employee_list = self.controller.get_all_employees_for_view()
            if employee_list:
                for item in employee_list:
                    self.tree.insert("", tk.END, values=item)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def add_employee(self):
        """SỬA: Thu thập dữ liệu và gọi Controller."""
        # 1. Lấy department_id và position_id
        department_name = self.combo_department.get()
        department_id = self.get_department_id(department_name)
        
        position_title = self.combo_position.get()
        position_id = self.get_position_id(position_title)
        
        # 2. Thu thập dữ liệu thô từ Form
        data = {
            'employee_code': self.txt_id.get(),
            'first_name': self.txt_name.get(), # Controller sẽ tự tách tên
            'gender': self.combo_gender.get(),
            'email': self.txt_email.get(),
            'phone_number': self.txt_phone.get(),
            'address': self.txt_address.get(),
            'department_id': department_id,
            'position_id': position_id,
            # Các trường này DB của bạn yêu cầu (từ schema)
            'date_of_birth': '1990-01-01', # Tạm thời - Cần thêm vào form
            'hire_date': '2025-01-01', # Tạm thời - Cần thêm vào form
            'status': 'Đang làm việc'
        }

        # 3. Gọi "bộ não" (Controller) để xử lý
        try:
            result_message = self.controller.add_employee(data)
            messagebox.showinfo("Thông báo", result_message)
            self.fetch_data() # Yêu cầu tải lại bảng
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm nhân viên: {e}")

    def update_employee(self):
        """SỬA: Thu thập dữ liệu và gọi Controller."""
        employee_code = self.txt_id.get()
        if not employee_code:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để cập nhật")
            return
        
        # Lấy department_id và position_id
        department_name = self.combo_department.get()
        department_id = self.get_department_id(department_name)
        
        position_title = self.combo_position.get()
        position_id = self.get_position_id(position_title)
            
        data = {
            'first_name': self.txt_name.get(), # Controller sẽ tự tách tên
            'gender': self.combo_gender.get(),
            'email': self.txt_email.get(),
            'phone_number': self.txt_phone.get(),
            'address': self.txt_address.get(),
            'department_id': department_id,
            'position_id': position_id,
        }
        
        try:
            result_message = self.controller.update_employee(employee_code, data)
            messagebox.showinfo("Thông báo", result_message)
            self.fetch_data()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {e}")

    def delete_employee(self):
        """SỬA: Lấy ID và gọi Controller."""
        employee_code = self.txt_id.get()
        if not employee_code:
            messagebox.showwarning("Lỗi", "Vui lòng chọn nhân viên để xóa")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên (Code: {employee_code})?"):
            try:
                result_message = self.controller.delete_employee(employee_code)
                messagebox.showinfo("Thông báo", result_message)
                self.fetch_data()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa: {e}")

    def search_data(self):
        """SỬA: Gọi Controller để tìm kiếm."""
        search_by = self.combo_search.get()
        search_text = self.txt_search.get()
        
        if not search_by or not search_text:
            messagebox.showwarning("Lỗi", "Vui lòng chọn điều kiện và nhập từ khóa tìm kiếm")
            return

        try:
            results = self.controller.search_employees(search_by, search_text)
            self.tree.delete(*self.tree.get_children())
            if results:
                for item in results:
                    self.tree.insert("", tk.END, values=item)
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {e}")

    # --- CÁC HÀM LOGIC CỦA VIEW (GIỮ NGUYÊN) ---
    
    def get_cursor(self, event):
        """GIỮ NGUYÊN: Hàm này là logic của View."""
        try:
            cursor_row = self.tree.focus()
            content = self.tree.item(cursor_row)
            row = content['values']
            
            self.txt_id.delete(0, tk.END)
            self.txt_id.insert(0, row[1]) # Cột 1 là 'Code'
            self.txt_name.delete(0, tk.END)
            self.txt_name.insert(0, row[2]) # Cột 2 là 'Full Name'
            self.combo_gender.set(row[5]) # Cột 5 là 'Gender'
            self.txt_email.delete(0, tk.END)
            self.txt_email.insert(0, row[3]) # Cột 3 là 'Email'
            self.txt_phone.delete(0, tk.END)
            self.txt_phone.insert(0, row[4]) # Cột 4 là 'Phone'
            self.txt_address.delete(0, tk.END)
            self.txt_address.insert(0, row[6]) # Cột 6 là 'Address'
            
            # Load department (Cột 7)
            if len(row) > 7 and row[7]:
                dept_name = row[7]
                self.combo_department.set(dept_name)
                # Cập nhật positions cho department này
                self.on_department_changed(dept_name)
                
                # Load position (Cột 8)
                if len(row) > 8 and row[8]:
                    self.combo_position.set(row[8])
            else:
                self.combo_department.set("Marketing")
                self.on_department_changed("Marketing")
        except (IndexError, tk.TclError):
            pass

    def clear_form(self):
        """GIỮ NGUYÊN: Hàm này là logic của View."""
        self.txt_id.delete(0, "end")
        self.txt_name.delete(0, "end")
        self.combo_gender.set('')
        self.txt_email.delete(0, "end")
        self.txt_phone.delete(0, "end")
        self.txt_address.delete(0, "end")
        self.combo_department.set("Marketing")  # Reset về giá trị mặc định
        self.on_department_changed("Marketing")  # Cập nhật positions cho Marketing

    def _center_window(self) -> None:
        """Center this window on the primary screen without changing its size."""
        self.update_idletasks()
        
        # Lấy kích thước đã thiết lập từ geometry ban đầu
        try:
            geom = self.geometry().split('+')[0]
            w_str, h_str = geom.split('x')
            w, h = int(w_str), int(h_str)
        except Exception:
            # Fallback nếu không parse được
            w, h = 1280, 720

        # Tính toán vị trí giữa màn hình
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        
        # Chỉ thay đổi vị trí, giữ nguyên kích thước
        self.geometry(f"+{x}+{y}")
    
    def get_department_id(self, department_name):
        """Chuyển đổi tên department thành department_id."""
        department_mapping = {
            'Marketing': 1,
            'IT': 2,
            'Finance': 3,
            'HR': 4
        }
        return department_mapping.get(department_name, 1)
    
    def get_department_name(self, department_id):
        """Chuyển đổi department_id thành tên department."""
        department_mapping = {
            1: 'Marketing',
            2: 'IT',
            3: 'Finance',
            4: 'HR'
        }
        return department_mapping.get(department_id, 'Marketing')
    
    def get_positions_by_department(self, department_name):
        """
        Lấy danh sách positions theo department.
        """
        positions_mapping = {
            'Marketing': ['Marketing Manager', 'Content Creator', 'Social Media Specialist'],
            'IT': ['IT Manager', 'Software Engineer', 'Web Developer', 'Tester'],
            'Finance': ['Finance Manager', 'Accountant', 'Financial Analyst', 'Auditor'],
            'HR': ['HR Manager', 'Recruiter', 'Training Specialist']
        }
        return positions_mapping.get(department_name, [])
    
    def get_department_by_position(self, position_title):
        """
        Tìm department dựa trên position.
        Trả về tên department.
        """
        position_to_dept = {
            # Marketing positions
            'Marketing Manager': 'Marketing',
            'Content Creator': 'Marketing',
            'Social Media Specialist': 'Marketing',
            # IT positions
            'IT Manager': 'IT',
            'Software Engineer': 'IT',
            'Web Developer': 'IT',
            'Tester': 'IT',
            # Finance positions
            'Finance Manager': 'Finance',
            'Accountant': 'Finance',
            'Financial Analyst': 'Finance',
            'Auditor': 'Finance',
            # HR positions
            'HR Manager': 'HR',
            'Recruiter': 'HR',
            'Training Specialist': 'HR'
        }
        return position_to_dept.get(position_title, 'Marketing')
    
    def get_position_id(self, position_title):
        """Chuyển đổi tên position thành position_id."""
        position_mapping = {
            # Marketing (1-3)
            'Marketing Manager': 1,
            'Content Creator': 2,
            'Social Media Specialist': 3,
            # IT (4-6, 13)
            'Software Engineer': 4,
            'Web Developer': 5,
            'Tester': 6,
            'IT Manager': 13,
            # Finance (7-9, 14)
            'Accountant': 7,
            'Financial Analyst': 8,
            'Auditor': 9,
            'Finance Manager': 14,
            # HR (10-12)
            'HR Manager': 10,
            'Recruiter': 11,
            'Training Specialist': 12
        }
        return position_mapping.get(position_title, 1)
    
    def get_position_name(self, position_id):
        """Chuyển đổi position_id thành tên position."""
        position_mapping = {
            1: 'Marketing Manager',
            2: 'Content Creator',
            3: 'Social Media Specialist',
            4: 'Software Engineer',
            5: 'Web Developer',
            6: 'Tester',
            7: 'Accountant',
            8: 'Financial Analyst',
            9: 'Auditor',
            10: 'HR Manager',
            11: 'Recruiter',
            12: 'Training Specialist',
            13: 'IT Manager',
            14: 'Finance Manager'
        }
        return position_mapping.get(position_id, 'Marketing Manager')
    
    def on_department_changed(self, selected_dept):
        """
        Event handler: Khi user chọn department, 
        cập nhật danh sách positions tương ứng.
        """
        positions = self.get_positions_by_department(selected_dept)
        self.combo_position.configure(values=positions)
        if positions:
            self.combo_position.set(positions[0])  # Set position đầu tiên
    
    def on_position_changed(self, selected_position):
        """
        Event handler: Khi user chọn position,
        tự động cập nhật department tương ứng.
        """
        department = self.get_department_by_position(selected_position)
        self.combo_department.set(department)
    
    def apply_permissions(self):
        """Áp dụng quyền dựa trên role của user"""
        if not self.auth_controller:
            return
        
        # Lấy thông tin role và quyền
        current_role = self.auth_controller.get_current_role()
        
        # Disable các button dựa trên quyền
        if not self.auth_controller.can_add_employees():
            self.add_button.configure(state="disabled")
        
        if not self.auth_controller.can_edit_employees():
            self.update_button.configure(state="disabled")
        
        if not self.auth_controller.can_delete_employees():
            self.delete_button.configure(state="disabled")
        
        # Cập nhật header để hiển thị role
        print(f"🔐 Đã áp dụng quyền cho role: {current_role}")