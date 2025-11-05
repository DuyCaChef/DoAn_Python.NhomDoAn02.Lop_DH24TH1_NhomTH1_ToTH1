# SỬA: Import code DB của BẠN (không phải code wrapper)
from app.database.employee_queries import EmployeeQueries
from typing import List, Dict, Tuple, Any
from app.controllers.auth_controller import AuthController
class EmployeeController:
    """
    Kết nối View (Giao diện) với Model (Database).
    View gọi các hàm ở đây.
    """
    def __init__(self, auth_controller: AuthController):
        self.db = EmployeeQueries() 
        self.auth = auth_controller # Sử dụng AuthController được truyền vào
        # Các cột mà Treeview của bạn bạn mong đợi
        self.view_columns = ('ID', 'Code', 'Full Name', 'Email', 'Phone', 'Gender', 'Address')

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
                emp.get('address', '')
            ))
        return formatted_list

    # --- Các hàm được gọi bởi View ---

    def get_all_employees_for_view(self) -> List[Dict[str, Any]]:
        """
        Lấy danh sách nhân viên DỰA TRÊN VAI TRÒ.
        """
        try:
            # Lấy thông tin người đang đăng nhập
            role = self.auth.get_current_user_role()
            my_employee_id = self.auth.get_current_user_employee_id()
            
            print(f"Đang tải dữ liệu cho Role: {role}, Employee ID: {my_employee_id}")
            
            if role == 'Admin':
                # 1. Admin thấy tất cả
                return self.db.get_all_employees() 
            elif role == 'Manager':
                # 2. Manager thấy nhân viên do mình quản lý
                # (Cần hàm get_employees_by_manager_id trong queries)
                return self.db.get_employees_by_manager_id(my_employee_id)
            elif role == 'Employee':
                # 3. Employee chỉ thấy chính mình
                # (Cần hàm get_employee_by_id trong queries)
                emp = self.db.get_employee_by_id(my_employee_id)
                return [emp] if emp else []
            else:
                return [] # Không có vai trò -> không thấy gì
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
            self.db.add_employee(data) # Truyền dictionary đã xử lý
            return "Thêm nhân viên thành công!"
            
        except Exception as e:
            # Hiển thị lỗi thân thiện hơn
            raise Exception(f"Lỗi khi thêm: {e}")

    def update_employee(self, employee_code: str, data: Dict[str, Any]) -> str:
        """
        View gọi hàm này để CẬP NHẬT nhân viên.
        """
        role = self.auth.get_current_user_role()
        my_emp_id = self.auth.get_current_user_employee_id()
        try:
            if not employee_code:
                raise ValueError("Không có mã nhân viên để cập nhật.")

            # SỬA: Logic phân quyền
            # (Giả sử Employee không được update)
            if role not in ['Admin', 'Manager']:
                 raise Exception("Bạn không có quyền cập nhật thông tin.")

            # Tách tên giống như lúc Add
            name_parts = data['first_name'].split(maxsplit=1)
            data['first_name'] = name_parts[0]
            data['last_name'] = name_parts[1] if len(name_parts) > 1 else ""
            
            # Gọi hàm DB của bạn (giả sử tên là update_employee)
            print(f"ĐANG CẬP NHẬT: {employee_code} với dữ liệu {data}")
            self.db.update_employee(employee_code, data)
            return "Cập nhật thành công!"
        except Exception as e:
            raise Exception(f"Lỗi khi cập nhật: {e}")

    def delete_employee(self, employee_code: str) -> str:
        """
        View gọi hàm này để XÓA nhân viên.
        """
        role = self.auth.get_current_user_role()
        if role != 'Admin':
            raise Exception("Bạn không có quyền xóa nhân viên.")
        try:
            if not employee_code:
                raise ValueError("Không có mã nhân viên để xóa.")
            
            print(f"ĐANG XÓA: {employee_code}")
            self.db.delete_employee(employee_code) # Gọi hàm DB của bạn
            return "Xóa thành công!"
        except Exception as e:
            raise Exception(f"Lỗi khi xóa: {e}")

    def search_employees(self, search_by: str, search_text: str) -> List[Tuple]:
        """
        View gọi hàm này để TÌM KIẾM.
        """
        try:
            # Gọi hàm DB của bạn
            print(f"ĐANG TÌM KIẾM: {search_by} = {search_text}")
            all_data = self.db.get_all_employees()
            results = [emp for emp in all_data if search_text.lower() in str(emp.get(search_by)).lower()]
            return results
        except Exception as e:
            raise Exception(f"Lỗi khi tìm kiếm: {e}")