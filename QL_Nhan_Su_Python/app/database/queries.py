"""MySQL database queries for HRM project."""
from typing import List, Dict, Any, Optional
from . import db_init


def _row_to_dict(cursor, row) -> Dict[str, Any]:
    """Convert MySQL cursor row to dictionary."""
    if hasattr(cursor, 'column_names'):
        columns = cursor.column_names
        return {columns[i]: row[i] for i in range(len(columns))}
    return {}


def get_all_employees() -> List[Dict[str, Any]]:
    """Fetch all employees with basic information."""
    conn = db_init.get_connection()
    try:
        cur = conn.cursor()
        query = """
        SELECT 
            e.id, e.employee_code, e.first_name, e.last_name, e.gender,
            e.date_of_birth, e.email, e.phone_number, e.address, 
            e.hire_date, e.status, e.salary,
            d.name as department_name,
            p.title as position_title,
            e.manager_id
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        ORDER BY e.id
        """
        cur.execute(query)
        rows = [_row_to_dict(cur, row) for row in cur.fetchall()]
        return rows
    finally:
        conn.close()


def get_employee_by_id(employee_id: int) -> Optional[Dict[str, Any]]:
    """Fetch single employee by ID."""
    conn = db_init.get_connection()
    try:
        cur = conn.cursor()
        query = """
        SELECT 
            e.id, e.employee_code, e.first_name, e.last_name, e.gender,
            e.date_of_birth, e.email, e.phone_number, e.address, 
            e.hire_date, e.status, e.salary,
            d.name as department_name,
            p.title as position_title,
            e.manager_id
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        WHERE e.id = %s
        """
        cur.execute(query, (employee_id,))
        row = cur.fetchone()
        return _row_to_dict(cur, row) if row else None
    finally:
        conn.close()


def create_employee(
    first_name: str,
    last_name: str = "",
    gender: str = "",
    date_of_birth: str = None,  # 'YYYY-MM-DD'
    email: str = "",
    phone_number: str = None,
    address: str = None,
    hire_date: str = None,  # 'YYYY-MM-DD', defaults to today
    status: str = "Probation",
    department_id: int = None,
    position_id: int = None,
    manager_id: int = None,
    employee_code: str = None,
    salary: float = 0.0,  # Thêm tham số salary
) -> Optional[int]:
    """Create new employee and return the new ID."""
    conn = db_init.get_connection()
    try:
        # Auto-generate employee code if not provided
        if employee_code is None:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as count FROM employees")
            count = cur.fetchone()[0]
            employee_code = f"EMP{count + 1:04d}"
        
        cur = conn.cursor()
        query = """
        INSERT INTO employees 
        (employee_code, first_name, last_name, gender, date_of_birth, 
         email, phone_number, address, hire_date, status, 
         department_id, position_id, manager_id, salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            employee_code, first_name, last_name, gender, date_of_birth,
            email, phone_number, address, hire_date, status,
            department_id, position_id, manager_id, salary
        )
        cur.execute(query, values)
        conn.commit()
        return cur.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_employee(
    employee_id: int,
    **kwargs
) -> bool:
    """Update employee information."""
    conn = db_init.get_connection()
    try:
        # Build dynamic update query
        update_fields = []
        values = []
        
        allowed_fields = [
            'employee_code', 'first_name', 'last_name', 'gender', 
            'date_of_birth', 'email', 'phone_number', 'address', 
            'hire_date', 'status', 'department_id', 'position_id', 'manager_id', 'salary'
        ]
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                update_fields.append(f"{field} = %s")
                values.append(value)
        
        if not update_fields:
            return False
            
        values.append(employee_id)
        
        cur = conn.cursor()
        query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = %s"
        cur.execute(query, values)
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def delete_employee(employee_id: int) -> bool:
    """Delete employee by ID."""
    conn = db_init.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_all_departments() -> List[Dict[str, Any]]:
    """Fetch all departments."""
    conn = db_init.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM departments ORDER BY name")
        return [_row_to_dict(cur, row) for row in cur.fetchall()]
    finally:
        conn.close()


def get_all_positions() -> List[Dict[str, Any]]:
    """Fetch all positions."""
    conn = db_init.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, title, description FROM positions ORDER BY title")
        return [_row_to_dict(cur, row) for row in cur.fetchall()]
    finally:
        conn.close()

