import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# Giả sử controller của bạn ở đây, nếu không, hãy import đúng đường dẫn
# from app.controllers.employee_controller import EmployeeController 

class MainWindow(tk.Tk):
    def __init__(self, controller): # Nhận controller từ bên ngoài
        super().__init__()
        self.controller = controller

        self.title("Hệ thống Quản lý Nhân sự (Employee Management System)")
        self.geometry("1200x700+50+50") # Kích thước cửa sổ
        
        # --- Cấu hình Style để trông hiện đại ---
        self._setup_styles()
        
        # --- Tạo các thành phần giao diện ---
        self._create_widgets()
        
        # Tải dữ liệu nhân viên từ database ngay khi khởi động
        self.load_all_employees()

    def _setup_styles(self):
        """Thiết lập Tùy chỉnh Giao diện (Theme) cho ứng dụng."""
        self.configure(bg="#2E2E2E") # Màu nền chính
        
        style = ttk.Style(self)
        style.theme_use('clam') # Sử dụng theme 'clam' vì nó dễ tùy chỉnh nhất

        # --- Định nghĩa màu sắc ---
        BG_COLOR = "#2E2E2E"       # Nền tối
        FG_COLOR = "#FFFFFF"       # Chữ trắng
        LIGHT_BG = "#3C3C3C"     # Nền cho Entry, Treeview
        ACCENT_COLOR = "#4A4AFF"   # Màu nhấn (Xanh/Tím)
        RED_COLOR = "#FF5555"      # Màu nút Xóa

        # --- Cấu hình chung ---
        style.configure('.', 
                        background=BG_COLOR, 
                        foreground=FG_COLOR, 
                        font=('Arial', 11))
        
        # --- Cấu hình riêng cho từng Widget ---
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR)
        
        # Nút bấm
        style.configure('TButton', 
                        background=ACCENT_COLOR, 
                        foreground=FG_COLOR, 
                        font=('Arial', 11, 'bold'), 
                        borderwidth=0,
                        padding=(10, 5))
        style.map('TButton', background=[('active', '#5A5AFF')]) # Khi hover/click
        
        # Nút bấm màu đỏ (cho Xóa)
        style.configure('Red.TButton', background=RED_COLOR)
        style.map('Red.TButton', background=[('active', '#FF6565')])

        # Ô nhập liệu
        style.configure('TEntry', 
                        fieldbackground=LIGHT_BG, 
                        foreground=FG_COLOR, 
                        borderwidth=1, 
                        insertcolor=FG_COLOR) # Màu con trỏ
        
        # Combobox (Hộp chọn)
        style.configure('TCombobox', 
                        fieldbackground=LIGHT_BG, 
                        foreground=FG_COLOR, 
                        borderwidth=1)
        
        # Bảng dữ liệu (Treeview)
        style.configure("Treeview", 
                        background=LIGHT_BG, 
                        foreground=FG_COLOR, 
                        fieldbackground=LIGHT_BG, 
                        rowheight=25)
        style.map("Treeview", background=[('selected', ACCENT_COLOR)]) # Màu khi chọn 1 dòng
        
        # Tiêu đề bảng
        style.configure("Treeview.Heading", 
                        background=BG_COLOR, 
                        foreground=FG_COLOR, 
                        font=('Arial', 12, 'bold'))
        style.map("Treeview.Heading", background=[('active', LIGHT_BG)])

    def _create_widgets(self):
        """Tạo tất cả các thành phần con của cửa sổ chính."""
        
        # --- 1. Header Frame ---
        # Chúng ta mô phỏng header bằng một Frame và các Label
        header_frame = ttk.Frame(self, style='TFrame')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(header_frame, text="Employee Management System", 
                  font=("Arial", 24, "bold")).pack(anchor='w')
        ttk.Label(header_frame, text="Manage your team efficiently", 
                  font=("Arial", 12)).pack(anchor='w')

        # --- 2. Main Frame (Chia làm 2 cột) ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Cấu hình grid: cột 1 (data) sẽ rộng gấp 3 cột 0 (form)
        main_frame.grid_columnconfigure(1, weight=3)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- 3. Form Nhập liệu (Bên trái) ---
        self._create_form_panel(main_frame)
        
        # --- 4. Bảng Dữ liệu (Bên phải) ---
        self._create_data_panel(main_frame)

    def _create_form_panel(self, parent):
        """Tạo khung nhập liệu bên tay trái."""
        form_frame = ttk.Frame(parent, padding=10)
        form_frame.grid(row=0, column=0, sticky="nswe", padx=(0, 10))
        form_frame.grid_rowconfigure(7, weight=1) # Đẩy các nút bấm xuống dưới

        ttk.Label(form_frame, text="Employee Details", 
                  font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky='w')

        # Các nhãn và ô nhập liệu
        labels = ["ID", "Name", "Phone", "Role", "Gender", "Email", "Salary"]
        self.entries = {} # Dictionary để lưu các widget nhập liệu
        
        for i, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(row=i+1, column=0, sticky='w', padx=5, pady=8)
            
            if label_text in ["Role", "Gender"]:
                # Dùng Combobox cho Role và Gender
                widget = ttk.Combobox(form_frame, state='readonly', width=25)
                if label_text == "Role":
                    # TODO: Nên lấy danh sách Role từ database
                    widget['values'] = ('Software Engineer', 'UX/UI Designer', 'Data Scientist', 'Network Engineer')
                else:
                    widget['values'] = ('Male', 'Female', 'Other')
            else:
                # Dùng Entry cho các trường khác
                widget = ttk.Entry(form_frame, width=27)
                
            widget.grid(row=i+1, column=1, sticky='we', padx=5, pady=8)
            self.entries[label_text] = widget

        # ID không cho phép chỉnh sửa
        self.entries["ID"].config(state='readonly', foreground="#AAAAAA")

        # Khung chứa các nút bấm (Add, Update, Delete, Clear)
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=7, column=0, columnspan=2, sticky='sew', pady=10)
        # Cấu hình 4 cột bằng nhau
        button_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        ttk.Button(button_frame, text="Add", command=self._add_employee).grid(row=0, column=0, sticky='ew', padx=2)
        ttk.Button(button_frame, text="Update", command=self._update_employee).grid(row=0, column=1, sticky='ew', padx=2)
        ttk.Button(button_frame, text="Delete", style='Red.TButton', command=self._delete_employee).grid(row=0, column=2, sticky='ew', padx=2)
        ttk.Button(button_frame, text="Clear", command=self._clear_form).grid(row=0, column=3, sticky='ew', padx=2)


    def _create_data_panel(self, parent):
        """Tạo khung dữ liệu (bảng) bên tay phải."""
        data_frame = ttk.Frame(parent, padding=10)
        data_frame.grid(row=0, column=1, sticky="nswe")
        data_frame.grid_rowconfigure(1, weight=1) # Cho bảng Treeview co giãn
        data_frame.grid_columnconfigure(0, weight=1)

        # Thanh tìm kiếm
        search_frame = ttk.Frame(data_frame)
        search_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1)

        self.search_by_combo = ttk.Combobox(search_frame, state='readonly', values=['All', 'Name', 'Role', 'ID'])
        self.search_by_combo.current(0)
        self.search_by_combo.grid(row=0, column=0, padx=(0,5))
        
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, sticky='we', padx=5)
        
        ttk.Button(search_frame, text="Search", command=self._search_data).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Show All", command=self.load_all_employees).grid(row=0, column=3, padx=5)

        # Khung chứa bảng và thanh cuộn
        tree_frame = ttk.Frame(data_frame)
        tree_frame.grid(row=1, column=0, sticky='nswe')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Bảng dữ liệu (Treeview)
        columns = ('ID', 'Name', 'Phone', 'Role', 'Gender', 'Email', 'Salary')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Định nghĩa các cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        
        # Gán sự kiện khi click vào một dòng
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
        
        # Thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Vị trí của bảng và thanh cuộn
        self.tree.grid(row=0, column=0, sticky='nswe')
        scrollbar.grid(row=0, column=1, sticky='ns')

    # --- Các hàm xử lý sự kiện ---

    def load_all_employees(self):
        """Yêu cầu controller lấy dữ liệu và hiển thị lên bảng."""
        try:
            # Xóa dữ liệu cũ trên bảng
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Lấy dữ liệu mới từ controller
            employees = self.controller.get_all_employees()
            
            # Chèn dữ liệu mới vào bảng
            for emp in employees:
                # Chuyển đổi dữ liệu employee object thành tuple cho hiển thị
                display_data = (
                    emp.id if hasattr(emp, 'id') else '',
                    f"{emp.first_name} {emp.last_name}".strip() if hasattr(emp, 'first_name') else emp.name if hasattr(emp, 'name') else '',
                    emp.phone_number if hasattr(emp, 'phone_number') else '',
                    emp.position_title if hasattr(emp, 'position_title') else '',
                    emp.gender if hasattr(emp, 'gender') else '',
                    emp.email if hasattr(emp, 'email') else '',
                    getattr(emp, 'salary', '0.00')
                )
                self.tree.insert('', tk.END, values=display_data)
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu nhân viên: {str(e)}")
            print(f"Chi tiết lỗi: {e}")

    def _on_tree_select(self, event):
        """Sự kiện khi người dùng click vào một dòng trên bảng."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        # Lấy dữ liệu của dòng đã chọn
        selected_item = selected_items[0]
        values = self.tree.item(selected_item, 'values')
        
        # Xóa form và điền dữ liệu mới
        self._clear_form(clear_selection=False)
        
        self.entries['ID'].config(state='normal')
        self.entries['ID'].insert(0, values[0]) # ID
        self.entries['ID'].config(state='readonly', foreground="#AAAAAA")
        
        self.entries['Name'].insert(0, values[1]) # Name
        self.entries['Phone'].insert(0, values[2]) # Phone
        self.entries['Role'].set(values[3]) # Role
        self.entries['Gender'].set(values[4]) # Gender
        self.entries['Email'].insert(0, values[5]) # Email
        self.entries['Salary'].insert(0, values[6]) # Salary

    def _clear_form(self, clear_selection=True):
        """Xóa trắng các ô nhập liệu trên form."""
        self.entries['ID'].config(state='normal')
        self.entries['ID'].delete(0, tk.END)
        self.entries['ID'].config(state='readonly')
        
        for key in ['Name', 'Phone', 'Email', 'Salary']:
            self.entries[key].delete(0, tk.END)
            
        self.entries['Role'].set('')
        self.entries['Gender'].set('')
        
        if clear_selection:
            # Bỏ chọn tất cả các dòng trên bảng
            for item in self.tree.selection():
                self.tree.selection_remove(item)

    # --- Các hàm gọi Controller (Cần triển khai logic) ---

    def _add_employee(self):
        """Thêm nhân viên mới vào database."""
        try:
            # Kiểm tra dữ liệu đầu vào
            name = self.entries['Name'].get().strip()
            phone = self.entries['Phone'].get().strip()
            role = self.entries['Role'].get()
            gender = self.entries['Gender'].get()
            email = self.entries['Email'].get().strip()
            
            if not name:
                messagebox.showwarning("Lỗi", "Vui lòng nhập tên nhân viên!")
                return
                
            # Xử lý salary
            salary_value = self.entries['Salary'].get().strip()
            try:
                salary = float(salary_value) if salary_value else 0.0
            except ValueError:
                salary = 0.0
                
            # Map role sang position_id (cần có bảng positions trong DB)
            role_mapping = {
                'Software Engineer': 1,  # Software Engineer
                'UX/UI Designer': 2,     # UX/UI Designer
                'Data Scientist': 3,     # Data Scientist
                'Network Engineer': 4    # Network Engineer
            }
            position_id = role_mapping.get(role, 1)  # Default to 1 if role not found
                
            data = {
                "first_name": name.split()[0] if name.split() else name,
                "last_name": " ".join(name.split()[1:]) if len(name.split()) > 1 else "",
                "phone_number": phone,
                "gender": gender,
                "email": email or f"{name.lower().replace(' ', '.')}@company.com",
                "salary": salary,
                "date_of_birth": "1990-01-01",  # Giá trị mặc định
                "hire_date": "2024-01-01",      # Giá trị mặc định
                "department_id": 1,  # Mặc định department
                "position_id": position_id,    # Sử dụng position_id từ role
            }
            
            # Gọi controller để thêm nhân viên
            result = self.controller.create_employee(data)
            
            if result:
                messagebox.showinfo("Thành công", "Thêm nhân viên thành công!")
                self._clear_form()
                self.load_all_employees()  # Tải lại bảng
            else:
                messagebox.showerror("Lỗi", "Không thể thêm nhân viên!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            print(f"Chi tiết lỗi: {e}")

    def _update_employee(self):
        """Cập nhật thông tin nhân viên."""
        try:
            # Kiểm tra xem có nhân viên nào được chọn không
            selected_items = self.tree.selection()
            if not selected_items:
                messagebox.showwarning("Lỗi", "Vui lòng chọn một nhân viên để cập nhật!")
                return
                
            # Lấy ID từ form
            emp_id = self.entries['ID'].get().strip()
            if not emp_id:
                messagebox.showwarning("Lỗi", "Không có ID nhân viên để cập nhật!")
                return
                
            # Lấy dữ liệu từ form
            name = self.entries['Name'].get().strip()
            phone = self.entries['Phone'].get().strip()
            role = self.entries['Role'].get()
            gender = self.entries['Gender'].get()
            email = self.entries['Email'].get().strip()
            salary_value = self.entries['Salary'].get().strip()
            
            if not name:
                messagebox.showwarning("Lỗi", "Vui lòng nhập tên nhân viên!")
                return
                
            # Xử lý salary
            try:
                salary = float(salary_value) if salary_value else 0.0
            except ValueError:
                salary = 0.0
                
            # Map role sang position_id
            role_mapping = {
                'Software Engineer': 1,  # Software Engineer
                'UX/UI Designer': 2,     # UX/UI Designer
                'Data Scientist': 3,     # Data Scientist
                'Network Engineer': 4    # Network Engineer
            }
            position_id = role_mapping.get(role, 1)
                
            # Tạo dữ liệu để cập nhật
            data = {
                "first_name": name.split()[0] if name.split() else name,
                "last_name": " ".join(name.split()[1:]) if len(name.split()) > 1 else "",
                "phone_number": phone,
                "gender": gender,
                "email": email,
                "salary": salary,
                "position_id": position_id,
            }
            
            # Gọi controller để cập nhật
            result = self.controller.update_employee(int(emp_id), data)
            
            if result:
                messagebox.showinfo("Thành công", "Cập nhật nhân viên thành công!")
                self.load_all_employees()  # Tải lại bảng
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật nhân viên!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            print(f"Chi tiết lỗi: {e}")
        
    def _delete_employee(self):
        """Xóa nhân viên được chọn."""
        try:
            selected_items = self.tree.selection()
            if not selected_items:
                messagebox.showwarning("Lỗi", "Vui lòng chọn một nhân viên để xóa.")
                return
                
            # Lấy ID từ form hoặc từ tree
            emp_id = self.entries['ID'].get().strip()
            if not emp_id:
                # Lấy từ tree nếu form trống
                selected_item = selected_items[0]
                values = self.tree.item(selected_item, 'values')
                emp_id = values[0]
                
            if not emp_id:
                messagebox.showwarning("Lỗi", "Không thể xác định ID nhân viên!")
                return
                
            # Xác nhận xóa
            if messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc chắn muốn xóa nhân viên ID: {emp_id}?"):
                # Gọi controller để xóa
                result = self.controller.delete_employee(int(emp_id))
                
                if result:
                    messagebox.showinfo("Thành công", "Xóa nhân viên thành công!")
                    self._clear_form()
                    self.load_all_employees()  # Tải lại bảng
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa nhân viên!")
                    
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            print(f"Chi tiết lỗi: {e}")

    def _search_data(self):
        search_term = self.search_entry.get()
        search_by = self.search_by_combo.get()
        # TODO: Triển khai logic tìm kiếm và tải lại bảng
        messagebox.showinfo("Chức năng", f"Tìm kiếm với: {search_term} theo {search_by} - Cần được triển khai!")

