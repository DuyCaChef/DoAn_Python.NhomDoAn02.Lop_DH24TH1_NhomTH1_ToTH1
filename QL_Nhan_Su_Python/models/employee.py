"""Employee model for HRM demo."""
from dataclasses import dataclass


@dataclass
class Employee:
	id: int
	name: str
	email: str = ""

	@staticmethod
	def from_row(row):
		# row can be dict or sqlite3.Row
		if isinstance(row, dict):
			return Employee(id=row.get("id", 0), name=row.get("name", ""), email=row.get("email", ""))
		return Employee(id=row["id"], name=row["name"], email=row.get("email", ""))
"""Employee model for HRM demo."""
from dataclasses import dataclass


@dataclass
class Employee:
	id: int
	name: str
	email: str = ""

	@staticmethod
	def from_row(row):
		# row can be dict or sqlite3.Row
		if isinstance(row, dict):
			return Employee(id=row.get("id", 0), name=row.get("name", ""), email=row.get("email", ""))
		return Employee(id=row["id"], name=row["name"], email=row.get("email", ""))

