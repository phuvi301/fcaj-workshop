---
title: "Bản đề xuất dự án"
date: 2026-06-01
weight: 2
chapter: false
pre: " <b> 2. </b> "
---
<!-- {{% notice warning %}}
⚠️ **Lưu ý:** Các thông tin dưới đây chỉ nhằm mục đích tham khảo, vui lòng **không sao chép nguyên văn** cho bài báo cáo của bạn kể cả warning này.
{{% /notice %}} -->

# CODEXECUTE - HỆ THỐNG CHẤM BÀI TRỰC TUYẾN & NỀN TẢNG THUẬT TOÁN TỰ ĐỘNG


## 1. TỔNG QUAN DỰ ÁN

**CodExecute** là một nền tảng chấm bài tự động trực tuyến (Online Judge Platform) và mạng xã hội lập trình viên hiện đại, được thiết kế để giải quyết bài toán kiểm thử code, luyện tập thuật toán và đánh giá năng lực lập trình theo thời gian thực.

Dự án được xây dựng 100% theo mô hình **Pure Serverless Cloud-Native AWS**, sử dụng **AWS Lambda** làm môi trường thực thi backend lẫn sandbox chấm bài cách ly hoàn toàn, nhằm đảm bảo tính sẵn sàng cao (High Availability), khả năng tự động mở rộng từ 0 (Scale-to-Zero), và môi trường thực thi mã nguồn bảo mật (Secure Sandbox Execution).

<div align="center" style="margin: 24px 0;">

<img src="/images/5-Workshop/5.1-Workshop-overview/project_overview.png" alt="Giao diện nền tảng CodExecute Online Judge" style="width: 95%; max-width: 1100px; border-radius: 8px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);">

<p style="font-size: 1.05rem; font-weight: 600; margin-top: 10px; color: #475569;">
<i>Giao diện tổng quan nền tảng chấm bài tự động &amp; mạng xã hội CodExecute</i>
</p>

</div>


---

## 2. MỤC TIÊU DỰ ÁN

* **Khả năng mở rộng vô hạn (Elastic Scalability):** Hệ thống Serverless tự động thu phóng theo nhu cầu, có khả năng xử lý từ hàng trăm đến hàng chục nghìn lượt nộp bài (submissions) đồng thời trong các kỳ thi mà không gây nghẽn hoặc sập hệ thống.
* **Môi trường chấm bài an toàn tuyệt đối (Isolation & Security):** Thực thi mã nguồn nguy hiểm do người dùng gửi lên trong môi trường sandbox Lambda cách ly được giới hạn tài nguyên (CPU, RAM, Time, Network), chống lại các nguy cơ Remote Code Execution (RCE) hoặc chiếm quyền hạ tầng.
* **Phản hồi thời gian thực với độ trễ tối thiểu (Low-Latency Response):** Tối ưu luồng nhận bài và trả kết quả chấm bài (Accept/Wrong Answer/Time Limit Exceeded/Memory Limit Exceeded) trong dưới 2 giây đối với bài tập thông thường.
* **Tối ưu hóa chi phí vận hành (Cost Optimization):** Áp dụng triệt để mô hình *Pay-As-You-Go*, chỉ chi trả cho lượng tài nguyên compute/storage thực tế tiêu thụ, hoàn toàn không có chi phí duy trì máy chủ nhàn rỗi 24/7.
* **Trải nghiệm người dùng cao cấp (Seamless UX/UI):** Cung cấp giao diện trực quan với Trình soạn thảo Code chuyên nghiệp, hỗ trợ đa ngôn ngữ (Python, C++, Java, JavaScript), hệ thống bài tập phân loại theo chủ đề, cùng tính năng tương tác mạng xã hội (Post, Follow, Achievement Badges).

---

## 3. VẤN ĐỀ DỰ ÁN GIẢI QUYẾT

| Vấn đề của hệ thống truyền thống | Giải pháp của CodExecute trên AWS |
| :--- | :--- |
| **Rủi ro rò rỉ bảo mật (RCE):** Mã nguồn chưa kiểm duyệt của người dùng có thể thực thi lệnh xóa file hệ thống, đào coin, hoặc tấn công nội bộ server. | **Chống RCE với Lambda Sandbox:** Mỗi submission được chạy trong một Lambda Worker cách ly hoàn toàn, không có quyền truy cập mạng ngoài và bị giới hạn tài nguyên nghiêm ngặt (Memory, Execution Timeout, Process Limits). |
| **Nghẽn cổ chai khi cao điểm (Traffic Spikes):** Các đợt nộp bài dồn dập khiến server bị quá tải (Overload/Crash). | **Hàng chờ bất đồng bộ với Amazon SQS:** Đẩy các bài nộp vào queue để điều tiết lưu lượng (Buffer), giúp Lambda Worker tự động scale xử lý ổn định theo cơ chế nạp xả tự động. |
| **Chi phí máy chủ nhàn rỗi cao:** Phải duy trì cụm máy chủ EC2/Container cấu hình cao 24/7 dù giờ thấp điểm không có người dùng. | **Serverless Pay-As-You-Go (Lambda + API Gateway + DynamoDB):** Hạ tầng tự động thu phóng về 0 (Scale to Zero) khi không có request, giảm đến 75% chi phí hạ tầng. |
| **Quản lý bộ dữ liệu Testcase khổng lồ:** Testcase lớn (vài chục MB đến vài GB) làm quá tải cơ sở dữ liệu quan hệ (RDBMS). | **Lưu trữ phân tầng S3 & DynamoDB:** Metadata bài tập lưu ở DynamoDB (NoSQL tốc độ cao), bộ Testcase input/output lớn lưu trên Amazon S3 với tốc độ đọc cực nhanh. |

---

## 4. CÁC TÍNH NĂNG CHÍNH

1. **Hệ Thống Quản Lý & Phân Loại Bài Tập (Problemset & Tagging System):**
   - Tìm kiếm bài tập theo tiêu đề, độ khó (Easy, Medium, Hard), chủ đề thuật toán (Binary Tree, DP, Graph, Dynamic Array...).
   - Thống kê tỷ lệ giải thành công (Acceptance Rate) và số lượng lượt nộp bài.

2. **Trình Soạn Thảo & Chạy Bài Nộp (Interactive Code Editor & Runner):**
   - Hỗ trợ biên dịch và thực thi 4 ngôn ngữ phổ biến: **C++, Java, Python, JavaScript**.
   - Chế độ **Run Code** (Chạy thử với custom input) và **Submit Code** (Chấm điểm toàn bộ Testcase).
   - Tự động bắt lỗi biên dịch (Compile Error), Runtime Error, Time Limit Exceeded (TLE), Memory Limit Exceeded (MLE).

3. **Môi Trường Sandbox Chấm Bài Tự Động (Automated Isolated Sandbox):**
   - Tách biệt hoàn toàn môi trường nhận API và môi trường thực thi code.
   - So sánh output với chuẩn chính xác từng ký tự/dòng.

4. **Mạng Xã Hội Lập Trình Viên (Developer Social Network):**
   - Tạo bài viết chia sẻ kiến thức (Posts), thảo luận lời giải (Comments), theo dõi bạn bè (Follow system).
   - Hệ thống danh hiệu & huy hiệu thành tựu (Achievement Badges).

5. **Trang Cá Nhân & Thống Kê Tiến Độ (User Dashboard & Analytics):**
   - Biểu đồ nhiệt lượt giải bài (Submission Heatmap).
   - Lịch sử nộp bài chi tiết kèm mã nguồn và thời gian chạy/bộ nhớ tiêu dùng.

---

## 5. KIẾN TRÚC HOẠT ĐỘNG CỦA DỰ ÁN

### 5 trụ cột của AWS Well-Architected Framework
Kiến trúc của **CodExecute** tuân thủ 5 trụ cột của **AWS Well-Architected Framework**:

1. **Operational Excellence (Vận hành xuất sắc):** Quản lý cấu hình bằng Infrastructure as Code (IaC SAM/CloudFormation), giám sát tập trung với Amazon CloudWatch Logs & Metrics.
2. **Security (Bảo mật):** Phân quyền tối thiểu (Least Privilege) với IAM Roles, mã hóa dữ liệu At-Rest (KMS) & In-Transit (TLS 1.3/HTTPS via CloudFront), sandbox cách ly hoàn toàn.
3. **Reliability (Độ tin cậy):** Đảm bảo tính khả dụng cao qua đa Availability Zone (Multi-AZ), cơ chế retry và Dead-Letter Queue (DLQ) trên SQS.
4. **Performance Efficiency (Hiệu năng):** Phân phối tĩnh với CloudFront CDN Edge locations, đọc dữ liệu cực nhanh với DynamoDB Single-digit millisecond latency.
5. **Cost Optimization (Tối ưu chi phí):** Áp dụng triệt để kiến trúc Pure Serverless Event-Driven (Lambda Pay-As-You-Go).

### Sơ đồ kiến trúc của dự án
![Sơ đồ kiến trúc CodExecute](/images/2-Proposal/architect-codexecute.drawio.png)

### Phân Tích Phân Lớp Kiến Trúc (Architecture Layers)
Dựa trên sơ đồ kiến trúc tổng quan chuẩn AWS, hệ thống CodExecute được thiết kế phân thành 6 lớp chức năng hoạt động tại AWS Region `ap-southeast-1`:

1. **Lớp CDN & Bảo mật bề mặt (CDN Layer):**
   - **Amazon CloudFront:** Phân phối nội dung tĩnh từ S3 tới người dùng toàn cầu với độ trễ thấp và đóng vai trò Reverse Proxy định tuyến `/api/*` tới API Gateway.
   - **AWS WAF:** Tường lửa ứng dụng web giúp ngăn chặn các đợt tấn công layer 7, SQL Injection, Cross-Site Scripting (XSS) và giới hạn tần suất request (Rate Limiting).
   - **Xác thực OAuth Providers:** Hỗ trợ đăng nhập ứng dụng thông qua Google và GitHub.

2. **Lớp Cổng tiếp nhận & Host tĩnh (Ingress & Static Hosting Layer):**
   - **AWS S3 Bucket (Static Hosting):** Lưu trữ gói sản phẩm tĩnh (React Frontend HTML/JS/CSS).
   - **AWS API Gateway (REST API):** Cổng giao tiếp RESTful API tiếp nhận các yêu cầu HTTP từ CloudFront và chuyển tiếp đồng bộ (**Synchronous Invoke**) tới Lambda API Handler.

3. **Lớp Tính toán Serverless & Môi trường Sandbox (Serverless Compute & Sandbox Layer):**
   - **AWS ECR (Container Registry):** Quản lý và lưu trữ Container Images để triển khai lên các hàm Lambda.
   - **AWS Lambda (API Handler):** Chạy backend FastAPI, tương tác dữ liệu với DynamoDB, đọc S3 assets và đẩy job bài nộp vào hàng chờ SQS.
   - **AWS Lambda (Code Executor Sandbox):** Nhận kích hoạt từ SQS, tải bộ testcase từ S3, thực thi code người dùng trong môi trường Sandbox cách ly tuyệt đối và lưu kết quả vào DynamoDB.

4. **Lớp Xử lý hàng chờ (Queue Processing Layer):**
   - **AWS SQS (Submission Queue):** Hàng chờ đệm bất đồng bộ tiếp nhận job bài nộp, đóng vai trò điều tiết thông lượng (Buffer) và kích hoạt Lambda Sandbox.

5. **Lớp Cơ sở dữ liệu & Lưu trữ (Database & Storage Layer):**
   - **AWS DynamoDB (Submission & Problem):** Cơ sở dữ liệu NoSQL tốc độ cao lưu trữ bảng bài tập, bài nộp, thông tin người dùng và mạng xã hội.
   - **AWS S3 Bucket (Testcases):** Lưu trữ bộ dữ liệu Testcases (Input/Output text files) bài tập.
   - **AWS S3 Bucket (User Avatar):** Lưu trữ hình ảnh đại diện của người dùng.

6. **Lớp Bảo mật & Giám sát (Security & Monitoring Layer):**
   - **IAM Roles (Execution Role):** Phân quyền truy cập tối thiểu (Least Privilege) giữa các dịch vụ.
   - **AWS CloudWatch (Logs & Metrics):** Giám sát log thực thi và chỉ số hiệu năng hệ thống.
   - **AWS SNS:** Gửi thông báo cảnh báo sự cố tự động cho đội ngũ vận hành.

---

### Luồng Xử Lý Bài Nộp Đầy Đủ (End-to-End Execution Workflow)
Luồng vận hành từ lúc người dùng tương tác đến khi nhận kết quả chấm bài diễn ra qua **9 bước**:

1. **Step 1:** Người dùng gửi **HTTP Request** từ trình duyệt (User Browser) sau khi đăng nhập qua **OAuth Providers** (Google/GitHub).
2. **Step 2:** **Amazon CloudFront** đọc dữ liệu tĩnh (**Fetch Static Files**) từ **AWS S3 Bucket (Static Hosting)** để phân phối trang web cho người dùng.
3. **Step 3:** Với các yêu cầu API (`/api/*`), CloudFront chuyển tiếp đường dẫn (**Forward API Routing**) tới **AWS API Gateway (REST API)**.
4. **Step 4:** API Gateway gọi đồng bộ (**Synchronous Invoke**) đến hàm **AWS Lambda (API Handler)**.
5. **Step 5a, 5b, 5c:** Lambda API Handler thực hiện các thao tác:
   - **Step 5a:** Đọc/Ghi dữ liệu người dùng & bài tập (**CRUD User/Problem Data**) trên **Amazon DynamoDB**.
   - **Step 5b:** Đọc các mẫu testcase (**Fetch Sample Testcases**) từ **AWS S3 Bucket (Testcases)**.
   - **Step 5c:** Đọc ảnh đại diện (**Fetch User Avatar**) từ **AWS S3 Bucket (User Avatar)**.
6. **Step 6:** Lambda API Handler đóng gói payload bài nộp và đẩy vào hàng chờ (**Push Execution Job**) trên **AWS SQS (Submission Queue)**, trả về trạng thái `Pending` ngay lập tức cho người dùng.
7. **Step 7:** **AWS SQS** tự động phát sự kiện kích hoạt (**Event Trigger**) hàm **AWS Lambda (Code Executor Sandbox)**.
8. **Step 8:** Lambda Code Executor Sandbox tải toàn bộ tệp testcase (**Fetch Full Testcases**) từ **AWS S3 Bucket (Testcases)**.
9. **Step 9:** Lambda Code Executor Sandbox thực thi code trong môi trường Sandbox cách ly và ghi nhận kết quả chấm bài (**Save Result**) vào **Amazon DynamoDB**.

---

### Bảng Liệt Kê Các Dịch Vụ AWS Cốt LõiTrong Dự Án

Dưới đây là bảng tổng hợp các dịch vụ AWS được ứng dụng trong sơ đồ kiến trúc CodExecute:

| STT | Dịch vụ AWS | Vai trò & Nhiệm vụ trong CodExecute | Lý do lựa chọn & Lợi ích kỹ thuật |
| :---: | :--- | :--- | :--- |
| **1** | **Amazon CloudFront** | Phân phối ứng dụng React Frontend từ S3 Bucket đến người dùng toàn cầu. Đóng vai trò Reverse Proxy điều hướng `/api/*` tới API Gateway. | Tăng tốc tải trang toàn cầu bằng caching ở các Edge Locations. Hỗ trợ HTTPS/TLS 1.3 tự động, tích hợp bảo vệ chống DDoS. |
| **2** | **AWS WAF** | Tường lửa ứng dụng bảo vệ CloudFront và API Gateway. | Ngăn chặn các đợt tấn công Web (SQLi, XSS, Bot Attack) và áp dụng Rate Limiting chống spam request. |
| **3** | **Amazon S3** | **Bucket 1:** Lưu trữ static assets (HTML/JS/CSS) Frontend.<br>**Bucket 2:** Lưu trữ bộ Testcase bài tập.<br>**Bucket 3:** Lưu trữ file avatar người dùng. | Chi phí lưu trữ rẻ ($0.023/GB), độ tin cậy 99.999999999% (11 số 9 durability). Dung lượng mở rộng vô hạn, hỗ trợ S3 Presigned URL. |
| **4** | **Amazon API Gateway** | Cổng giao tiếp RESTful API tiếp nhận request từ CloudFront và gọi đồng bộ tới Lambda API Handler. | Hỗ trợ Rate Limiting / Throttling phòng chống Spam API, xác thực JWT Token, tích hợp trực tiếp với CORS và CloudFront Domain. |
| **5** | **AWS ECR** | Lưu trữ Container Images cho Lambda API Handler và Lambda Code Executor Sandbox. | Quản lý container image bảo mật, tích hợp native với AWS Lambda để kéo image nhanh chóng khi scale. |
| **6** | **AWS Lambda** | **Lambda API Handler:** Xử lý logic ứng dụng RESTful API.<br>**Lambda Code Executor Sandbox:** Thực thi và chấm điểm mã nguồn (C++, Java, Python, JS) trong Sandbox cách ly. | Mô hình Serverless Pay-As-You-Go (chỉ trả tiền khi code chạy). Tự động scale tức thì mà không cần quản lý cụm máy chủ. |
| **7** | **Amazon SQS** | Làm hàng chờ bất đồng bộ lưu trữ các bài nộp (`Submission Queue`) điều tiết lưu lượng cho Worker chấm bài. | Đóng vai trò Buffer chống nghẽn hệ thống khi có đợt nộp bài cao điểm. Đảm bảo không mất bài nộp nhờ mechanism Message Retention & DLQ. |
| **8** | **Amazon DynamoDB** | Lưu trữ toàn bộ dữ liệu cấu trúc hệ thống: Bảng `Users`, `Problems`, `Submissions`, `TestCases`, `Posts`, `Notifications`, `UserFollows`. | Tốc độ truy vấn ổn định ở mức single-digit millisecond. Chế độ On-Demand tự động scale xử lý hàng triệu request không cần sharding. |
| **9** | **AWS IAM** | Quản lý định danh và phân quyền tối thiểu (Least Privilege Access Execution Role) giữa các dịch vụ AWS. | Đảm bảo nguyên tắc bảo mật Zero-Trust. Ngăn chặn quyền truy cập trái phép giữa các thành phần hệ thống thông qua IAM Roles & Policies. |
| **10** | **Amazon CloudWatch** | Thu thập toàn bộ Logs thực thi từ Lambda, API Gateway. Theo dõi chỉ số hiệu năng (Metrics) và thiết lập Cảnh báo (Alarms). | Giám sát sức khỏe hệ thống thời gian thực. Cảnh báo tự động khi tỷ lệ lỗi vượt ngưỡng, hỗ trợ truy vết lỗi (Debugging) nhanh chóng. |
| **11** | **Amazon SNS** | Dịch vụ gửi thông báo cảnh báo sự cố từ CloudWatch Alarms tới email quản trị viên. | Đảm bảo phản ứng nhanh trước các sự cố vận hành thông qua các kênh notification tức thời. |

---

## 8. KẾ HOẠCH TRIỂN KHAI & TIMELINE 

Dự án được triển khai trong vòng **7 tuần** (từ ngày **15/06/2026** đến ngày **31/07/2026**) chia thành **5 Giai Đoạn (Phases)** với các cột mốc quan trọng (Milestones):

* **Phase 1: Khởi Tạo Hạ Tầng & IaC** *(15/06/2026 – 24/06/2026)*
  > Khởi tạo kiến trúc hạ tầng S3, DynamoDB, SQS, IAM Roles chuẩn AWS Well-Architected bằng AWS SAM & Terraform.

* **Phase 2: Xây Dựng Frontend & Backend Core** *(25/06/2026 – 05/07/2026)*
  > Phát triển giao diện React + Vite (Trình soạn thảo Code, Bộ bài tập) và hệ thống RESTful APIs với FastAPI trên AWS Lambda.

* **Phase 3: Xử Lý Bất Đồng Bộ & Lambda Sandbox** *(06/07/2026 – 16/07/2026)*
  > Xây dựng hàng chờ Amazon SQS và triển khai Lambda Worker thực thi mã nguồn tự động trong môi trường Sandbox cách ly.

* **Phase 4: Kiểm Thử & Bảo Mật Hardening** *(17/07/2026 – 25/07/2026)*
  > Kiểm thử chịu tải (Load Testing với Locust/k6 lên đến 1,000 VUs), đánh giá an ninh bảo mật chống RCE và thử nghiệm cơ chế DLQ failover.

* **Phase 5: Tối Ưu Chi Phí & Chính Thức Go-Live** *(26/07/2026 – 31/07/2026)*
  > Tối ưu cấu hình RAM/Timeout Lambda, thiết lập cảnh báo CloudWatch Budgets và chính thức **GO-LIVE ngày 31/07/2026**.

### Chi Tiết Từng Giai Đoạn

| Giai Đoạn | Thời Gian | Công Việc Chi Tiết | Sản Phẩm Đầu Ra (Deliverables) |
| :--- | :--- | :--- | :--- |
| **Phase 1: Khởi Tạo Hạ Tầng & IaC** | **15/06/2026 – 24/06/2026** *(10 ngày)* | - Thiết kế kiến trúc chi tiết chuẩn AWS Well-Architected.<br>- Viết kịch bản AWS SAM / Terraform khởi tạo S3 Buckets, DynamoDB Tables, SQS Queues, IAM Roles.<br>- Thiết lập Repository, CI/CD Pipeline với GitHub Actions. | - Cụm hạ tầng AWS Dev environment sẵn sàng.<br>- Codebase SAM Template hoàn chỉnh. |
| **Phase 2: Xây Dựng Frontend & Backend Core** | **25/06/2026 – 05/07/2026** *(11 ngày)* | - Phát triển ứng dụng React + Vite Frontend (Code Editor, Task filtering, User profile).<br>- Phát triển FastAPI Backend với các endpoint Authentication (JWT), Problems API, Submissions API.<br>- Đóng gói Lambda API Handler. Tích hợp API Gateway & CloudFront. | - Web UI chạy mượt trên CloudFront + S3.<br>- RESTful API hoạt động đầy đủ trên Lambda & DynamoDB. |
| **Phase 3: Xử Lý Bất Đồng Bộ & Lambda Sandbox** | **06/07/2026 – 16/07/2026** *(11 ngày)* | - Xây dựng mô hình đẩy job nộp bài vào Amazon SQS Queue.<br>- Viết Lambda Worker Runner cách ly thực thi 4 ngôn ngữ (C++, Java, Python, JS).<br>- Triển khai AWS Lambda Worker nhận job từ SQS, đọc Testcase từ S3 và chấm điểm. | - Luồng chấm bài tự động bất đồng bộ hoàn tất.<br>- Chống RCE thành công trong Lambda Sandbox. |
| **Phase 4: Kiểm Thử & Bảo Mật Hardening** | **17/07/2026 – 25/07/2026** *(9 ngày)* | - Kiểm thử chịu tải (Load Testing với Locust/k6 lên đến 1,000 VUs).<br>- Kiểm thử bảo mật (Penetration Testing) chống RCE, SQLi, XSS, Resource Exhaustion.<br>- Thử nghiệm trường hợp đứt gãy hạ tầng (Failover & DLQ testing). | - Báo cáo Load Test đạt chỉ số cam kết.<br>- Khắc phục 100% lỗ hổng bảo mật mức High/Critical. |
| **Phase 5: Tối Ưu Chi Phí & Chính Thức Go-Live** | **26/07/2026 – 31/07/2026** *(6 ngày)* | - Thiết lập CloudWatch Alarms & Cost Budgets Alert.<br>- Tối ưu hóa dung lượng RAM/Timeout của AWS Lambda.<br>- Chuyển đổi môi trường Production & Bàn giao toàn bộ tài liệu dự án. | - **Dự án CHÍNH THỨC GO-LIVE ngày 31/07/2026.**<br>- Bộ tài liệu kiến trúc & vận hành chi tiết. |

---

## 9. ƯỚC TÍNH NGÂN SÁCH & ĐÁNH GIÁ COST OPTIMIZATION

### 1. Ước Tính Ngân Sách Hàng Tháng 

Dự toán ngân sách được tính dựa trên quy mô vận hành trung bình: **100,000 bài nộp/tháng** và **500,000 API requests/tháng**.

| Dịch Vụ AWS | Mức Độ Sử Dụng Dự Kiến / Tháng | Đơn Giá Tham Chiếu (ap-southeast-1) | Chi Phí Hàng Tháng (USD) |
| :--- | :--- | :--- | :---: |
| **AWS Lambda** | 500,000 API Requests + 100,000 Worker Sandbox executions (Memory: 512MB, Avg duration: 800ms) | $0.20 / 1M Requests + Compute time | **$3.80** |
| **Amazon API Gateway** | 500,000 HTTP API calls | $1.00 / 1M Requests | **$0.50** |
| **Amazon SQS** | 200,000 SQS Requests (SendMessage + ReceiveMessage) | $0.40 / 1M Requests | **$0.08** |
| **Amazon DynamoDB** | 1,000,000 Read/Write Units (On-Demand Mode) + 5GB Data Storage | $0.25 / 1M WCU, $0.05 / 1M RCU | **$3.20** |
| **Amazon S3** | 15GB Storage (Testcases + User Media + Web Assets) + 100k GET/PUT | $0.023 / GB | **$0.65** |
| **Amazon CloudFront** | 50GB Data Transfer Out + 500k HTTPS Requests | $0.09 / GB | **$4.50** |
| **AWS WAF** | 1 Web ACL + 2 Rules (Rate Limit & Core Rule Set) + 500k Requests | $5.00/Web ACL + $1.00/Rule + $0.60/1M Requests | **$7.30** |
| **AWS ECR** | 5GB Storage chứa Container Images cho Lambda Sandbox & API Handler | $0.10 / GB Storage / tháng | **$0.50** |
| **Amazon SNS** | ~100 Email notifications gửi từ CloudWatch Alarms khi có sự cố | 1,000 Email đầu tiên & 1M Publish requests miễn phí | **$0.00** |
| **Amazon CloudWatch** | 3GB Ingestion Logs + 5 Custom Metrics + 3 Alarms | $0.57 / GB Logs | **$2.70** |
| **AWS IAM** | Toàn bộ IAM Users, Roles, Policies | Miễn phí | **$0.00** |
| **TỔNG CỘNG CHI PHÍ DỰ KIẾN / THÁNG:** | | | **~$23.23 USD / tháng** |

> 💡 *Lưu ý:* Trong 12 tháng đầu tiên triển khai, phần lớn chi phí trên sẽ nằm trong gói **AWS Free Tier** (1M Lambda requests/tháng, 1M API Gateway requests/tháng, 25GB DynamoDB storage, 5GB S3 storage, 1,000 SNS Emails/tháng), giúp chi phí thực tế duy trì ở mức **< $8.50 USD/tháng** (chủ yếu từ AWS WAF Base ACL).

---

### 2. Chiến Lược Tối Ưu Chi Phí

1. **Mô hình Pure Serverless Pay-As-You-Go:**
   - Sử dụng **AWS Lambda** và **API Gateway HTTP API** (rẻ hơn 70% so với REST API) giúp hệ thống không tốn bất kỳ chi phí duy trì máy chủ nào khi không có người dùng truy cập.

2. **Tối ưu hóa DynamoDB On-Demand vs Provisioned:**
   - Trong giai đoạn đầu triển khai, sử dụng chế độ **On-Demand Capacity** để trả tiền chính xác theo số lượng read/write. Khi lưu lượng ổn định, chuyển các bảng chính sang **Provisioned Capacity + Auto Scaling** để giảm thêm 40% chi phí.

3. **S3 Lifecycle Rules & Compression:**
   - Cấu hình **S3 Lifecycle Rules** chuyển các log testcase cũ hơn 90 ngày sang lớp lưu trữ **S3 Glacier Flexible Retrieval** (giảm 85% chi phí lưu trữ).
   - Nén bộ Testcase bằng Gzip trước khi lưu trên S3 giúp giảm băng thông truyền tải.

4. **Sử Dụng SQS Long Polling:**
   - Cấu hình SQS `ReceiveMessageWaitTimeSeconds = 20` (Long Polling). Điều này giúp giảm số lượng yêu cầu kiểm tra tin nhắn rỗng (Empty Receive Requests), tiết kiệm chi phí gọi SQS API lên tới 90%.

5. **Tối Ưu Dung Lượng ECR & WAF Rules:**
   - Cấu hình **ECR Lifecycle Policy** tự động xóa các container image untagged cũ và chỉ duy trì tối đa 3 image mới nhất, giữ dung lượng ECR dưới 5GB.
   - Kết hợp **AWS WAF** với CloudFront Caching và Rate Limiting để chặn traffic độc hại ngay tại Edge Location, bảo vệ backend Lambda khỏi các đợt tấn công tốn kém.

6. **AWS Lambda Power Tuning:**
   - Sử dụng công cụ *AWS Lambda Power Tuning* để tìm mức RAM/vCPU tối ưu nhất cho Lambda API & Worker, giúp vừa tăng tốc độ phản hồi vừa giảm thời gian tính phí.

---

## 10. ĐÁNH GIÁ RỦI RO DỰ ÁN & BIỆN PHÁP GIẢM THIỂU

| STT | Loại Rủi Ro | Phân Tích Chi Tiết Rủi Ro | Mức Độ | Biện Pháp Giảm Thiểu (Mitigation Strategy) |
| :---: | :--- | :--- | :---: | :--- |
| **1** | **Bảo Mật (Security)** | **RCE (Remote Code Execution) trong Sandbox:** Người dùng viết mã độc nhằm đọc file hệ thống, thực hiện fork bomb làm kiệt quệ CPU/RAM, hoặc truy cập mạng nội bộ AWS. | **CRITICAL** | - Thực thi code trong **Lambda Isolated Sandbox** không có root privilege.<br>- Tắt toàn bộ kết nối mạng ngoài (`VPC Network: Disabled / Strict Subnet Security Groups`) trong Sandbox Runner.<br>- Áp dụng giới hạn cứng tài nguyên: RAM (max 512MB), CPU (max 1 Core), Timeout (max 5s), Process limit (max 20 pids). |
| **2** | **Hiệu Năng (Performance)** | **Nghẽn hàng chờ SQS hoặc Cold Start Lambda:** Khi có đợt thi nộp bài tập trung (hàng nghìn bài nộp/phút), Cold Start của Lambda có thể làm tăng độ trễ chấm bài. | **HIGH** | - Thiết lập **Provisioned Concurrency** cho các hàm Lambda quan trọng trong thời gian diễn ra kỳ thi.<br>- Tăng số lượng Worker tự động scale theo chỉ số `ApproximateNumberOfMessagesVisible` của SQS. |
| **3** | **Bảo Mật (Security)** | **Tấn công DDoS / Spam API:** Kẻ xấu liên tục gửi request rác làm cạn kiệt ngân sách AWS (Financial Exhaustion). | **HIGH** | - Bật **AWS WAF** và cấu hình **API Gateway Throttling / Rate Limiting** (giới hạn max 20 requests/phút cho mỗi IP/User).<br>- Tích hợp CloudFront Geo Blocking và AWS Shield Standard. |
| **4** | **Vận Hành (Operations)** | **Mất mát bài nộp do lỗi hệ thống (Data Loss):** Worker chấm bài bị crash bất ngờ khi đang xử lý job từ SQS. | **MEDIUM** | - Cấu hình SQS `VisibilityTimeout` phù hợp.<br>- Bật **Dead-Letter Queue (DLQ)**: Tin nhắn lỗi quá 3 lần sẽ được đẩy vào DLQ để kỹ sư kiểm tra lại mà không bị mất dữ liệu. |
| **5** | **Quản Lý Chi Phí (Cost)** | **Chi phí gia tăng đột biến (Spike Cost):** Lỗi vòng lặp vô tận trong code Lambda hoặc ghi log quá nhiều vào CloudWatch. | **MEDIUM** | - Thiết lập **AWS Budgets Alert** cảnh báo tự động qua Email/Slack khi chi phí vượt $20 USD/tháng.<br>- Cấu hình CloudWatch Log Retention Period tối đa 14 ngày thay vì để vĩnh viễn. |

---

## 11. KẾT QUẢ KỲ VỌNG

Sau khi hoàn thành triển khai vào ngày **31/07/2026**, hệ thống **CodExecute** dự kiến đạt được các chỉ số kỹ thuật và mục tiêu kinh doanh sau:

### Chỉ Số Kỹ Thuật (Technical KPIs)
* **Độ sẵn sàng (Availability SLA):** Đạt tối thiểu **99.9%** thời gian hoạt động ổn định nhờ hạ tầng Multi-AZ Serverless.
* **Thời gian phản hồi API (API Response Latency):** < 200ms đối với các tác vụ đọc/ghi dữ liệu thông thường qua API Gateway & Lambda.
* **Thời gian chấm bài (Submission Processing Time):** < 2.0 giây kể từ lúc người dùng nhấn Submit đến khi nhận kết quả (đối với các bài tập có bộ Testcase dưới 50MB).
* **Khả năng chịu tải (Concurrent Capacity):** Xử lý mượt mà tối thiểu **1,000 bài nộp đồng thời (concurrent submissions)** mà không xảy ra hiện tượng drop request hay nghẽn hệ thống.
* **An toàn tuyệt đối (Zero RCE Vulnerability):** 100% mã nguồn người dùng được kiểm soát và cách ly hoàn toàn trong Lambda Sandbox, không phát sinh bất kỳ sự cố rò rỉ bảo mật nào.

### Giá Trị Vận Hành & Kinh Doanh (Business Outcomes)
* **Tối ưu chi phí:** Tiết kiệm hơn **75%** chi phí vận hành hạ tầng so với việc thuê máy chủ truyền thống (EC2/Dedicated Server).
* **Khả năng bảo trì cao:** Hạ tầng quản lý 100% bằng kịch bản Code (IaC SAM/CloudFormation), giúp việc tạo mới hoặc khôi phục môi trường thử nghiệm chỉ mất dưới 15 phút.
* **Trải nghiệm người dùng vượt trội:** Cung cấp cho cộng đồng lập trình viên Việt Nam một nền tảng thực thi thuật toán chuẩn hóa, tin cậy, góp phần nâng cao kỹ năng lập trình và chuẩn bị cho các kỳ thi tuyển dụng công nghệ.
