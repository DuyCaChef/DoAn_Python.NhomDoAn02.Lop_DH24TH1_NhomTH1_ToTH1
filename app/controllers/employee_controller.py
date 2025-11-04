# SỬA: Import code DB của BẠN (không phải code wrapper)
from app.database import employee_queries as db 
from typing import List, Dict, Tuple, Any

class EmployeeController:
    """
    Kết nối View (Giao diện) với Model (Database).
    View gọi các hàm ở đây.
    """
    
    def __init__(self):
        # Các cột mà Treeview mong đợi - Thêm Department và Position
        self.view_columns = ('ID', 'Code', 'Full Name', 'Email', 'Phone', 'Gender', 'Address', 'Department', 'Position')

    def _format_data_for_view(self, employees_raw: List[Dict[str, Any]]) -> List[Tuple]:
        """
        Hàm nội bộ: Chuyển đổi dữ liệu thô từ DB (List[Dict]) 
        thành dữ liệu cho View (List[Tuple])
        """
        formatted_list = []
        for emp in employees_raw:
            full_name = f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip()
            formatted_list.append((
                emp.get('id', ''),
                emp.get('employee_code', ''),
                full_name,
                emp.get('email', ''),
                emp.get('phone_number', ''),
                emp.get('gender', ''),
                emp.get('address', ''),
                emp.get('department_name', ''),  # Department từ JOIN
                emp.get('position_title', '')    # ✅ Position từ JOIN
            ))
        return formatted_list

    # --- Các hàm được gọi bởi View ---

    def get_all_employees_for_view(self) -> List[Tuple]:
        """
        View gọi hàm này để lấy TẤT CẢ nhân viên
        đã được định dạng cho bảng.
        """
        try:
            employees_raw = db.get_all_employees() # 1. Gọi DB của bạn
            return self._format_data_for_view(employees_raw) # 2. Định dạng
        except Exception as e:
            raise Exception(f"Không thể tải danh sách nhân viên: {e}")

    def add_employee(self, data: Dict[str, Any]) -> str:
        """
        View gọi hàm này để THÊM nhân viên.
        'data' là dữ liệu thô từ các ô Entry.
        """
        try:
            # --- Đây là Logic Nghiệp vụ (Business Logic) ---
            if not data['employee_code'] or not data['first_name']:
                raise ValueError("Mã nhân viên và Tên là bắt buộc.")
            
            # Tách tên (vì form của bạn bạn chỉ có 1 trường 'Name')
            name_parts = data['first_name'].split(maxsplit=1)
            data['first_name'] = name_parts[0]
            data['last_name'] = name_parts[1] if len(name_parts) > 1 else ""

            # 3. Gọi Database
            db.add_employee(data) # Truyền dictionary đã xử lý
            return "Thêm nhân viên thành công!"
            
        except Exception as e:
            # Hiển thị lỗi thân thiện hơn
            raise Exception(f"Lỗi khi thêm: {e}")

    def update_employee(self, employee_code: str, data: Dict[str, Any]) -> str:
        """
        View gọi hàm này để CẬP NHẬT nhân viên.
        """
        try:
            if not employee_code:
                raise ValueError("Không có mã nhân viên để cập nhật.")
            
            # Tách tên giống như lúc Add
            name_parts = data['first_name'].split(maxsplit=1)
            data['first_name'] = name_parts[0]
            data['last_name'] = name_parts[1] if len(name_parts) > 1 else ""
            
            # Gọi hàm DB của bạn (giả sử tên là update_employee)
            db.update_employee(employee_code, data)
            return "Cập nhật thành công!"
        except Exception as e:
            raise Exception(f"Lỗi khi cập nhật: {e}")

    def delete_employee(self, employee_code: str) -> str:
        """
        View gọi hàm này để XÓA nhân viên.
        """
        try:
            if not employee_code:
                raise ValueError("Không có mã nhân viên để xóa.")
                
            db.delete_employee(employee_code) # Gọi hàm DB của bạn
            return "Xóa thành công!"
        except Exception as e:
            raise Exception(f"Lỗi khi xóa: {e}")

    def search_employees(self, search_by: str, search_text: str) -> List[Tuple]:
        """
        View gọi hàm này để TÌM KIẾM.
        """
        try:
            # Gọi hàm DB của bạn
            employees_raw = db.search_employees(search_by, search_text) 
            # Định dạng lại kết quả tìm kiếm cho View
            return self._format_data_for_view(employees_raw)
        except Exception as e:
            raise Exception(f"Lỗi khi tìm kiếm: {e}")