---
title: "Worklog Tuần 3"
date: 2026-06-29
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
reportTableColumns:
  - Thứ
  - Công việc
  - Ngày hoàn thành
reportType: worklog
---

### Mục tiêu tuần 3:

* Hiểu hạ tầng mạng Amazon VPC (Virtual Private Cloud) và dịch vụ Amazon CloudFront CDN.
* Nắm vững kỹ thuật phân chia Subnet Multi-AZ, đính kèm WAF bảo vệ bề mặt ứng dụng và phân phối Frontend qua CloudFront CDN.

### Các công việc cần triển khai trong tuần này:
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Tìm hiểu cơ bản về VPC: IPv4 CIDR Block (`10.0.0.0/16`), quy hoạch Subnets (2 Public Subnets & 2 Private Subnets đa vùng AZ) | 29/06/2026 | 29/06/2026 | <https://docs.aws.amazon.com/vpc/latest/userguide/configure-your-vpc.html> |
| 3 | - Tìm hiểu Amazon CloudFront CDN: Edge Locations, Cache Behaviors, Custom Domain & HTTPS SSL/TLS Certificate | 30/06/2026 | 30/06/2026 | <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Welcome.html> |
| 4 | - **Thực hành:** <br>&emsp; + Khởi tạo Custom VPC, đính kèm Internet Gateway và cấu hình Route Tables <br>&emsp; + Thiết lập Security Groups cho môi trường nội bộ | 01/07/2026 | 01/07/2026 | <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-subnets-routing.html> |
| 5 | - **Thực hành:** <br>&emsp; + Tạo CloudFront Distribution trỏ tới S3 Static Web Bucket để phân phối React Frontend của CodExecute | 02/07/2026 | 02/07/2026 | <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DistributionConfig.html> |
| 6 | - **Thực hành:** <br>&emsp; + Tạo CloudFront Cache Behavior định tuyến `/api/*` tới API Gateway <br>&emsp; + Bật AWS WAF Web ACL với Rate Limiting rule chống DDoS/Spam API | 03/07/2026 | 03/07/2026 | <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html> |


### Kết quả đạt được tuần 3:

* Thiết kế và xây dựng thành công hạ tầng Custom VPC cô lập môi trường mạng Public và Private.
* Phân phối ứng dụng React Frontend thành công qua CloudFront CDN với tốc độ tải trang cao ở Edge Locations.
* Định tuyến API thành công qua CloudFront và kích hoạt tường lửa AWS WAF bảo vệ ứng dụng trước các đợt tấn công Layer 7.
