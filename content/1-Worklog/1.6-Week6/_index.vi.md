---
title: "Worklog Tuần 6"
date: 2026-07-20
weight: 6
chapter: false
pre: " <b> 1.6. </b> "
reportTableColumns:
  - Thứ
  - Công việc
  - Ngày hoàn thành
reportType: worklog
---

### Mục tiêu tuần 6:

* Tìm hiểu cơ chế hàng đợi bất đồng bộ Amazon SQS và kỹ thuật thiết lập môi trường Sandbox cách ly chấm bài trên AWS Lambda.
* Triển khai hệ thống chấm bài bất đồng bộ an toàn chống Remote Code Execution (RCE) và xử lý lỗi bằng Dead-Letter Queue (DLQ).

### Các công việc cần triển khai trong tuần này:
| Thứ | Công việc | Ngày bắt đầu | Ngày hoàn thành | Nguồn tài liệu |
| --- | --- | --- | --- | --- |
| 2 | - Tìm hiểu Amazon SQS: Standard Queue, Message Retention, Long Polling (`WaitTime=20s`), Visibility Timeout và Dead-Letter Queue (DLQ) | 20/07/2026 | 20/07/2026 | <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html> |
| 3 | - Tìm hiểu kỹ thuật giới hạn tài nguyên và cách ly Sandbox (Memory limit, CPU, Timeout, Process PIDs) chống RCE trong Lambda Worker | 21/07/2026 | 21/07/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html> |
| 4 | - **Thực hành:** <br>&emsp; + Khởi tạo SQS Queue `codexecute-submission-queue` kèm DLQ `codexecute-submission-dlq` <br>&emsp; + Cấu hình Lambda API Handler gửi tin nhắn bài nộp vào SQS | 22/07/2026 | 22/07/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html> |
| 5 | - **Thực hành:** <br>&emsp; + Xây dựng hàm Lambda Code Executor Sandbox (Python/Docker trên ECR) triggered tự động bởi SQS <br>&emsp; + Hàm tải testcases từ S3, biên dịch/thực thi mã nguồn (C++, Java, Python, JS) và cập nhật kết quả vào DynamoDB | 23/07/2026 | 23/07/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/services-sqs.html> |
| 6 | - **Thực hành:** <br>&emsp; + Thử nghiệm kịch bản bài nộp bị lỗi vô hạn (TLE/MLE) hoặc mã độc lệnh hệ thống <br>&emsp; + Xác minh tính an toàn cách ly tuyệt đối của Sandbox | 24/07/2026 | 24/07/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/security-isolation.html> |


### Kết quả đạt được tuần 6:

* Xây dựng thành công hàng đợi tin nhắn SQS đệm bài nộp chống quá tải hệ thống.
* Triển khai môi trường Lambda Code Executor Sandbox cách ly tuyệt đối, chấm tự động đa ngôn ngữ (C++, Java, Python, JavaScript).
* Xử lý triệt để các trường hợp mã độc hoặc lỗi vòng lặp vô hạn (TLE/MLE) không ảnh hưởng tới hạ tầng chung.
