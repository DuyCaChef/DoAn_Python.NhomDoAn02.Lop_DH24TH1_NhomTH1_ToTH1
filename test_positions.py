"""
Test script để kiểm tra positions loading
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.database.employee_queries import EmployeeQueries

print("=" * 60)
print("TEST POSITIONS LOADING")
print("=" * 60)

try:
    emp_queries = EmployeeQueries()
    positions_data = emp_queries.get_all_positions()
    
    print(f"\n✅ Query thành công!")
    print(f"📊 Số lượng positions: {len(positions_data)}")
    print(f"📊 Type: {type(positions_data)}")
    
    if positions_data:
        print("\n📋 Danh sách positions:")
        print("-" * 60)
        
        positions_map = {}
        positions_list = []
        
        for i, pos in enumerate(positions_data, 1):
            pos_id = pos.get('id')
            pos_title = pos.get('title')
            dept_name = pos.get('department_name', '')
            
            display_text = f"{pos_title} ({dept_name})"
            positions_list.append(display_text)
            positions_map[pos_id] = display_text
            
            print(f"{i:2d}. ID={pos_id:2d} | {display_text}")
        
        print("\n" + "=" * 60)
        print(f"✅ positions_list: {len(positions_list)} items")
        print(f"✅ positions_map: {len(positions_map)} items")
        
        print("\n📦 positions_list sẽ được dùng cho ComboBox:")
        for item in positions_list[:5]:
            print(f"   - {item}")
        if len(positions_list) > 5:
            print(f"   ... và {len(positions_list) - 5} items khác")
            
        print("\n🗺️ positions_map (sample):")
        for pid, display in list(positions_map.items())[:5]:
            print(f"   {pid} -> {display}")
            
    else:
        print("❌ positions_data trống!")
        
except Exception as e:
    print(f"\n❌ LỖI: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST HOÀN TẤT")
print("=" * 60)
