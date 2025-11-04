import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
# SỬA: Không import database ở đây

# SỬA: Đổi tên class thành 'MainWindow' và kế thừa từ ctk.CTk
class MainWindow(ctk.CTk):
    
    # SỬA: Hàm __init__ nhận 'controller'
    def __init__(self, controller): 
        super().__init__() # Khởi tạo ctk.CTk
        self.controller = controller # LƯU LẠI "BỘ NÃO"

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

        # Hiển thị giữa màn hình
        self._center_window()

        # Tải dữ liệu lần đầu
        self.fetch_data()

    def create_header(self):
        """Tạo khung header màu tím ở trên cùng"""
        header_frame = ctk.CTkFrame(self, height=80, fg_color="#5D3FD3", corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            header_frame, 
            text="Employee Management System", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(padx=20, pady=(15, 2), anchor="w") 

        subtitle_label = ctk.CTkLabel(
            header_frame, 
            text="Manage your team efficiently", 
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(padx=20, pady=(0, 15), anchor="w")

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

        # Buttons frame
        buttons_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Add button
        add_button = ctk.CTkButton(
            buttons_frame,
            text="Add Employee",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28A745",
            hover_color="#218838",
            command=self.add_employee
        )
        add_button.pack(fill="x", pady=(0, 10))

        # Buttons row - Grid layout để đều nhau
        button_row = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        button_row.pack(fill="x", pady=(0, 10))
        
        # Cấu hình 3 cột đều nhau
        button_row.grid_columnconfigure(0, weight=1, uniform="button")
        button_row.grid_columnconfigure(1, weight=1, uniform="button")
        button_row.grid_columnconfigure(2, weight=1, uniform="button")
        
        update_button = ctk.CTkButton(
            button_row,
            text="Update",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.update_employee
        )
        update_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        delete_button = ctk.CTkButton(
            button_row,
            text="Delete",
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.delete_employee
        )
        delete_button.grid(row=0, column=1, padx=5, sticky="ew")
        
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
        
        # Treeview
        self.tree_columns = ('ID', 'Code', 'Full Name', 'Email', 'Phone', 'Gender', 'Address')
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
        self.tree['show'] = 'headings'
        
        self.tree.column('ID', width=50)
        self.tree.column('Code', width=100)
        self.tree.column('Full Name', width=150)
        self.tree.column('Email', width=180)
        self.tree.column('Phone', width=120)
        self.tree.column('Gender', width=80)
        self.tree.column('Address', width=200)
        
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
        # 1. Thu thập dữ liệu thô từ Form
        data = {
            'employee_code': self.txt_id.get(),
            'first_name': self.txt_name.get(), # Controller sẽ tự tách tên
            'gender': self.combo_gender.get(),
            'email': self.txt_email.get(),
            'phone_number': self.txt_phone.get(),
            'address': self.txt_address.get(),
            # Các trường này DB của bạn yêu cầu (từ schema)
            'date_of_birth': '1990-01-01', # Tạm thời - Cần thêm vào form
            'hire_date': '2025-01-01', # Tạm thời - Cần thêm vào form
            'status': 'Đang làm việc'
        }

        # 2. Gọi "bộ não" (Controller) để xử lý
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
            
        data = {
            'first_name': self.txt_name.get(), # Controller sẽ tự tách tên
            'gender': self.combo_gender.get(),
            'email': self.txt_email.get(),
            'phone_number': self.txt_phone.get(),
            'address': self.txt_address.get(),
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