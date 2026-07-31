---
title: "Worklog Tuần 5"
date: 2026-07-13
weight: 5
chapter: false
pre: " <b> 1.5. </b> "
reportTableColumns:
  - Thứ
  - Công việc
  - Ngày hoàn thành
reportType: worklog
---

### Mục tiêu tuần 5:

* Tìm hiểu kiến trúc Serverless Web Application (AWS Lambda, API Gateway) và kỹ thuật đóng gói ứng dụng với Docker & ECR.
* Phát triển hệ thống Backend RESTful APIs (FastAPI) cho dự án CodExecute, tích hợp xác thực JWT và kết nối DynamoDB.

### Các công việc cần triển khai trong tuần này:
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Tìm hiểu kiến trúc Serverless Web API: Mangum ASGI Adapter, API Gateway HTTP API Proxy Integration | 13/07/2026 | 13/07/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html> |
| 3 | - Tìm hiểu cơ chế xác thực JWT Token & đăng nhập qua OAuth Providers (Google/GitHub) | 14/07/2026 | 14/07/2026 | <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html> |
| 4 | - **Thực hành:** <br>&emsp; + Đóng gói ứng dụng FastAPI backend thành Container Image và đẩy lên AWS ECR repository <br>&emsp; + Tạo hàm AWS Lambda (API Handler) từ ECR Container Image | 15/07/2026 | 15/07/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html> |
| 5 | - **Thực hành:** <br>&emsp; + Tạo API Gateway HTTP API và liên kết với Lambda API Handler <br>&emsp; + Cấu hình CORS policy cho phép kết nối từ React Frontend | 16/07/2026 | 16/07/2026 | <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html> |
| 6 | - **Thực hành:** <br>&emsp; + Phát triển các API Endpoints: Auth API, Problemset List, Code Run API, Post/Comment APIs <br>&emsp; + Kiểm thử API qua Postman | 17/07/2026 | 17/07/2026 | <https://fastapi.tiangolo.com/> |


### Kết quả đạt được tuần 5:

* Đóng gói thành công ứng dụng FastAPI backend lên AWS ECR và triển khai chạy trên AWS Lambda.
* Khởi tạo và cấu hình API Gateway HTTP API định tuyến thông suốt từ Frontend tới Backend.
* Hoàn thiện hệ thống RESTful APIs phục vụ đầy đủ các chức năng quản lý bài tập, bài viết mạng xã hội và thực thi chạy thử code.
