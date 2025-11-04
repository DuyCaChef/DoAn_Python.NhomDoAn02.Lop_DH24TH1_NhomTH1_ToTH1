"""
Script tạo MySQL users cho manager và user
"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Kết nối bằng root
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),  # root
    password=os.getenv('DB_PASSWORD')
)

cursor = conn.cursor()

print("=== TẠO MYSQL USERS ===\n")

# 1. Tạo user 'manager'
try:
    cursor.execute("DROP USER IF EXISTS 'manager'@'localhost'")
    cursor.execute("CREATE USER 'manager'@'localhost' IDENTIFIED BY 'manager123'")
    cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON quanlynhansu.* TO 'manager'@'localhost'")
    print("✅ Đã tạo MySQL user: manager@localhost")
except Exception as e:
    print(f"❌ Lỗi tạo manager: {e}")

# 2. Tạo user 'user'
try:
    cursor.execute("DROP USER IF EXISTS 'user'@'localhost'")
    cursor.execute("CREATE USER 'user'@'localhost' IDENTIFIED BY 'user123'")
    cursor.execute("GRANT SELECT ON quanlynhansu.* TO 'user'@'localhost'")
    print("✅ Đã tạo MySQL user: user@localhost")
except Exception as e:
    print(f"❌ Lỗi tạo user: {e}")

# Flush privileges
cursor.execute("FLUSH PRIVILEGES")
print("\n✅ Đã flush privileges")

# Kiểm tra lại
cursor.execute("SELECT user, host FROM mysql.user WHERE user IN ('admin', 'manager', 'user')")
mysql_users = cursor.fetchall()

print("\n=== DANH SÁCH MYSQL USERS ===")
for u in mysql_users:
    print(f"  - {u[0]}@{u[1]}")

cursor.close()
conn.close()

print("\n✅ Hoàn tất! Giờ có thể đăng nhập với:")
print("   - manager/manager123")
print("   - user/user123")
