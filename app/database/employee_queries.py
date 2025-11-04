from app.database.connection import create_connection
from typing import Dict, Any, List, Optional

# --- HÀM TRỢ GIÚP CHUNG ---
def _execute_query(query: str, params: tuple = None, fetch_one=False, fetch_all=False, commit=False):
    """Hàm trợ giúp chung để chạy các truy vấn."""
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

def get_all_employees() -> List[Dict[str, Any]]:
    """Lấy tất cả nhân viên với thông tin JOIN."""
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
    return _execute_query(query, fetch_all=True)

def add_employee(data: Dict[str, Any]) -> Optional[int]:
    """Thêm một nhân viên mới từ dictionary."""
    # Lấy các trường khớp với DB (từ schema)
    cols = [
        "employee_code", "first_name", "last_name", "gender", 
        "date_of_birth", "email", "phone_number", "address", 
        "hire_date", "status", "department_id", "position_id", "manager_id"
    ]
    
    # Lọc ra các giá trị từ data, nếu thiếu thì dùng None
    values_tuple = tuple(data.get(col) for col in cols)
    
    placeholders = ", ".join(["%s"] * len(cols))
    query = f"INSERT INTO employees ({', '.join(cols)}) VALUES ({placeholders})"
    
    return _execute_query(query, params=values_tuple, commit=True)

def update_employee(employee_code: str, data: Dict[str, Any]):
    """Cập nhật nhân viên dựa trên employee_code."""
    # Lọc ra các trường mà View gửi lên (an toàn) - Thêm department_id và position_id
    safe_cols = ["first_name", "last_name", "gender", "email", "phone_number", "address", "department_id", "position_id"]
    
    set_clauses = []
    params = []
    
    for col in safe_cols:
        if col in data:
            set_clauses.append(f"{col} = %s")
            params.append(data[col])
            
    if not set_clauses:
        raise ValueError("Không có dữ liệu để cập nhật")
        
    # Thêm employee_code vào cuối cho mệnh đề WHERE
    params.append(employee_code)
    
    query = f"UPDATE employees SET {', '.join(set_clauses)} WHERE employee_code = %s"
    
    return _execute_query(query, params=tuple(params), commit=True)

def delete_employee(employee_code: str):
    """Xóa nhân viên bằng employee_code."""
    query = "DELETE FROM employees WHERE employee_code = %s"
    return _execute_query(query, params=(employee_code,), commit=True)

def search_employees(search_by: str, search_text: str) -> List[Dict[str, Any]]:
    """Tìm kiếm nhân viên (an toàn)."""
    # Chỉ cho phép tìm kiếm ở các cột này
    safe_columns = ['employee_code', 'first_name', 'last_name', 'email', 'phone_number']
    if search_by not in safe_columns:
        raise ValueError("Điều kiện tìm kiếm không hợp lệ")

    query = f"""
        SELECT e.*, p.title as position_title, d.name as department_name 
        FROM employees e
        LEFT JOIN positions p ON e.position_id = p.id
        LEFT JOIN departments d ON e.department_id = d.id
        WHERE e.{search_by} LIKE %s
        ORDER BY e.id
    """
    params = (f"%{search_text}%",) # Tìm kiếm %like%
    return _execute_query(query, params=params, fetch_all=True)