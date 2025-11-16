"""
Loading Overlay Component
Hiển thị GIF loading với overlay tối màu khi đang xử lý
"""
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import os
from typing import Optional


class LoadingOverlay:
    """
    Component hiển thị loading animation với overlay tối màu
    
    Usage:
        # Hiển thị loading
        loading = LoadingOverlay(parent_window)
        loading.show()
        
        # Ẩn loading sau khi xong
        loading.hide()
    """
    
    def __init__(self, parent: ctk.CTk, message: str = "Đang xử lý..."):
        """
        Args:
            parent: Cửa sổ cha (CTk window hoặc Toplevel)
            message: Text hiển thị dưới GIF
        """
        self.parent = parent
        self.message = message
        
        # Overlay frame (tối màu)
        self.overlay = None
        self.gif_label = None
        self.text_label = None
        
        # Animation data
        self.original_gif = None  # GIF gốc
        self.gif_frames = []
        self.current_frame = 0
        self.animation_job = None
        
        # Load GIF frames
        self._load_gif()
    
    def _load_gif(self):
        """Load tất cả frames từ load.gif và scale theo màn hình"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            gif_path = os.path.join(current_dir, '..', '..', 'access', 'LoadIndicator', 'load.gif')
            gif_path = os.path.abspath(gif_path)
            
            if not os.path.exists(gif_path):
                print(f"❌ Không tìm thấy GIF tại: {gif_path}")
                return
            
            # Lấy kích thước màn hình
            # Sẽ update lại khi show() được gọi
            self.original_gif = Image.open(gif_path)
            
            print(f"✅ Đã load GIF từ {gif_path}")

        except Exception as e:
            print(f"❌ Lỗi khi load GIF: {e}")
            self.original_gif = None
    
    def show(self):
        """Hiển thị loading overlay"""
        if self.overlay is not None:
            return  # Đã hiển thị rồi
        
        # Tạo overlay frame (phủ toàn bộ parent)
        self.overlay = ctk.CTkFrame(
            self.parent,
            fg_color=("gray90", "gray10"),
            corner_radius=0
        )
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Load GIF frames theo kích thước màn hình
        if self.original_gif and not self.gif_frames:
            # Lấy kích thước màn hình TRỰC TIẾP
            screen_width = self.parent.winfo_screenwidth()
            screen_height = self.parent.winfo_screenheight()
            
            # FORCE GIF size = 90% kích thước màn hình (rất lớn)
            gif_size = int(min(screen_width, screen_height) * 0.9)

            print(f"📐 Scaling GIF to {gif_size}x{gif_size}px (Screen: {screen_width}x{screen_height})")
            
            for frame in ImageSequence.Iterator(self.original_gif):
                frame_resized = frame.copy().resize((gif_size, gif_size), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(frame_resized)
                self.gif_frames.append(photo)
        
        # Label hiển thị GIF - FULLSCREEN (không dùng container)
        if self.gif_frames:
            self.gif_label = ctk.CTkLabel(
                self.overlay,
                text="",
                fg_color="transparent"
            )
            self.gif_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Bắt đầu animation
            self._animate()
        
        # # Label hiển thị text - ĐÈ LÊN TRÊN GIF Ở PHÍA DƯỚI
        # self.text_label = ctk.CTkLabel(
        #     self.overlay,
        #     text=self.message,
        #     font=ctk.CTkFont(size=40, weight="bold"),  # Font RẤT LỚN
        #     text_color=("#0A3871", "white")
        #     # Không dùng rgba vì CustomTkinter không hỗ trợ
        # )
        # # Đặt text ở PHÍA DƯỚI GIF (70% từ trên xuống)
        # self.text_label.place(relx=0.5, rely=0.75, anchor="center")
        
        # Đưa overlay lên top
        self.overlay.lift()
    
    def hide(self):
        """Ẩn loading overlay"""
        # Dừng animation
        if self.animation_job:
            self.parent.after_cancel(self.animation_job)
            self.animation_job = None
        
        # Xóa overlay
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None
            self.gif_label = None
            self.text_label = None
        
        # Reset gif frames để load lại lần sau (vì kích thước có thể khác)
        self.gif_frames = []
        self.current_frame = 0
    
    def _animate(self):
        """Animate GIF frames"""
        if not self.gif_frames or not self.gif_label:
            return
        
        # Hiển thị frame hiện tại
        frame = self.gif_frames[self.current_frame]
        self.gif_label.configure(image=frame)
        self.gif_label.image = frame  # Keep reference
        
        # Chuyển sang frame tiếp theo
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        
        # Schedule frame tiếp theo (50ms = ~20 FPS)
        self.animation_job = self.parent.after(50, self._animate)
    
    def update_message(self, new_message: str):
        """Cập nhật text message"""
        self.message = new_message
        if self.text_label:
            self.text_label.configure(text=new_message)


# Utility function để sử dụng nhanh
def show_loading(parent: ctk.CTk, message: str = "Đang xử lý...") -> LoadingOverlay:
    """
    Helper function để show loading nhanh
    
    Usage:
        loading = show_loading(self, "Đang đăng nhập...")
        # ... do work ...
        loading.hide()
    """
    loading = LoadingOverlay(parent, message)
    loading.show()
    return loading
