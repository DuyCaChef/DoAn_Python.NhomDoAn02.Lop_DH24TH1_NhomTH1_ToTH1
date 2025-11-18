"""
Leave Request Controller
Xử lý logic nghiệp vụ cho yêu cầu nghỉ phép
"""
from datetime import datetime, date
from app.database.leave_request_queries import LeaveRequestQueries


class LeaveRequestController:
    """Controller xử lý nghiệp vụ leave request"""
    
    def __init__(self):
        self.queries = LeaveRequestQueries()
    
    def create_request(self, employee_id, leave_type, start_date_str, end_date_str, reason):
        """
        Tạo yêu cầu nghỉ phép mới với validation
        
        Args:
            employee_id: ID nhân viên
            leave_type: Loại nghỉ phép (tiếng Việt)
            start_date_str: Ngày bắt đầu (string YYYY-MM-DD)
            end_date_str: Ngày kết thúc (string YYYY-MM-DD)
            reason: Lý do nghỉ
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Validate input
            if not all([employee_id, leave_type, start_date_str, end_date_str, reason]):
                return False, "Vui lòng điền đầy đủ thông tin!"
            
            # Validate reason length
            if len(reason.strip()) < 10:
                return False, "Lý do phải có ít nhất 10 ký tự!"
            
            # Parse dates
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                return False, "Định dạng ngày không hợp lệ! (YYYY-MM-DD)"
            
            # Validate date logic
            if start_date > end_date:
                return False, "Ngày bắt đầu phải trước hoặc bằng ngày kết thúc!"
            
            if start_date < date.today():
                return False, "Ngày bắt đầu không được ở quá khứ!"
            
            # Calculate total days
            total_days = (end_date - start_date).days + 1
            
            if total_days > 30:
                return False, "Không thể nghỉ quá 30 ngày trong một lần!"
            
            # Create request
            return self.queries.create_leave_request(
                employee_id=employee_id,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                total_days=total_days,
                reason=reason.strip()
            )
            
        except Exception as e:
            return False, f"Lỗi xử lý: {str(e)}"
    
    def get_my_requests(self, employee_id):
        """
        Lấy danh sách yêu cầu của nhân viên
        
        Args:
            employee_id: ID nhân viên
            
        Returns:
            list: Danh sách yêu cầu
        """
        return self.queries.get_leave_requests_by_employee(employee_id)
    
    def get_pending_requests_for_approval(self, manager_id):
        """
        Lấy danh sách yêu cầu chờ duyệt cho manager
        
        Args:
            manager_id: ID manager
            
        Returns:
            list: Danh sách yêu cầu chờ duyệt
        """
        return self.queries.get_pending_requests_for_manager(manager_id)
    
    def get_all_requests_for_manager(self, manager_id, status_filter=None):
        """
        Lấy tất cả yêu cầu của manager (có filter)
        
        Args:
            manager_id: ID manager
            status_filter: Filter status (pending/approved/rejected)
            
        Returns:
            list: Danh sách yêu cầu
        """
        # Map Vietnamese to enum
        status_map = {
            "Chờ duyệt": "pending",
            "Đã duyệt": "approved",
            "Từ chối": "rejected"
        }
        
        status_enum = status_map.get(status_filter, None) if status_filter else None
        return self.queries.get_all_requests_for_manager(manager_id, status_enum)
    
    def approve_request(self, request_id, manager_id, note=None):
        """
        Duyệt yêu cầu nghỉ phép
        
        Args:
            request_id: ID yêu cầu
            manager_id: ID manager
            note: Ghi chú (tùy chọn)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.queries.update_request_status(
            request_id=request_id,
            status="approved",
            manager_id=manager_id,
            manager_note=note
        )
    
    def reject_request(self, request_id, manager_id, note):
        """
        Từ chối yêu cầu nghỉ phép
        
        Args:
            request_id: ID yêu cầu
            manager_id: ID manager
            note: Lý do từ chối (bắt buộc)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not note or len(note.strip()) < 5:
            return False, "Vui lòng nhập lý do từ chối (ít nhất 5 ký tự)!"
        
        return self.queries.update_request_status(
            request_id=request_id,
            status="rejected",
            manager_id=manager_id,
            manager_note=note.strip()
        )
    
    def get_request_detail(self, request_id):
        """
        Lấy chi tiết yêu cầu
        
        Args:
            request_id: ID yêu cầu
            
        Returns:
            dict: Thông tin yêu cầu
        """
        return self.queries.get_request_by_id(request_id)
    
    def can_edit_request(self, request_id, employee_id):
        """
        Kiểm tra xem nhân viên có thể sửa/xóa yêu cầu không
        
        Args:
            request_id: ID yêu cầu
            employee_id: ID nhân viên
            
        Returns:
            tuple: (can_edit: bool, message: str)
        """
        request = self.queries.get_request_by_id(request_id)
        
        if not request:
            return False, "Không tìm thấy yêu cầu!"
        
        if request['employee_id'] != employee_id:
            return False, "Bạn không có quyền với yêu cầu này!"
        
        if request['status'] != 'pending':
            return False, "Chỉ có thể chỉnh sửa yêu cầu đang chờ duyệt!"
        
        return True, "OK"
