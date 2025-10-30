"""Seed database with minimal mock data using project's queries helpers."""
from QL_Nhan_Su_Python.database import employee_queries


def main():
    print('Seeding mock data...')
    emp_id = employee_queries.seed_mock_data()
    print('Inserted employee id:', emp_id)


if __name__ == '__main__':
    main()
