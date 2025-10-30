"""Simple controller wrapper for employee operations."""

from typing import List

try:
    from app.database import queries as db_queries
    from app.models import employee as employee_model
except Exception:
    # Fallback: try package-root imports (when running as `QL_Nhan_Su_Python` package)
    try:
        from QL_Nhan_Su_Python.database import queries as db_queries  # type: ignore
        from QL_Nhan_Su_Python.models import employee as employee_model  # type: ignore
    except Exception:
        db_queries = None
        employee_model = None


class EmployeeController:
    """Controller class for handling employee operations."""
    
    def __init__(self):
        """Initialize employee controller."""
        pass
    
    def get_all_employees(self) -> List:
        """Get all employees from database."""
        return list_employees()
    
    def create_employee(self, employee_data: dict):
        """Create a new employee."""
        if db_queries is None:
            print("Warning: Database queries module not available")
            return None
        try:
            return db_queries.create_employee(**employee_data)
        except Exception as e:
            print(f"Error creating employee: {e}")
            return None
    
    def update_employee(self, employee_id: int, employee_data: dict):
        """Update employee information."""
        if db_queries is None:
            print("Warning: Database queries module not available")
            return None
        try:
            return db_queries.update_employee(employee_id, **employee_data)
        except Exception as e:
            print(f"Error updating employee: {e}")
            return None
    
    def delete_employee(self, employee_id: int):
        """Delete an employee."""
        if db_queries is None:
            print("Warning: Database queries module not available")
            return None
        try:
            return db_queries.delete_employee(employee_id)
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return None


def list_employees() -> List:
    """Return list of employees from database queries."""
    if db_queries is None or employee_model is None:
        return []
    rows = db_queries.get_all_employees()
    # try to use model factory if available
    result = []
    for r in rows:
        if hasattr(employee_model.Employee, 'from_db_row'):
            result.append(employee_model.Employee.from_db_row(r))
        else:
            # fallback: build with minimal mapping
            result.append(employee_model.Employee(
                id=r.get('id'),
                employee_code=r.get('employee_code'),
                first_name=r.get('first_name') or r.get('name', ''),
                last_name=r.get('last_name') or '',
                gender=r.get('gender', ''),
                date_of_birth=r.get('date_of_birth'),
                email=r.get('email'),
                phone_number=r.get('phone_number'),
                address=r.get('address'),
                hire_date=r.get('hire_date'),
                status=r.get('status', ''),
                department_name=r.get('department_name'),
                position_title=r.get('position_title'),
                manager_id=r.get('manager_id'),
            ))
    return result
