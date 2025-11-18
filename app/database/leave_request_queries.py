"""
Leave Request Queries
Xử lý các truy vấn liên quan đến yêu cầu nghỉ phép
"""
from app.database.connection import create_connection
from datetime import datetime


class LeaveRequestQueries:
    """Class xử lý queries cho leave requests"""
    
    @staticmethod
    def create_leave_request(employee_id, leave_type, start_date, end_date, total_days, reason):
        """
        Tạo yêu cầu nghỉ phép mới
        
        Args:
            employee_id: ID nhân viên
            leave_type: Loại nghỉ (annual, sick, unpaid, personal)
            start_date: Ngày bắt đầu (YYYY-MM-DD)
            end_date: Ngày kết thúc (YYYY-MM-DD)
            total_days: Tổng số ngày nghỉ
            reason: Lý do nghỉ
            
        Returns:
            tuple: (success: bool, message: str)
        """
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Map loại nghỉ tiếng Việt sang enum
            leave_type_map = {
                "Nghỉ phép năm": "annual",
                "Nghỉ ốm": "sick",
                "Nghỉ việc riêng": "personal",
                "Nghỉ không lương": "unpaid"
            }
            leave_type_enum = leave_type_map.get(leave_type, leave_type)
            
            # Lấy manager_id của nhân viên
            cursor.execute("""
                SELECT e.manager_id 
                FROM employees e
                WHERE e.id = %s
            """, (employee_id,))
            result = cursor.fetchone()
            manager_id = result[0] if result else None
            
            # Insert leave request
            query = """
                INSERT INTO leave_requests 
                (employee_id, manager_id, leave_type, start_date, end_date, 
                 total_days, reason, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending', NOW(), NOW())
            """
            
            cursor.execute(query, (
                employee_id, manager_id, leave_type_enum, 
                start_date, end_date, total_days, reason
            ))
            
            conn.commit()
            cursor.close()
            
            return True, "Tạo yêu cầu nghỉ phép thành công!"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi tạo yêu cầu: {str(e)}"
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_leave_requests_by_employee(employee_id):
        """
        Lấy danh sách yêu cầu nghỉ phép của nhân viên
        
        Args:
            employee_id: ID nhân viên
            
        Returns:
            list: Danh sách yêu cầu nghỉ phép
        """
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    lr.id,
                    lr.leave_type,
                    lr.start_date,
                    lr.end_date,
                    lr.total_days,
                    lr.reason,
                    lr.status,
                    lr.manager_note,
                    lr.created_at,
                    lr.updated_at,
                    CONCAT(m.first_name, ' ', m.last_name) as manager_name
                FROM leave_requests lr
                LEFT JOIN employees m ON lr.manager_id = m.id
                WHERE lr.employee_id = %s
                ORDER BY lr.created_at DESC
            """
            
            cursor.execute(query, (employee_id,))
            requests = cursor.fetchall()
            
            # Map enum sang tiếng Việt
            leave_type_map = {
                "annual": "Nghỉ phép năm",
                "sick": "Nghỉ ốm",
                "personal": "Nghỉ việc riêng",
                "unpaid": "Nghỉ không lương"
            }
            
            status_map = {
                "pending": "Chờ duyệt",
                "approved": "Đã duyệt",
                "rejected": "Đã từ chối"
            }
            
            for req in requests:
                req['leave_type_display'] = leave_type_map.get(req['leave_type'], req['leave_type'])
                req['status_display'] = status_map.get(req['status'], req['status'])
            
            cursor.close()
            return requests
            
        except Exception as e:
            print(f"Lỗi lấy danh sách yêu cầu: {e}")
            return []
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_pending_requests_for_manager(manager_id):
        """
        Lấy danh sách yêu cầu chờ duyệt của manager
        
        Args:
            manager_id: ID manager
            
        Returns:
            list: Danh sách yêu cầu chờ duyệt
        """
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    lr.id,
                    lr.employee_id,
                    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
                    e.employee_code,
                    lr.leave_type,
                    lr.start_date,
                    lr.end_date,
                    lr.total_days,
                    lr.reason,
                    lr.status,
                    lr.created_at
                FROM leave_requests lr
                INNER JOIN employees e ON lr.employee_id = e.id
                WHERE lr.manager_id = %s AND lr.status = 'pending'
                ORDER BY lr.created_at ASC
            """
            
            cursor.execute(query, (manager_id,))
            requests = cursor.fetchall()
            
            # Map enum sang tiếng Việt
            leave_type_map = {
                "annual": "Nghỉ phép năm",
                "sick": "Nghỉ ốm",
                "personal": "Nghỉ việc riêng",
                "unpaid": "Nghỉ không lương"
            }
            
            for req in requests:
                req['leave_type_display'] = leave_type_map.get(req['leave_type'], req['leave_type'])
            
            cursor.close()
            return requests
            
        except Exception as e:
            print(f"Lỗi lấy yêu cầu chờ duyệt: {e}")
            return []
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_all_requests_for_manager(manager_id, status_filter=None):
        """
        Lấy tất cả yêu cầu của manager (có thể filter theo status)
        
        Args:
            manager_id: ID manager
            status_filter: Lọc theo trạng thái (pending/approved/rejected) hoặc None
            
        Returns:
            list: Danh sách yêu cầu
        """
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    lr.id,
                    lr.employee_id,
                    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
                    e.employee_code,
                    lr.leave_type,
                    lr.start_date,
                    lr.end_date,
                    lr.total_days,
                    lr.reason,
                    lr.status,
                    lr.manager_note,
                    lr.created_at,
                    lr.updated_at
                FROM leave_requests lr
                INNER JOIN employees e ON lr.employee_id = e.id
                WHERE lr.manager_id = %s
            """
            
            params = [manager_id]
            
            if status_filter:
                query += " AND lr.status = %s"
                params.append(status_filter)
            
            query += " ORDER BY lr.created_at DESC"
            
            cursor.execute(query, params)
            requests = cursor.fetchall()
            
            # Map enum sang tiếng Việt
            leave_type_map = {
                "annual": "Nghỉ phép năm",
                "sick": "Nghỉ ốm",
                "personal": "Nghỉ việc riêng",
                "unpaid": "Nghỉ không lương"
            }
            
            status_map = {
                "pending": "Chờ duyệt",
                "approved": "Đã duyệt",
                "rejected": "Đã từ chối"
            }
            
            for req in requests:
                req['leave_type_display'] = leave_type_map.get(req['leave_type'], req['leave_type'])
                req['status_display'] = status_map.get(req['status'], req['status'])
            
            cursor.close()
            return requests
            
        except Exception as e:
            print(f"Lỗi lấy tất cả yêu cầu: {e}")
            return []
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def update_request_status(request_id, status, manager_id, manager_note=None):
        """
        Cập nhật trạng thái yêu cầu (approve/reject)
        
        Args:
            request_id: ID yêu cầu
            status: Trạng thái mới (approved/rejected)
            manager_id: ID manager duyệt
            manager_note: Ghi chú của manager
            
        Returns:
            tuple: (success: bool, message: str)
        """
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE leave_requests 
                SET status = %s, manager_note = %s, updated_at = NOW()
                WHERE id = %s AND manager_id = %s
            """
            
            cursor.execute(query, (status, manager_note, request_id, manager_id))
            
            if cursor.rowcount == 0:
                return False, "Không tìm thấy yêu cầu hoặc bạn không có quyền!"
            
            conn.commit()
            cursor.close()
            
            status_text = "duyệt" if status == "approved" else "từ chối"
            return True, f"Đã {status_text} yêu cầu thành công!"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Lỗi cập nhật: {str(e)}"
            
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_request_by_id(request_id):
        """
        Lấy thông tin chi tiết yêu cầu
        
        Args:
            request_id: ID yêu cầu
            
        Returns:
            dict: Thông tin yêu cầu hoặc None
        """
        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                    lr.*,
                    CONCAT(e.first_name, ' ', e.last_name) as employee_name,
                    CONCAT(m.first_name, ' ', m.last_name) as manager_name
                FROM leave_requests lr
                INNER JOIN employees e ON lr.employee_id = e.id
                LEFT JOIN employees m ON lr.manager_id = m.id
                WHERE lr.id = %s
            """
            
            cursor.execute(query, (request_id,))
            request = cursor.fetchone()
            cursor.close()
            
            return request
            
        except Exception as e:
            print(f"Lỗi lấy chi tiết yêu cầu: {e}")
            return None
            
        finally:
            if conn:
                conn.close()
