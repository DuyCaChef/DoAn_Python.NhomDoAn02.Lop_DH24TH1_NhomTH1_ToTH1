"""
Test ApprovalTab có load data không
"""
import sys
sys.path.insert(0, '/home/tuanhai/Downloads/DoAn_Python.NhomDoAn02.Lop_DH24TH1_NhomTH1_ToTH1')

from app.controllers.leave_request_controller import LeaveRequestController
from app.database.connection import create_connection

print("="*60)
print("TEST APPROVAL TAB - MANAGER")
print("="*60)

# Kiểm tra manager nào có yêu cầu
conn = create_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT DISTINCT lr.manager_id, 
           CONCAT(m.first_name, ' ', m.last_name) as manager_name,
           COUNT(*) as total_requests
    FROM leave_requests lr
    INNER JOIN employees m ON lr.manager_id = m.id
    GROUP BY lr.manager_id, manager_name
""")

managers = cursor.fetchall()
print(f"\nManager có yêu cầu:")
for mgr in managers:
    print(f"  Manager ID: {mgr['manager_id']} ({mgr['manager_name']}) - {mgr['total_requests']} yêu cầu")

cursor.close()
conn.close()

# Test controller
if managers:
    test_manager_id = managers[0]['manager_id']
    print(f"\n{'='*60}")
    print(f"TEST với Manager ID = {test_manager_id}")
    print("="*60)
    
    controller = LeaveRequestController()
    
    # Test pending
    print("\n1. get_pending_requests_for_approval():")
    pending = controller.get_pending_requests_for_approval(test_manager_id)
    print(f"   Số yêu cầu pending: {len(pending)}")
    for req in pending:
        print(f"   - ID: {req['id']}, Employee: {req['employee_name']}, Type: {req['leave_type_display']}")
    
    # Test all
    print("\n2. get_all_requests_for_manager():")
    all_req = controller.get_all_requests_for_manager(test_manager_id)
    print(f"   Tổng số yêu cầu: {len(all_req)}")
    
    # Test filter
    print("\n3. get_all_requests_for_manager() với filter 'Chờ duyệt':")
    filtered = controller.get_all_requests_for_manager(test_manager_id, "Chờ duyệt")
    print(f"   Số yêu cầu: {len(filtered)}")

print("\n" + "="*60)
print("HOÀN THÀNH")
print("="*60)
