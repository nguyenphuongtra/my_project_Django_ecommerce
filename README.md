# Ecommerce Project (Django)

## Giới thiệu
Đây là dự án website thương mại điện tử được xây dựng bằng Django, hỗ trợ các chức năng cơ bản như:
- Quản lý sản phẩm, danh mục
- Đăng ký/đăng nhập người dùng
- Giỏ hàng, đặt hàng, lịch sử đơn hàng
- Đánh giá sản phẩm, upload ảnh đánh giá
- Tìm kiếm, lọc, chatbot hỗ trợ khách hàng

## Yêu cầu hệ thống
- Python 3.12+
- Django 5.x
- Windows (hoặc Linux/MacOS)
- SQLite (mặc định), có thể chuyển sang MySQL/PostgreSQL

## Cài đặt
1. **Clone source code:**
   ```powershell
   git clone <link-repo-cua-ban>
   cd Project_ecommerce
   ```
2. **Tạo virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Cài đặt các package:**
   ```powershell
   pip install -r requirements.txt
   ```
   (Nếu chưa có file `requirements.txt`, hãy tự tạo bằng lệnh `pip freeze > requirements.txt` sau khi cài đủ package)

4. **Chạy migrate database:**
   ```powershell
   python manage.py migrate
   ```
5. **Tạo tài khoản admin:**
   ```powershell
   python manage.py createsuperuser
   ```
6. **Chạy server:**
   ```powershell
   python manage.py runserver
   ```
7. Truy cập website tại: http://127.0.0.1:8000/

## Cấu trúc thư mục chính
- `accounts/` : Quản lý người dùng, đăng ký/đăng nhập, profile
- `cart/`     : Chức năng giỏ hàng
- `orders/`   : Đặt hàng, lịch sử đơn hàng
- `shop/`     : Sản phẩm, danh mục, đánh giá, tìm kiếm, chatbot
- `media/`    : Ảnh sản phẩm, ảnh review, avatar user
- `static/`   : CSS, JS, dữ liệu tĩnh
- `templates/`: Giao diện chung (base, header, footer)

## Một số lệnh quản trị
- Truy cập admin: http://127.0.0.1:8000/admin/
- Thêm dữ liệu mẫu: Có thể dùng admin hoặc tạo script riêng

## Ghi chú
- Để upload ảnh, thư mục `media/` phải có quyền ghi.
- Để chatbot hoạt động, cần cấu hình API key Google Gemini trong biến môi trường hoặc settings.
- Nếu muốn deploy lên server thật, cần chỉnh sửa `ALLOWED_HOSTS`, cấu hình static/media, bảo mật secret key...

## Đóng góp
Mọi đóng góp, báo lỗi hoặc ý tưởng mới đều được hoan nghênh!

---
**Tác giả:** Nguyen Phuong Tra
