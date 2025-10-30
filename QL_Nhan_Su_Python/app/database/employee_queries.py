from app.database.connection import create_connection
from app.models.employee import Employee
from typing import Dict, Any, List, Optional
import hashlib

class EmployeeQueries:
    """
    Lớp chứa tất cả các phương thức để tương tác với bảng 'employees' trong DB.
    """
    def get_all_employees(self) -> List[Dict[str, Any]]:
        conn = create_connection()
        if conn is None: return []
        employees = []
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    e.*,
                    d.name as department_name, 
                    p.title as position_title
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                ORDER BY e.id
            """
            cursor.execute(query)
            employees = cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi truy vấn nhân viên: {e}")
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
        return employees

    def add_employee(self, data: Dict[str, Any]) -> Optional[int]:
        conn = create_connection()
        if conn is None: return None
        last_id = None
        try:
            cursor = conn.cursor()
            cols = [
                "employee_code", "first_name", "last_name", "gender", "date_of_birth", 
                "email", "phone_number", "address", "hire_date", "status", 
                "department_id", "position_id", "manager_id"
            ]
            placeholders = ", ".join(["%s"] * len(cols))
            sql = f"INSERT INTO employees ({', '.join(cols)}) VALUES ({placeholders})"
            values = tuple(data.get(col) for col in cols)
            cursor.execute(sql, values)
            conn.commit()
            last_id = cursor.lastrowid
        except Exception as e:
            print(f"Lỗi khi thêm nhân viên: {e}")
            conn.rollback()
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
        return last_id

    # update_employee and delete_employee omitted for brevity
