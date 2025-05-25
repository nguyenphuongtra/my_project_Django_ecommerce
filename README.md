Dự án Thương mại điện tử Django
Giới thiệu chung
Đây là một dự án website thương mại điện tử mạnh mẽ và linh hoạt, được phát triển bằng framework Django. Dự án cung cấp đầy đủ các chức năng cần thiết cho một nền tảng mua sắm trực tuyến, từ quản lý sản phẩm đến tương tác với khách hàng, nhằm mang lại trải nghiệm người dùng mượt mà và hiệu quả. Điểm nổi bật là tích hợp Google Maps API để nâng cao trải nghiệm địa lý và AI Chatbot sử dụng Gemini 1.5 Flash Pro để hỗ trợ khách hàng thông minh.

Các tính năng chính
Dự án được trang bị các module và tính năng cốt lõi sau:

Quản lý sản phẩm và danh mục:

Thêm, sửa, xóa sản phẩm với các thông tin chi tiết (tên, mô tả, giá, số lượng, hình ảnh).

Phân loại sản phẩm theo danh mục để dễ dàng quản lý và tìm kiếm.

Quản lý người dùng:

Hệ thống đăng ký và đăng nhập an toàn.

Quản lý hồ sơ người dùng (profile).

Giỏ hàng và đặt hàng:

Thêm, xóa, cập nhật số lượng sản phẩm trong giỏ hàng.

Quy trình đặt hàng đơn giản, dễ sử dụng.

Lưu trữ lịch sử đơn hàng cho từng người dùng.

Đánh giá sản phẩm:

Người dùng có thể viết đánh giá và xếp hạng sản phẩm.

Hỗ trợ tải lên hình ảnh kèm theo đánh giá.

Tìm kiếm và lọc:

Chức năng tìm kiếm sản phẩm theo từ khóa.

Tùy chọn lọc sản phẩm theo danh mục, giá cả, v.v.

Tích hợp Google Maps API:

Hiển thị vị trí các cửa hàng trên bản đồ.

Hỗ trợ chọn địa chỉ giao hàng dễ dàng hơn thông qua tương tác bản đồ. (Bạn có thể thêm các chức năng khác nếu có, ví dụ: tính toán khoảng cách/phí ship, định vị người dùng, v.v.)

AI Chatbot hỗ trợ khách hàng (Gemini 1.5 Flash Pro):

Tích hợp chatbot thông minh sử dụng Gemini 1.5 Flash Pro để cung cấp hỗ trợ tức thì.

Có khả năng trả lời các câu hỏi thường gặp, hướng dẫn mua sắm, và hỗ trợ giải đáp thắc mắc của khách hàng một cách linh hoạt và hiệu quả.

Quản trị hệ thống:

Giao diện quản trị Django mạnh mẽ để quản lý toàn bộ dữ liệu (sản phẩm, đơn hàng, người dùng, đánh giá).

Yêu cầu hệ thống
Để chạy dự án, bạn cần có các môi trường sau:

Hệ điều hành: Windows, Linux hoặc macOS.

Python: Phiên bản 3.12 trở lên.

Django: Phiên bản 5.x.

Cơ sở dữ liệu: Mặc định sử dụng SQLite. Có thể dễ dàng cấu hình để sử dụng MySQL hoặc PostgreSQL.

Hướng dẫn cài đặt và chạy dự án
Thực hiện theo các bước sau để thiết lập và chạy dự án trên máy cục bộ của bạn:

Clone mã nguồn:
Mở Terminal hoặc PowerShell và thực hiện lệnh sau để sao chép mã nguồn từ kho lưu trữ của bạn:

```git clone  cd Project_ecommerce`



Tạo và kích hoạt môi trường ảo (Virtual Environment):
Môi trường ảo giúp cô lập các gói thư viện của dự án, tránh xung đột với các dự án Python khác.

```python -m venv venv .\venv\Scripts\activate` # Đối với Windows

source venv/bin/activate # Đối với Linux/macOS


Cài đặt các gói thư viện cần thiết:
Dự án sử dụng các gói thư viện được liệt kê trong file requirements.txt. Nếu file này chưa tồn tại, bạn có thể tạo nó sau khi đã cài đặt các gói cần thiết bằng lệnh pip freeze > requirements.txt.

```pip install -r requirements.txt`



Chạy migrations database:
Áp dụng các thay đổi từ models vào cơ sở dữ liệu của bạn.

```python manage.py migrate`



Tạo tài khoản quản trị (Superuser):
Tạo một tài khoản admin để truy cập vào trang quản trị Django.

```python manage.py createsuperuser`


Làm theo hướng dẫn trên màn hình để nhập tên người dùng, email và mật khẩu.


Chạy máy chủ phát triển (Development Server):
Khởi động máy chủ cục bộ để truy cập website.

```python manage.py runserver`



Tru cập website:
Mở trình duyệt web và truy cập địa chỉ: http://127.0.0.1:8000/

Cấu trúc thư mục chính
Dự án được tổ chức thành các ứng dụng Django riêng biệt, mỗi ứng dụng chịu trách nhiệm cho một phần chức năng cụ thể:

accounts/ : Quản lý người dùng, bao gồm đăng ký, đăng nhập và hồ sơ cá nhân.

cart/     : Xử lý các chức năng liên quan đến giỏ hàng của người dùng.

orders/   : Quản lý quy trình đặt hàng và lưu trữ lịch sử các đơn hàng.

shop/     : Chứa logic cho sản phẩm, danh mục, đánh giá, chức năng tìm kiếm, và tích hợp chatbot.

media/    : Nơi lưu trữ các tệp tải lên như ảnh sản phẩm, ảnh đánh giá và avatar người dùng.

static/   : Chứa các tệp tĩnh như CSS, JavaScript và hình ảnh không thay đổi.

templates/: Chứa các mẫu HTML chung của dự án (ví dụ: base.html, header.html, footer.html).

Một số lệnh quản trị hữu ích
Tru cập trang quản trị Django:
Sau khi chạy server, bạn có thể truy cập trang quản trị tại: http://127.0.0.1:8000/admin/
Sử dụng tài khoản superuser đã tạo ở bước 5 để đăng nhập.

Thêm dữ liệu mẫu:
Bạn có thể thêm dữ liệu sản phẩm, danh mục, người dùng... thông qua giao diện admin hoặc viết các script riêng để tự động thêm dữ liệu.

Ghi chú quan trọng và Cấu hình API
Quyền ghi cho thư mục media/: Để chức năng tải ảnh lên (ảnh sản phẩm, ảnh review) hoạt động, đảm bảo rằng thư mục media/ của dự án có quyền ghi.

Cấu hình API Key Google Maps: Bạn cần có một API Key Google Maps để các chức năng bản đồ hoạt động. Key này nên được lưu trữ trong biến môi trường hoặc trong file settings.py của Django (đảm bảo bảo mật và không đưa trực tiếp lên Git).

Cấu hình API Key Gemini 1.5 Flash Pro: Tương tự, để chatbot hoạt động, bạn cần cấu hình API Key Gemini 1.5 Flash Pro của Google. Key này cũng nên được lưu trữ một cách an toàn.

Triển khai lên máy chủ thật (Deployment): Khi triển khai dự án lên môi trường production, bạn cần thực hiện các bước sau:

Chỉnh sửa ALLOWED_HOSTS trong settings.py để bao gồm tên miền của bạn.

Cấu hình phục vụ các tệp static/ và media/ một cách đúng đắn (thường thông qua Nginx hoặc Apache).

Đảm bảo SECRET_KEY được bảo mật tuyệt đối và tạo một khóa mới, phức tạp.

Chuyển DEBUG = False trong settings.py.

Sử dụng một cơ sở dữ liệu mạnh mẽ hơn như PostgreSQL hoặc MySQL.

Đóng góp
Chúng tôi rất hoan nghênh mọi đóng góp để cải thiện dự án này! Nếu bạn phát hiện lỗi, có ý tưởng mới hoặc muốn thêm tính năng, xin vui lòng:

Mở một Issue để báo cáo lỗi hoặc đề xuất tính năng.

Tạo một Pull Request với các thay đổi của bạn.

Tác giả: Nguyen Phuong Tra