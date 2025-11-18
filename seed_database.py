"""
Script để seed database với dữ liệu mẫu đầy đủ
Bao gồm: Departments, Positions, Employees (với salary), Leave Requests
"""

from app.database.connection import create_connection
from datetime import date

def seed_all_data():
    """Seed tất cả dữ liệu mẫu vào database"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        print("="*70)
        print("🌱 BẮT ĐẦU SEED DATABASE")
        print("="*70)
        
        # XÓA DỮ LIỆU CŨ (theo thứ tự foreign key: child -> parent)
        print("\n🗑️  Xóa dữ liệu cũ...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM leave_requests WHERE id > 0")
        cursor.execute("DELETE FROM employees WHERE id > 0")
        cursor.execute("DELETE FROM positions WHERE id > 0")
        cursor.execute("DELETE FROM departments WHERE id > 0")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        print("  ✅ Đã xóa dữ liệu cũ")
        
        # 1. DEPARTMENTS
        print("\n📁 [1/4] Tạo Departments...")
        departments = [
            (1, 'IT'),
            (2, 'Marketing'),
            (3, 'Sales'),
            (4, 'HR'),
            (5, 'Finance'),
            (6, 'Operations')
        ]
        
        for dept in departments:
            cursor.execute("""
                INSERT INTO departments (id, name) 
                VALUES (%s, %s)
            """, dept)
        print(f"  ✅ Đã tạo {len(departments)} departments")
        
        # 2. POSITIONS
        print("\n💼 [2/4] Tạo Positions...")
        positions = [
            (1, 'IT Manager', 1),
            (2, 'Senior Developer', 1),
            (3, 'Junior Developer', 1),
            (4, 'Marketing Manager', 2),
            (5, 'Marketing Specialist', 2),
            (6, 'Sales Manager', 3),
            (7, 'Sales Executive', 3),
            (8, 'Sales Representative', 3),
            (9, 'Recruitment Specialist', 4),
            (10, 'HR Manager', 4),
            (11, 'HR Assistant', 4),
            (12, 'Finance Manager', 5),
            (13, 'Accountant', 5),
            (14, 'Operations Manager', 6),
            (15, 'Operations Coordinator', 6)
        ]
        
        for pos in positions:
            cursor.execute("""
                INSERT INTO positions (id, title, department_id) 
                VALUES (%s, %s, %s)
            """, pos)
        print(f"  ✅ Đã tạo {len(positions)} positions")
        
        # 3. EMPLOYEES (Với salary)
        print("\n👥 [3/4] Tạo Employees...")
        employees = [
            # IT Department (dept_id=1)
            (10, 'DIR001', 'Nguyễn', 'Văn An', 'Male', '1975-05-15', 'director@company.com', 
             50000000.00, '0901234567', '123 Q1, TP.HCM', '2020-01-01', 'Đang làm việc', 4, 10, None),
            
            (11, 'MGR_IT001', 'Trần', 'Văn Bình', 'Male', '1985-03-20', 'it_manager@company.com',
             50000000.00, '0902345678', '456 Q2, TP.HCM', '2020-02-01', 'Đang làm việc', 1, 1, 10),
            
            (17, 'EMP_IT001', 'Nguyễn', 'Văn Hải', 'Male', '1995-01-01', 'hai_nguyen@company.com',
             15000000.00, '0911111111', 'TP.HCM', '2021-01-01', 'Đang làm việc', 1, 2, 11),
            
            (18, 'EMP_IT002', 'Trần', 'Thị Hoa', 'Female', '1996-05-15', 'hoa_tran@company.com',
             15000000.00, '0922222222', 'TP.HCM', '2021-06-01', 'Đang làm việc', 1, 3, 11),
            
            # Marketing Department (dept_id=2)
            (12, 'MGR_MKT001', 'Lê', 'Thị Cúc', 'Female', '1987-08-10', 'mkt_manager@company.com',
             50000000.00, '0903456789', '789 Q3, TP.HCM', '2020-03-01', 'Đang làm việc', 2, 4, 10),
            
            (19, 'EMP_MKT001', 'Phạm', 'Văn Đức', 'Male', '1994-09-20', 'duc_pham@company.com',
             25000000.00, '0933333333', 'TP.HCM', '2022-01-01', 'Đang làm việc', 2, 5, 12),
            
            # Sales Department (dept_id=3)
            (13, 'MGR_SALES001', 'Hoàng', 'Văn Dũng', 'Male', '1986-11-05', 'sales_manager@company.com',
             50000000.00, '0904567890', '321 Q4, TP.HCM', '2020-04-01', 'Đang làm việc', 3, 6, 10),
            
            (20, 'EMP_SALES001', 'Võ', 'Thị Lan', 'Female', '1997-03-12', 'lan_vo@company.com',
             25000000.00, '0944444444', 'TP.HCM', '2022-06-01', 'Đang làm việc', 3, 7, 13),
            
            (21, 'EMP_SALES002', 'Đặng', 'Văn Nam', 'Male', '1998-07-08', 'nam_dang@company.com',
             15000000.00, '0955555555', 'TP.HCM', '2023-01-01', 'Đang làm việc', 3, 8, 13),
            
            # HR Department (dept_id=4) - includes Director
            (22, 'EMP_HR001', 'Bùi', 'Thị Oanh', 'Female', '1999-11-25', 'oanh_bui@company.com',
             25000000.00, '0966666666', 'TP.HCM', '2023-06-01', 'Đang làm việc', 4, 9, 10),
            
            # Finance Department (dept_id=5)
            (14, 'MGR_FIN001', 'Ngô', 'Văn Em', 'Male', '1984-02-28', 'finance_manager@company.com',
             50000000.00, '0905678901', '654 Q5, TP.HCM', '2020-05-01', 'Đang làm việc', 5, 12, 10),
            
            (23, 'EMP_FIN001', 'Duy', '', 'Male', '2000-04-15', 'duy@gmail.com',
             25000000.00, '0977777777', 'TP.HCM', '2024-01-01', 'Đang làm việc', 5, 13, 14),
            
            # Operations Department (dept_id=6)
            (15, 'MGR_OPS001', 'Phan', 'Thị Phương', 'Female', '1988-06-12', 'ops_manager@company.com',
             50000000.00, '0906789012', '987 Q6, TP.HCM', '2020-06-01', 'Đang làm việc', 6, 14, 10),
        ]
        
        for emp in employees:
            cursor.execute("""
                INSERT INTO employees 
                (id, employee_code, last_name, first_name, gender, date_of_birth, email, 
                 salary, phone_number, address, hire_date, status, department_id, position_id, manager_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, emp)
        print(f"  ✅ Đã tạo {len(employees)} employees (với salary)")
        
        # 4. LEAVE REQUESTS
        print("\n📝 [4/4] Tạo Leave Requests...")
        leave_requests = [
            # Employee 17 (Nguyễn Văn Hải) - (employee_id, leave_type, start, end, total_days, reason, status)
            (17, 'annual', '2025-12-01', '2025-12-05', 5, 'Về quê nghỉ lễ cuối năm cùng gia đình', 'pending'),
            (17, 'sick', '2025-11-25', '2025-11-26', 2, 'Bị cảm cúm, cần nghỉ ngơi để phục hồi sức khỏe', 'pending'),
            (17, 'personal', '2025-12-15', '2025-12-15', 1, 'Đi làm thủ tục giấy tờ cá nhân', 'approved'),
            
            # Employee 18 (Trần Thị Hoa)
            (18, 'annual', '2025-12-10', '2025-12-14', 5, 'Nghỉ phép thăm gia đình', 'pending'),
            (18, 'sick', '2025-11-20', '2025-11-21', 2, 'Khám bệnh định kỳ', 'approved'),
            
            # Employee 19 (Phạm Văn Đức)
            (19, 'annual', '2025-12-20', '2025-12-27', 8, 'Nghỉ Tết Dương lịch', 'pending'),
            
            # Employee 20 (Võ Thị Lan)
            (20, 'personal', '2025-11-28', '2025-11-28', 1, 'Việc gia đình đột xuất', 'rejected'),
            
            # Employee 21 (Đặng Văn Nam)
            (21, 'annual', '2025-12-05', '2025-12-08', 4, 'Du lịch cùng bạn bè', 'approved'),
        ]
        
        for lr in leave_requests:
            cursor.execute("""
                INSERT INTO leave_requests 
                (employee_id, leave_type, start_date, end_date, total_days, reason, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """, lr)
        print(f"  ✅ Đã tạo {len(leave_requests)} leave requests")
        
        # Commit tất cả changes
        conn.commit()
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH SEED DATABASE!")
        print("="*70)
        
        # In summary
        print("\n📊 TỔNG KẾT:")
        print(f"  • Departments: {len(departments)}")
        print(f"  • Positions: {len(positions)}")
        print(f"  • Employees: {len(employees)}")
        print(f"  • Leave Requests: {len(leave_requests)}")
        
        print("\n👤 TÀI KHOẢN TEST:")
        print("  🔑 Director:")
        print("     Username: director@company.com")
        print("     Password: 123456")
        print()
        print("  🔑 IT Manager:")
        print("     Username: it_manager@company.com")
        print("     Password: 123456")
        print()
        print("  🔑 Employee (IT):")
        print("     Username: hai_nguyen@company.com")
        print("     Password: 123456")
        
        return True
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
        return False
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    print("\n🌱 SEED DATABASE - Tạo dữ liệu mẫu đầy đủ\n")
    success = seed_all_data()
    
    if success:
        print("\n✅ Bạn có thể chạy ứng dụng và đăng nhập bằng các tài khoản trên!")
    else:
        print("\n❌ Có lỗi xảy ra khi seed database. Vui lòng kiểm tra lại!")
