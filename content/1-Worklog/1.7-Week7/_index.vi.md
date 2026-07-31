---
title: "Worklog Tuần 7"
date: 2026-07-27
weight: 7
chapter: false
pre: " <b> 1.7. </b> "
reportTableColumns:
  - Thứ
  - Công việc
  - Ngày hoàn thành
reportType: worklog
---

### Mục tiêu tuần 7:

* Tự động hóa toàn bộ hạ tầng dự án CodExecute bằng Infrastructure as Code (AWS SAM/Terraform), kiểm thử chịu tải và tối ưu chi phí.
* Rà soát bảo mật toàn hệ thống, nghiệm thu dự án Capstone và hoàn thiện báo cáo tổng kết kỳ thực tập.

### Các công việc cần triển khai trong tuần này:
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Viết kịch bản AWS SAM Template (`template.yaml`) định nghĩa hạ tầng Serverless (Lambda, API Gateway, SQS, DynamoDB, S3, IAM Roles) | 27/07/2026 | 27/07/2026 | <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html> |
| 3 | - **Thực hành:** <br>&emsp; + Tự động hóa quá trình Deploy toàn bộ stack dự án CodExecute bằng AWS SAM CLI <br>&emsp; + Kiểm tra tính toàn vẹn tài nguyên hạ tầng sau khi triển khai tự động | 28/07/2026 | 28/07/2026 | <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html> |
| 4 | - **Thực hành:** <br>&emsp; + Thực hiện Load Testing bài bản bằng Locust/k6 (đạt khả năng chịu tải 1,000 concurrent users) <br>&emsp; + Cấu hình CloudWatch Alarms & SNS Notifications cảnh báo khi có lỗi phát sinh | 29/07/2026 | 29/07/2026 | <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html> |
| 5 | - Tổng hợp kết quả đo kiểm hiệu năng, bảng tính toán chi phí vận hành hàng tháng (~$23.23/tháng) và hoàn thiện báo cáo thực tập 7 tuần | 30/07/2026 | 30/07/2026 |  |
| 6 | - Báo cáo tổng kết dự án Capstone CodExecute với các Mentor FCAJ, bảo vệ giải pháp kiến trúc và hoàn thành kỳ thực tập | 31/07/2026 | 31/07/2026 |  |


### Kết quả đạt được tuần 7:

* Triển khai tự động hóa 100% toàn bộ hạ tầng dự án CodExecute bằng script IaC (AWS SAM).
* Hệ thống trải qua đợt Load Testing thành công với khả năng phục vụ đồng thời 1,000 concurrent users không nghẽn mạng.
* Hoàn thành xuất sắc chương trình thực tập 7 tuần FCAJ, hoàn thiện tài liệu báo cáo và bảo vệ thành công dự án Capstone.
