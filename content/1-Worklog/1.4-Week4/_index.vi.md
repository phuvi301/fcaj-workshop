---
title: "Worklog Tuần 4"
date: 2026-07-06
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
reportTableColumns:
  - Thứ
  - Công việc
  - Ngày hoàn thành
reportType: worklog
---

### Mục tiêu tuần 4:

* Tìm hiểu Cơ sở dữ liệu NoSQL (Amazon DynamoDB) và kỹ thuật quản lý bộ dữ liệu Testcases trên Amazon S3.
* Thiết kế mô hình dữ liệu Single-Table Design cho DynamoDB, tạo GSI và thiết lập S3 Lifecycle Rules tối ưu chi phí.

### Các công việc cần triển khai trong tuần này:
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Tìm hiểu Amazon DynamoDB: Partition Key, Sort Key, Global Secondary Index (GSI) và chế độ On-Demand Capacity | 06/07/2026 | 06/07/2026 | <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html> |
| 3 | - Tìm hiểu Amazon S3 Lifecycle Rules, S3 Glacier Flexible Retrieval và nén tập tin Testcase bằng Gzip | 07/07/2026 | 07/07/2026 | <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html> |
| 4 | - **Thực hành:** <br>&emsp; + Thiết kế sơ đồ dữ liệu cho các bảng `Users`, `Problems`, `Submissions`, `Posts` và `UserFollows` <br>&emsp; + Tạo bảng DynamoDB và GSI `SubmissionUserIndex` | 08/07/2026 | 08/07/2026 | <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html> |
| 5 | - **Thực hành:** <br>&emsp; + Viết script Python (boto3) thực thi các tác vụ CRUD dữ liệu bài tập & người dùng <br>&emsp; + Thử nghiệm truy vấn dữ liệu với độ trễ thấp (Single-digit ms) | 09/07/2026 | 09/07/2026 | <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html> |
| 6 | - **Thực hành:** <br>&emsp; + Tải bộ dữ liệu Testcases mẫu (Input/Output) lên S3 Bucket <br>&emsp; + Cấu hình S3 Lifecycle Rule chuyển dữ liệu testcase cũ hơn 90 ngày sang Glacier | 10/07/2026 | 10/07/2026 | <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html> |


### Kết quả đạt được tuần 4:

* Thiết kế và triển khai thành công mô hình dữ liệu DynamoDB On-Demand phục vụ các tác vụ chấm bài và mạng xã hội.
* Lập trình thành công các thao tác CRUD dữ liệu với DynamoDB Python SDK (boto3).
* Tải lên và quản lý hiệu quả bộ Testcase bài tập trên Amazon S3 kèm chính sách lưu trữ tối ưu chi phí.
