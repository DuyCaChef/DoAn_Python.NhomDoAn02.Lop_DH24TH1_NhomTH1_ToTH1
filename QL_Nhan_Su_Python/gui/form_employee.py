import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Cấu hình cửa sổ chính ---
        self.title("Employee Management System")
        self.geometry('1200x650')  # Đặt kích thước cửa sổ
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Cấu hình grid layout cho cửa sổ chính ---
        # Hàng 0: Header (co giãn theo chiều rộng)
        # Hàng 1: Content (co giãn theo cả chiều rộng và chiều cao)
        # Cột 0: Left Panel (chiều rộng cố định)
        # Cột 1: Right Panel (co giãn theo chiều rộng)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Tạo các thành phần giao diện ---
        self.create_header()
        self.create_left_panel()
        self.create_right_panel()

        # Hiển thị giữa màn hình
        self._center_window()

    def create_header(self):
        """Tạo khung header màu tím ở trên cùng"""
        # Lưu ý: CustomTkinter không hỗ trợ gradient.
        # Chúng ta sử dụng màu tím đồng nhất (#5D3FD3) để mô phỏng.
        header_frame = ctk.CTkFrame(self, height=80, fg_color="#5D3FD3", corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_frame.pack_propagate(False) # Ngăn co lại theo nội dung

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
        left_panel = ctk.CTkFrame(self, width=320, fg_color="#2B2B2B")
        left_panel.grid(row=1, column=0, sticky="nsw", padx=(10, 5), pady=10)
        left_panel.grid_propagate(False) # Ngăn thay đổi kích thước theo nội dung

        details_label = ctk.CTkLabel(
            left_panel, 
            text="Employee Details", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        details_label.pack(pady=20, padx=20, anchor="w")

        # --- Form Fields ---
        # Id
        id_label = ctk.CTkLabel(left_panel, text="Id", anchor="w")
        id_label.pack(fill="x", padx=20, pady=(0, 5))
        id_entry = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter id", 
        )
        id_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Name
        name_label = ctk.CTkLabel(left_panel, text="Name", anchor="w")
        name_label.pack(fill="x", padx=20, pady=(0, 5))
        name_entry = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter name"
        )
        name_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Phone
        phone_label = ctk.CTkLabel(left_panel, text="Phone", anchor="w")
        phone_label.pack(fill="x", padx=20, pady=(0, 5))
        phone_entry = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter phone"
        )
        phone_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Role
        role_label = ctk.CTkLabel(left_panel, text="Role", anchor="w")
        role_label.pack(fill="x", padx=20, pady=(0, 5))
        role_combo = ctk.CTkComboBox(
            left_panel, 
            values=["Web Developer", "UX/UI Designer", "Cloud Architect", "Network Engineer", "Data Scientist"]
        )
        role_combo.set("Web Developer")
        role_combo.pack(fill="x", padx=20, pady=(0, 15))

        # Gender
        gender_label = ctk.CTkLabel(left_panel, text="Gender", anchor="w")
        gender_label.pack(fill="x", padx=20, pady=(0, 5))
        gender_combo = ctk.CTkComboBox(
            left_panel, 
            values=["Male", "Female", "Other"]
        )
        gender_combo.set("Male")
        gender_combo.pack(fill="x", padx=20, pady=(0, 15))

        # Salary
        salary_label = ctk.CTkLabel(left_panel, text="Salary", anchor="w")
        salary_label.pack(fill="x", padx=20, pady=(0, 5))
        salary_entry = ctk.CTkEntry(
            left_panel, 
            placeholder_text="Enter salary"
        )
        salary_entry.pack(fill="x", padx=20, pady=(0, 15))

    def create_right_panel(self):
        """Tạo khung hiển thị dữ liệu bên phải"""
        right_panel = ctk.CTkFrame(self, fg_color="#343638")
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # --- Search Bar ---
        self.create_search_bar(right_panel)

        # --- Table (Mô phỏng bằng ScrollableFrame và Grid) ---
        self.create_table(right_panel)

    def create_search_bar(self, parent):
        """Tạo thanh tìm kiếm và lọc"""
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        filter_combo = ctk.CTkComboBox(search_frame, values=["All"])
        filter_combo.set("All")
        filter_combo.pack(side="left", padx=(0, 10))

        search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Search..."
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=10)

        search_button = ctk.CTkButton(
            search_frame, 
            text="Search", 
            width=100, 
            fg_color="#5D3FD3", 
            hover_color="#4A2F9D"
        )
        search_button.pack(side="left", padx=10)

        show_all_button = ctk.CTkButton(
            search_frame, 
            text="Show All", 
            width=100, 
            fg_color="#5D3FD3", 
            hover_color="#4A2F9D"
        )
        show_all_button.pack(side="left", padx=(0, 10))

    def create_table(self, parent):
        """Tạo bảng dữ liệu mô phỏng"""
        table_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Cấu hình grid cho bảng
        table_frame.grid_columnconfigure(0, weight=0) # Id
        table_frame.grid_columnconfigure(1, weight=2) # Name
        table_frame.grid_columnconfigure(2, weight=2) # Phone
        table_frame.grid_columnconfigure(3, weight=2) # Role
        table_frame.grid_columnconfigure(4, weight=1) # Gender
        table_frame.grid_columnconfigure(5, weight=1) # Salary
        table_frame.grid_columnconfigure(6, weight=1) # Actions

        # --- Tiêu đề bảng ---
        headers = ["Id", "Name", "Phone", "Role", "Gender", "Salary", "Actions"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                table_frame, 
                text=header, 
                font=ctk.CTkFont(size=14, weight="bold")
            )
            header_label.grid(row=0, column=col, sticky="w", padx=10, pady=10)

        # --- Dữ liệu mẫu ---
        sample_data = [
            {"id": 1, "name": "faizan", "phone": "7905112734", "role": "Web Developer", "gender": "Male", "salary": "40,000"},
            {"id": 2, "name": "Eram", "phone": "7887887654", "role": "UX/UI Designer", "gender": "Female", "salary": "50,000"},
            {"id": 3, "name": "Joy", "phone": "8767567898", "role": "Cloud Architect", "gender": "Male", "salary": "45,000"},
            {"id": 5, "name": "Daisy", "phone": "9878989878", "role": "Network Engineer", "gender": "Female", "salary": "20,000"},
            {"id": 4, "name": "Sid", "phone": "8798786756", "role": "Data Scientist", "gender": "Male", "salary": "45,000"},
        ]

        # --- Tạo các hàng dữ liệu ---
        for i, row_data in enumerate(sample_data):
            row = i + 1 # Bắt đầu từ hàng 1 (sau header)

            # Id
            id_label = ctk.CTkLabel(table_frame, text=row_data["id"])
            id_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            # Name
            name_label = ctk.CTkLabel(table_frame, text=row_data["name"])
            name_label.grid(row=row, column=1, sticky="w", padx=10, pady=5)
            
            # Phone
            phone_label = ctk.CTkLabel(table_frame, text=row_data["phone"])
            phone_label.grid(row=row, column=2, sticky="w", padx=10, pady=5)
            
            # Role
            role_label = ctk.CTkLabel(table_frame, text=row_data["role"])
            role_label.grid(row=row, column=3, sticky="w", padx=10, pady=5)
            
            # Gender
            gender_label = ctk.CTkLabel(table_frame, text=row_data["gender"])
            gender_label.grid(row=row, column=4, sticky="w", padx=10, pady=5)
            
            # Salary
            salary_label = ctk.CTkLabel(table_frame, text=row_data["salary"])
            salary_label.grid(row=row, column=5, sticky="w", padx=10, pady=5)
            
            # Actions
            action_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
            action_frame.grid(row=row, column=6, sticky="w", padx=5, pady=5)
            
            edit_button = ctk.CTkButton(
                action_frame, 
                text="Edit", 
                width=60, 
                fg_color="#3B82F6", 
                hover_color="#2563EB"
            )
            edit_button.pack(side="left", padx=5)
            
            delete_button = ctk.CTkButton(
                action_frame, 
                text="Delete", 
                width=60, 
                fg_color="#EF4444", 
                hover_color="#DC2626"
            )
            delete_button.pack(side="left", padx=5)

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
            w, h = 1200, 650

        # Tính toán vị trí giữa màn hình
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        
        # Chỉ thay đổi vị trí, giữ nguyên kích thước
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    app = App()
    app.mainloop()


