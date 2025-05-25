# Ecommerce Project (Django)

Một dự án website thương mại điện tử đơn giản được xây dựng bằng Django, hỗ trợ đầy đủ các tính năng cơ bản như quản lý sản phẩm, giỏ hàng, đặt hàng, đánh giá, tìm kiếm, và chatbot hỗ trợ khách hàng.

## Mục lục

Tính năng

Yêu cầu hệ thống

Cài đặt

Sử dụng

Cấu trúc thư mục

Ghi chú

Đóng góp

Giấy phép

Tác giả

Tính năng

🔹 Quản lý sản phẩm & danh mục

🔹 Đăng ký, đăng nhập và quản lý người dùng

🔹 Giỏ hàng và đặt hàng trực tuyến

🔹 Quản lý đơn hàng & lịch sử mua hàng

🔹 Đánh giá sản phẩm (hỗ trợ upload ảnh)

🔹 Tìm kiếm và lọc nâng cao

🔹 Tích hợp chatbot hỗ trợ khách hàng (Google Gemini API)

🔹 Tích hợp Google Maps API hiển thị vị trí các cửa hàng trên bản đồ.



## Yêu cầu hệ thống

Python 3.12+

Django 5.x

Hệ điều hành: Windows, macOS hoặc Linux

SQLite (mặc định), có thể chuyển sang MySQL/PostgreSQL

Trình duyệt hiện đại (Chrome, Firefox,...)

 ## Cài đặt

## 1. Clone source code

` git clone <https://github.com/nguyenphuongtra/my_project_Django_ecommerce.git> `
` cd Project_ecommerce `

## 2. Tạo virtual environment

`python -m venv venv`
# Windows
`venv\Scripts\activate`
# macOS / Linux
`source venv/bin/activate`

## 3. Cài đặt các package cần thiết

`pip install -r requirements.txt`

Nếu chưa có file requirements.txt, bạn có thể tạo bằng:

`pip freeze > requirements.txt`

## 4. Khởi tạo cơ sở dữ liệu

`python manage.py migrate`

## 5. Tạo tài khoản admin

`python manage.py createsuperuser`

## 6. Chạy server

`python manage.py runserver`

Truy cập: http://127.0.0.1:8000

## Sử dụng

Truy cập trang admin: http://127.0.0.1:8000/admin/

Thêm dữ liệu mẫu: sử dụng giao diện admin hoặc tạo script riêng

Upload ảnh: đảm bảo thư mục media/ có quyền ghi

Sử dụng chatbot: cấu hình biến môi trường GEMINI_API_KEY

## Cấu trúc thư mục

Project_ecommerce/
│
├── accounts/        # Quản lý người dùng
├── cart/            # Chức năng giỏ hàng
├── orders/          # Xử lý đơn hàng
├── shop/            # Sản phẩm, danh mục, đánh giá, tìm kiếm, chatbot
├── media/           # Ảnh sản phẩm, review, avatar người dùng
├── static/          # CSS, JS, icon, ...
├── templates/       # Giao diện HTML (base.html, header, footer...)
├── manage.py        # Tập tin quản lý chính
├── requirements.txt # Danh sách thư viện cần thiết
└── db.sqlite3       # Cơ sở dữ liệu mặc định (SQLite)

Ghi chú

Đảm bảo media/ có quyền ghi để upload ảnh.

Để chatbot hoạt động, cần thêm Google Gemini API Key vào biến môi trường hoặc trong settings.py:

` GOOGLE_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")` 

Khi deploy lên production:

Cập nhật ALLOWED_HOSTS trong settings.py

Cấu hình static/media phù hợp

Bảo mật SECRET_KEY và thông tin nhạy cảm bằng biến môi trường

Cân nhắc sử dụng HTTPS, CSRF, CORS, v.v.

## Đóng góp

Chúng tôi hoan nghênh mọi đóng góp, đề xuất, và phản hồi!

## Fork dự án

Tạo nhánh mới: ` git checkout -b feature/ten-chuc-nang`

Commit thay đổi:` git commit -m "Thêm tính năng XYZ"`

Push lên nhánh của bạn:` git push origin feature/ten-chuc-nang`

Mở Pull Request

Giấy phép

Dự án được phân phối theo giấy phép MIT License. Xem thêm trong file LICENSE.

Tác giả: Nguyen Phuong Tra
Email: nguyenthanhtra.240805@gmail.com


