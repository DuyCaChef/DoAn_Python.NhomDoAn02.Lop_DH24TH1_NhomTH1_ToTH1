# SỬA: Import code DB của BẠN (không phải code wrapper)
from app.database.employee_queries import EmployeeQueries
from typing import List, Dict, Optional, Tuple, Any
from app.controllers.auth_controller import AuthController

class EmployeeController:
    """
    Bộ não xử lý logic cho Quản lý Nhân viên.
    Kết nối View (Giao diện) với Model (Database).
    """
    def __init__(self, auth_controller: AuthController):
        self.db = EmployeeQueries() 
        self.auth = auth_controller # "Bộ não" Auth
        
        # Tải map Chức vụ
        self.position_map = self._load_position_map()

    def _load_position_map(self):
        """Tải (tên -> id) cho tất cả Chức vụ."""
        try:
            # TODO: Cần hàm 'get_all_positions' trong queries
            # Tạm thời hardcode
            return {
                'Software Engineer': 4,
                'Web Developer': 5,
                'Tester': 6,
                'IT Manager': 13,
            }
        except Exception as e:
            print(f"Lỗi tải Position Map: {e}")
            return {}

    # --- Các hàm được gọi bởi View ---

    def get_all_employees_for_view(self) -> List[Dict[str, Any]]:
        """
        Lấy danh sách nhân viên DỰA TRÊN VAI TRÒ.
        """
        try:
            role = self.auth.get_current_user_role()
            my_employee_id = self.auth.get_current_user_employee_id()
            
            print(f"Đang tải dữ liệu cho Role: {role}, Employee ID: {my_employee_id}")
            
            if role == 'Admin':
                return self.db.get_all_employees() 
            elif role == 'Manager':
                return self.db.get_employees_by_manager_id(my_employee_id)
            elif role == 'Employee':
                emp = self.db.get_employee_by_id(my_employee_id)
                return [emp] if emp else []
            else:
                return [] 
        except Exception as e:
            raise Exception(f"Không thể tải danh sách nhân viên: {str(e)}")

    def get_employee_details(self, emp_id: int) -> Dict[str, Any]:
        """Lấy chi tiết 1 nhân viên (dùng cho form update)"""
        try:
            emp = self.db.get_employee_by_id(emp_id)
            if emp and 'base_salary' not in emp:
                emp['base_salary'] = 0.0 # Thêm giá trị nếu thiếu
            return emp
        except Exception as e:
            raise Exception(f"Lỗi khi lấy chi tiết: {e}")
        

    def add_employee(self, data: Dict[str, Any]) -> str:
        """
        View gọi hàm này để THÊM nhân viên.
        'data' là dữ liệu thô từ các ô Entry.
        """
        role = self.auth.get_current_user_role()
        if role not in ['Admin', 'Manager']: 
            raise Exception("Bạn không có quyền thêm nhân viên.")
        
        if not data['employee_code'] or not data['first_name']:
            raise ValueError("Mã nhân viên và Tên là bắt buộc.")
        
        name_parts = data['first_name'].split(maxsplit=1)
        data['first_name'] = name_parts[0]
        data['last_name'] = name_parts[1] if len(name_parts) > 1 else ""
            
        new_emp_id = self.db.add_employee(data)
        
        # TODO: Tạo Contract
        # base_salary = float(data.get('base_salary', 0))
        # self.db.create_contract(new_emp_id, base_salary, ...)
        
        return "Thêm nhân viên thành công!"

    
    def update_employee(self, emp_id: int, data: Dict[str, Any]) -> str:
        """
        View gọi hàm này để CẬP NHẬT nhân viên.
        """
        role = self.auth.get_current_user_role()
        my_emp_id = self.auth.get_current_user_employee_id()
        
        # Admin được sửa tất cả, Employee chỉ được sửa mình
        if role == 'Admin' or (role == 'Employee' and emp_id == my_emp_id):
            
            if 'first_name' in data:
                name_parts = data['first_name'].split(maxsplit=1)
                data['first_name'] = name_parts[0]
                data['last_name'] = name_parts[1] if len(name_parts) > 1 else ""
            
            print(f"ĐANG CẬP NHẬT: {emp_id}")
            # SỬA: Gửi ID (int) thay vì code
            self.db.update_employee_by_id(emp_id, data) # Cần hàm này
            return "Cập nhật thành công!"
        else:
            raise Exception("Bạn không có quyền sửa thông tin này.")
    
    def delete_employee(self, emp_id: int) -> str:
        """
        View gọi hàm này để XÓA nhân viên.
        """
        role = self.auth.get_current_user_role()
        if role != 'Admin': 
            raise Exception("Bạn không có quyền xóa nhân viên.")
            
        print(f"ĐANG XÓA: {emp_id}")
        # SỬA: Gửi ID (int)
        self.db.delete_employee_by_id(emp_id) # Cần hàm này
        return "Xóa thành công!"

    def search_employees(self, search_by: str, search_text: str) -> List[Dict[str, Any]]:
        """
        View gọi hàm này để TÌM KIẾM.
        """
        try:
            print(f"ĐANG TÌM KIẾM: {search_by} = {search_text}")
            # self.db.search_employees(...) # Cần hàm này
            all_data = self.db.get_all_employees()
            results = [emp for emp in all_data if search_text.lower() in str(emp.get(search_by)).lower()]
            return results
        except Exception as e:
            raise Exception(f"Lỗi khi tìm kiếm: {e}")
            
    # --- CÁC HÀM MỚI ĐỂ ĐIỀN VÀO COMBOBOX ---

    def get_all_departments_for_view(self) -> List[tuple[int, str]]:
        """Lấy danh sách (id, name) của TẤT CẢ phòng ban."""
        try:
            departments_raw = self.db.get_all_departments()
            return [(d['id'], d['name']) for d in departments_raw]
        except Exception as e:
            raise Exception(f"Không thể tải danh sách phòng ban: {str(e)}")

    def get_positions_by_department_id_for_view(self, dept_id: int) -> List[tuple[int, str]]:
        """Lấy (id, title) của các chức vụ thuộc 1 phòng ban."""
        try:
            positions_raw = self.db.get_positions_by_department_id(dept_id)
            return [(p['id'], p['title']) for p in positions_raw]
        except Exception as e:
            raise Exception(f"Không thể tải danh sách chức vụ: {str(e)}")

    def get_department_by_position_id_for_view(self, pos_id: int) -> Optional[tuple[int, str]]:
        """Tìm (id, name) của phòng ban từ 1 chức vụ."""
        try:
            dept_raw = self.db.get_department_by_position_id(pos_id)
            if dept_raw:
                return (dept_raw['id'], dept_raw['name'])
            return None
        except Exception as e:
            raise Exception(f"Không thể tìm phòng ban: {str(e)}")