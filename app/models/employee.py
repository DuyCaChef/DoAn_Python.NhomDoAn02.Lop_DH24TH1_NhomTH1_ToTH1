# app/models/employee.py

from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any

@dataclass
class Employee:
    """
    Lớp đại diện cho một đối tượng Nhân viên, sử dụng dataclass để ngắn gọn hơn.
    """
    id: int
    employee_code: str
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    email: str
    phone_number: Optional[str]
    address: Optional[str]
    hire_date: date
    status: str
    department_name: Optional[str]
    position_title: Optional[str]
    manager_id: Optional[int]

    def get_full_name(self) -> str:
        """Trả về họ và tên đầy đủ."""
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def from_db_row(row: Dict[str, Any]) -> "Employee":
        """
        Phương thức factory để tạo một đối tượng Employee từ một hàng dữ liệu 
        (dạng dictionary) trả về từ database.
        """
        return Employee(
            id=row.get("id"),
            employee_code=row.get("employee_code"),
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
            gender=row.get("gender"),
            date_of_birth=row.get("date_of_birth"),
            email=row.get("email"),
            phone_number=row.get("phone_number"),
            address=row.get("address"),
            hire_date=row.get("hire_date"),
            status=row.get("status"),
            department_name=row.get("department_name"),
            position_title=row.get("position_title"),
            manager_id=row.get("manager_id")
        )

