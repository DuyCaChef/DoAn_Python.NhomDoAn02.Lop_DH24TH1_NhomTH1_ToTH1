from app.database.connection import create_connection
from typing import Dict, Any, List, Optional

# SỬA: ĐỊNH NGHĨA CLASS 'EmployeeQueries'
class EmployeeQueries:
    """
    Lớp chứa tất cả các phương thức để tương tác với bảng 'employees' trong DB.
    """
    
    def _execute_query(self, query: str, params: tuple = None, fetch_one=False, fetch_all=False, commit=False): 
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor(dictionary=True) # Dùng dictionary=True
            
            cursor.execute(query, params if params else ())
                
            if commit:
                conn.commit()
                return cursor.lastrowid 
                
            if fetch_one:
                return cursor.fetchone() 
                
            if fetch_all:
                return cursor.fetchall() 
                
        except Exception as e:
            print(f"Lỗi truy vấn: {e}")
            if conn and commit:
                conn.rollback()
            raise e 
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # --- CÁC HÀM CRUD MÀ CONTROLLER GỌI ---

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """Lấy tất cả nhân viên với thông tin JOIN."""
        query = """
        SELECT 
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.gender,
            e.date_of_birth,
            e.email,
            e.phone_number,
            e.address,
            e.hire_date,
            e.status,
            e.department_id,
            e.position_id,
            e.manager_id,
            d.name as department_name, 
            p.title as position_title,
            COALESCE(c.base_salary, 0) as base_salary
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        LEFT JOIN contracts c ON e.id = c.employee_id
        ORDER BY e.id
        """
        return self._execute_query(query, fetch_all=True)
    
    def get_employee_by_id(self, emp_id: int) -> Optional[Dict[str, Any]]:
        """Lấy 1 nhân viên bằng ID (cho form update và role Employee)."""
        query = """
        SELECT 
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.gender,
            e.date_of_birth,
            e.email,
            e.phone_number,
            e.address,
            e.hire_date,
            e.status,
            e.department_id,
            e.position_id,
            e.manager_id,
            d.name as department_name, 
            p.title as position_title,
            COALESCE(c.base_salary, 0) as base_salary
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        LEFT JOIN contracts c ON e.id = c.employee_id
        WHERE e.id = %s
        """
        return self._execute_query(query, params=(emp_id,), fetch_one=True)

    def get_employees_by_manager_id(self, manager_id: int) -> List[Dict[str, Any]]:
        """Lấy các nhân viên mà manager này quản lý."""
        query = """
        SELECT 
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.gender,
            e.date_of_birth,
            e.email,
            e.phone_number,
            e.address,
            e.hire_date,
            e.status,
            e.department_id,
            e.position_id,
            e.manager_id,
            d.name as department_name, 
            p.title as position_title,
            COALESCE(c.base_salary, 0) as base_salary
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        LEFT JOIN contracts c ON e.id = c.employee_id
        WHERE e.manager_id = %s
        ORDER BY e.id
        """
        return self._execute_query(query, params=(manager_id,), fetch_all=True)


    def add_employee(self,data: Dict[str, Any]) -> Optional[int]:
        """Thêm một nhân viên mới từ dictionary."""
        cols = [
            "employee_code", "first_name", "last_name", "gender", 
            "date_of_birth", "email", "phone_number", "address", 
            "hire_date", "status", "department_id", "position_id", "manager_id"
        ]
        values_tuple = tuple(data.get(col) for col in cols)
        
        placeholders = ", ".join(["%s"] * len(cols))
        query = f"INSERT INTO employees ({', '.join(cols)}) VALUES ({placeholders})"
        
        return self._execute_query(query, params=values_tuple, commit=True)
    
    def update_employee_by_id(self, emp_id: int, data: Dict[str, Any]):
        """Cập nhật nhân viên dựa trên ID (integer)."""
        safe_cols = [
            "first_name", "last_name", "gender", "email", 
            "phone_number", "address", "department_id", "position_id"
        ]
        
        set_clauses = []
        params = []
        
        for col in safe_cols:
            if col in data:
                set_clauses.append(f"{col} = %s")
                params.append(data[col])
                
        if not set_clauses:
            raise ValueError("Không có dữ liệu để cập nhật")
            
        params.append(emp_id)
        
        query = f"UPDATE employees SET {', '.join(set_clauses)} WHERE id = %s"
        return self._execute_query(query, params=tuple(params), commit=True)

    def delete_employee_by_id(self, emp_id: int):
        """Xóa nhân viên dựa trên ID (integer)."""
        query = "DELETE FROM employees WHERE id = %s"
        return self._execute_query(query, params=(emp_id,), commit=True)

    def search_employees(self, search_by: str, search_text: str) -> List[Dict[str, Any]]:
        """Tìm kiếm nhân viên (an toàn)."""
        safe_columns = ['employee_code', 'first_name', 'last_name', 'email', 'phone_number']
        if search_by not in safe_columns:
            raise ValueError("Điều kiện tìm kiếm không hợp lệ")

        query = f"""
        SELECT 
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.gender,
            e.email,
            e.phone_number,
            e.address,
            d.name as department_name,
            p.title as position_title
        FROM employees e
        LEFT JOIN positions p ON e.position_id = p.id
        LEFT JOIN departments d ON e.department_id = d.id
        WHERE e.{search_by} LIKE %s
        ORDER BY e.id
        """
        params = (f"%{search_text}%",)
        return self._execute_query(query, params=params, fetch_all=True)
    
    
    
    def get_all_departments(self) -> List[Dict[str, Any]]:
   
        query = "SELECT id, name FROM departments ORDER BY name"
        return self._execute_query(query, fetch_all=True)

    def get_positions_by_department_id(self, department_id: int) -> List[Dict[str, Any]]:
        """Lấy các chức vụ (positions) CHỈ thuộc về một phòng ban."""
        query = "SELECT id, title FROM positions WHERE department_id = %s ORDER BY title"
        return self._execute_query(query, params=(department_id,), fetch_all=True)

    def get_department_by_position_id(self, position_id: int) -> Optional[Dict[str, Any]]:
        """Tìm phòng ban (department) của một chức vụ (position)."""
        query = """
            SELECT d.id, d.name
            FROM departments d
            JOIN positions p ON p.department_id = d.id
            WHERE p.id = %s
        """
        return self._execute_query(query, params=(position_id,), fetch_one=True)