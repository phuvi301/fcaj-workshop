---
title: "Worklog Tuần 2"
date: 2026-06-22
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
reportTableColumns:
  - Thứ
  - Công việc
  - Ngày hoàn thành
reportType: worklog
---

### Mục tiêu tuần 2:

* Nắm vững các khái niệm cốt lõi của AWS IAM: User, Group, Role và Policy.
* Thực hành thiết kế chính sách bảo mật cho CodExecute: Quyền tối thiểu (Least Privilege), IAM Roles cho Lambda & S3 Bucket Policies.

### Các công việc cần triển khai trong tuần này:
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Tìm hiểu tổng quan IAM: IAM User, IAM Group, Managed Policy và Inline Policy cho hệ thống đa dịch vụ | 22/06/2026 | 22/06/2026 | <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html> |
| 3 | - Thiết kế kiến trúc phân quyền tối thiểu (Least Privilege) cho Lambda API Handler, Lambda Executor Sandbox, S3 và DynamoDB | 23/06/2026 | 23/06/2026 | <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html> |
| 4 | - **Thực hành:** <br>&emsp; + Tạo các S3 Buckets (`codexecute-static-web`, `codexecute-testcases`, `codexecute-user-avatars`) <br>&emsp; + Cấu hình S3 Block Public Access & CORS | 24/06/2026 | 24/06/2026 | <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html> |
| 5 | - **Thực hành:** <br>&emsp; + Tạo IAM Execution Roles cho Lambda API Handler và Lambda Sandbox Executor <br>&emsp; + Cấp quyền đọc Testcases từ S3 và ghi kết quả chấm bài vào DynamoDB không lưu Hardcoded Keys | 25/06/2026 | 25/06/2026 | <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html> |
| 6 | - Tìm hiểu AWS Security Token Service (STS) và kiểm thử phân quyền IAM Roles qua AWS CLI | 26/06/2026 | 26/06/2026 | <https://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html> |


### Kết quả đạt được tuần 2:

* Hiểu rõ cấu trúc JSON của một IAM Policy (Effect, Action, Resource, Condition).
* Khởi tạo thành công các S3 Buckets lưu trữ dữ liệu tĩnh, bộ Testcase và ảnh đại diện cho CodExecute.
* Tạo và đính kèm IAM Roles an toàn cho các dịch vụ Serverless theo nguyên tắc phân quyền tối thiểu (Least Privilege).
