---
title: "Project Proposal"
date: 2026-06-01
weight: 2
chapter: false
pre: " <b> 2. </b> "
---

# CODEXECUTE - ONLINE JUDGE & AUTOMATED ALGORITHM EVALUATION PLATFORM


## 1. PROJECT OVERVIEW

**CodExecute** is an automated Online Judge evaluation platform and modern developer social network designed to compile, execute, and evaluate user-submitted code in real time.

Built 100% on a **Pure Serverless Cloud-Native AWS** architecture, CodExecute leverages **AWS Lambda** for both REST API backend business logic and isolated sandbox code execution, ensuring High Availability, automatic Scale-to-Zero capability, and robust execution sandbox security.

<div align="center" style="margin: 24px 0;">

<img src="/images/5-Workshop/5.1-Workshop-overview/project_overview.png" alt="CodExecute Online Judge Platform Interface Overview" style="width: 95%; max-width: 1100px; border-radius: 8px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);">

<p style="font-size: 1.05rem; font-weight: 600; margin-top: 10px; color: #475569;">
<i>CodExecute Platform Overview: Automated Online Judge &amp; Developer Social Platform</i>
</p>

</div>


---

## 2. PROJECT OBJECTIVES

* **Elastic Scalability:** Auto-scales serverless compute from zero to thousands of concurrent submissions during programming contests without server crashes or bottlenecking.
* **Isolated Sandbox Security:** Safely executes untrusted user code (C++, Java, Python, JavaScript) within restricted Lambda Workers, preventing Remote Code Execution (RCE) and infrastructure privilege escalation.
* **Low-Latency Feedback:** Evaluates and returns grading results (Accepted, Wrong Answer, Time Limit Exceeded, Memory Limit Exceeded) in under 2 seconds for standard problemsets.
* **Cost Optimization:** Enforces strict Pay-As-You-Go pricing, eliminating 24/7 idle server maintenance overhead.
* **Seamless User Experience:** Delivers an intuitive Web UI featuring an interactive code editor, multi-language support, problemset filtering by tag/difficulty, and developer social features (Posts, Follows, Achievement Badges).

---

## 3. PROBLEM STATEMENT & AWS SOLUTIONS

| Traditional Infrastructure Bottlenecks | CodExecute Cloud-Native AWS Solution |
| :--- | :--- |
| **Security Risks (RCE Attacks):** Untrusted code executions can compromise underlying servers, wipe file systems, or launch internal attacks. | **RCE Prevention via Lambda Sandbox:** Submissions run in isolated AWS Lambda Workers with strict CPU, RAM, Execution Timeout, and Network Access restrictions. |
| **Traffic Spikes & Server Overload:** Sudden submission bursts cause server slowdowns or system crashes during contests. | **Asynchronous Buffering with Amazon SQS:** Submission payloads are pushed to SQS queues, allowing background Lambda Workers to process workloads smoothly. |
| **High Idle Server Maintenance Costs:** Maintaining 24/7 dedicated servers or container clusters incurs heavy costs during low-traffic periods. | **Serverless Pay-As-You-Go:** Infrastructure scales to zero when idle, cutting operational infrastructure costs by up to 75%. |
| **Managing Large Testcase Datasets:** Large input/output files (MBs to GBs) overwhelm traditional relational databases (RDBMS). | **Tiered Storage (S3 + DynamoDB):** Fast metadata queries via DynamoDB NoSQL, while large testcases are stored securely in Amazon S3. |

---

## 4. CORE FEATURES

1. **Problemset & Tagging System:**
   - Filter problemsets by title, difficulty (Easy, Medium, Hard), and algorithm tags (DP, Graph, Binary Tree...).
   - Real-time acceptance rate statistics and submission counts.

2. **Interactive Code Editor & Runner:**
   - Multi-language compilation and execution support: **C++, Java, Python, JavaScript**.
   - **Run Code** (dry run with custom inputs) and **Submit Code** (full evaluation against testcase suites).
   - Automated error reporting: Compile Error, Runtime Error, TLE, MLE.

3. **Automated Isolated Sandbox Execution:**
   - Decoupled API entrypoint and evaluation execution environment.
   - Character-by-character output diff comparison against ground truth testcase outputs.

4. **Developer Social Network:**
   - Share knowledge posts, discuss solutions via comments, and follow other developers.
   - Achievement badges and gamified developer progress tracking.

5. **User Analytics Dashboard:**
   - Submission activity heatmaps.
   - Detailed submission history logs including source code, runtime, and memory consumption.

---

## 5. SYSTEM ARCHITECTURE

### 5 Pillars of AWS Well-Architected Framework
CodExecute's architecture adheres strictly to the 5 pillars of the **AWS Well-Architected Framework**:

1. **Operational Excellence:** Infrastructure as Code (IaC SAM/CloudFormation) deployment pipelines, centralized logging and telemetry using Amazon CloudWatch.
2. **Security:** Least-Privilege IAM Roles, Data Encryption At-Rest (KMS) & In-Transit (TLS 1.3/HTTPS via CloudFront), isolated Lambda execution sandbox.
3. **Reliability:** Multi-AZ High Availability fault tolerance, automated retry routines, and SQS Dead-Letter Queue (DLQ) safeguards.
4. **Performance Efficiency:** Global edge distribution via CloudFront CDN, single-digit millisecond latency NoSQL queries with Amazon DynamoDB.
5. **Cost Optimization:** Strict Event-Driven Pure Serverless architecture (Lambda Pay-As-You-Go).

### Project Architecture Diagram
![CodExecute Architecture Diagram](/images/2-Proposal/architect-codexecute.drawio.png)

### Functional Architecture Layer Analysis
Based on the AWS Serverless Architecture Diagram, CodExecute is structured into 6 dedicated functional layers deployed in the `ap-southeast-1` Region:

1. **CDN & Edge Security Layer:**
   - **Amazon CloudFront:** Delivers React static assets from S3 globally with low latency and acts as a Reverse Proxy routing `/api/*` requests to API Gateway.
   - **AWS WAF:** Protects web entrypoints against Layer 7 attacks, SQL Injection, XSS, and enforces Rate Limiting against spam traffic.
   - **OAuth Providers Authentication:** Authenticates users via Google and GitHub OAuth providers.

2. **Ingress & Static Hosting Layer:**
   - **AWS S3 Bucket (Static Hosting):** Stores compiled production static web assets (HTML/JS/CSS).
   - **AWS API Gateway (REST API):** Unified API entrypoint receiving HTTP requests from CloudFront and synchronously invoking (**Synchronous Invoke**) the Lambda API Handler.

3. **Serverless Compute & Sandbox Layer:**
   - **AWS ECR (Container Registry):** Manages and stores container images for Lambda function deployments.
   - **AWS Lambda (API Handler):** Executes FastAPI backend logic, performs CRUD operations on DynamoDB, fetches S3 assets, and pushes submission jobs to SQS.
   - **AWS Lambda (Code Executor Sandbox):** Triggered by SQS, fetches full testcase suites from S3, compiles and evaluates code in isolated sandbox environments, and writes results to DynamoDB.

4. **Queue Processing Layer:**
   - **AWS SQS (Submission Queue):** Asynchronous submission job queue regulating workload throughput and triggering Worker Lambdas.

5. **Database & Storage Layer:**
   - **AWS DynamoDB (Submission & Problem):** High-speed NoSQL database storing user profiles, problemsets, submissions, and social data.
   - **AWS S3 Bucket (Testcases):** Dedicated bucket storing problem input/output testcase text files.
   - **AWS S3 Bucket (User Avatar):** Dedicated bucket storing user profile avatar media.

6. **Security & Monitoring Layer:**
   - **IAM Roles (Execution Role):** Enforces Least-Privilege Access control for service interactions.
   - **AWS CloudWatch (Logs & Metrics):** Centralized execution logging, operational telemetry, and metrics dashboard.
   - **AWS SNS:** Emits automated incident notification alerts to system administrators.

---

### End-to-End Execution Workflow (Steps 1 to 9)
The end-to-end evaluation flow operates via a **9-step process**:

1. **Step 1:** User submits an **HTTP Request** from the browser after authenticating via **OAuth Providers** (Google/GitHub).
2. **Step 2:** **Amazon CloudFront** fetches static web assets (**Fetch Static Files**) from **AWS S3 Bucket (Static Hosting)** to serve the React UI.
3. **Step 3:** For API requests (`/api/*`), CloudFront forwards API routes (**Forward API Routing**) to **AWS API Gateway (REST API)**.
4. **Step 4:** API Gateway synchronously invokes (**Synchronous Invoke**) the **AWS Lambda (API Handler)**.
5. **Step 5a, 5b, 5c:** Lambda API Handler performs key operations:
   - **Step 5a:** Reads/writes user & problem metadata (**CRUD User/Problem Data**) in **Amazon DynamoDB**.
   - **Step 5b:** Fetches sample testcases (**Fetch Sample Testcases**) from **AWS S3 Bucket (Testcases)**.
   - **Step 5c:** Fetches user avatars (**Fetch User Avatar**) from **AWS S3 Bucket (User Avatar)**.
6. **Step 6:** Lambda API Handler pushes the submission job payload (**Push Execution Job**) to **AWS SQS (Submission Queue)** and immediately returns a `Pending` response to the user.
7. **Step 7:** **AWS SQS** automatically triggers an **Event Trigger** to invoke **AWS Lambda (Code Executor Sandbox)**.
8. **Step 8:** Lambda Code Executor Sandbox fetches the complete testcase dataset (**Fetch Full Testcases**) from **AWS S3 Bucket (Testcases)**.
9. **Step 9:** Lambda Code Executor Sandbox compiles and evaluates code in the isolated container sandbox and saves results (**Save Result**) to **Amazon DynamoDB**.

---

### Inventory of Core AWS Services

Below is the complete inventory of AWS services implemented in CodExecute:

| No. | AWS Service | Role & Responsibilities in CodExecute | Selection Rationale & Technical Benefits |
| :---: | :--- | :--- | :--- |
| **1** | **Amazon CloudFront** | Distributes React Frontend static assets globally from S3 with ultra-low latency. Acts as reverse proxy routing `/api/*` requests to API Gateway. | Accelerates global page load times using edge caching. Enables automated HTTPS/TLS 1.3 encryption and built-in DDoS protection. |
| **2** | **AWS WAF** | Protects CloudFront and API Gateway entrypoints against web exploits. | Filters malicious web traffic (SQLi, XSS, Bot Attack) and enforces Rate Limiting on API endpoints. |
| **3** | **Amazon S3** | **Bucket 1:** Frontend static hosting (HTML/JS/CSS).<br>**Bucket 2:** Testcase input/output file repository.<br>**Bucket 3:** User profile media storage. | Ultra-cost-effective storage ($0.023/GB), 99.999999999% (11 9's) durability. Infinite capacity scaling and secure Presigned URL capabilities. |
| **4** | **Amazon API Gateway** | Unified entry point managing RESTful API endpoints and routing HTTP requests to Lambda API handlers. | Built-in Rate Limiting / Throttling, JWT authentication integration, CORS support, and CloudFront binding. |
| **5** | **AWS ECR** | Container Registry storing Docker images for Lambda API Handler and Code Executor Sandbox. | Secure container image management with native AWS Lambda deployment integration. |
| **6** | **AWS Lambda** | **Lambda API:** Runs FastAPI RESTful backend logic.<br>**Lambda Worker:** Consumes messages from SQS, executes code in an isolated Sandbox runtime. | Millisecond-level billing precision (pay only when code executes). Automatic scaling from 0 to thousands of concurrent executions. |
| **7** | **Amazon SQS** | Asynchronous submission queue (`Submission Queue`) decoupling API handlers from background code evaluation workers. | Buffers traffic spikes during competitive programming contests. Prevents data loss via Message Retention and DLQ patterns. |
| **8** | **Amazon DynamoDB** | Stores structured platform data: `Users`, `Problems`, `Submissions`, `TestCases`, `Posts`, `Notifications`, and `UserFollows`. | Single-digit millisecond query performance. On-Demand auto-scaling handles millions of queries without complex cluster management. |
| **9** | **AWS IAM** | Manages identity, enforcing Least-Privilege Access control for cross-service communications. | Implements Zero-Trust security model via IAM Execution Roles and Resource-based Policies. |
| **10** | **Amazon CloudWatch** | Centralizes logging from Lambda API & Worker, and API Gateway. Tracks performance metrics and sets up proactive Alarms. | Real-time system observability. Triggers automated alarms when error rates exceed thresholds, accelerating debugging. |
| **11** | **Amazon SNS** | Publishes automated incident notification alerts from CloudWatch Alarms to administrators via email. | Guarantees rapid incident response through instant alert notification channels. |

---

## 8. IMPLEMENTATION ROADMAP & TIMELINE 

The project is executed over a **7-week duration** (from **June 15, 2026** to **July 31, 2026**) structured into **5 distinct phases**:

* **Phase 1: Infrastructure & IaC Setup** *(15/06/2026 – 24/06/2026)*
  > Provision S3 Buckets, DynamoDB Tables, SQS Queues, and IAM Roles using AWS SAM & Terraform scripts.

* **Phase 2: Frontend & Backend Core Development** *(25/06/2026 – 05/07/2026)*
  > Develop React + Vite UI (Interactive Code Editor, Problemset) & FastAPI RESTful APIs on AWS Lambda.

* **Phase 3: Asynchronous Pipeline & Lambda Sandbox** *(06/07/2026 – 16/07/2026)*
  > Implement Amazon SQS queues and deploy isolated AWS Lambda Workers for automated code evaluation.

* **Phase 4: Load Testing & Security Hardening** *(17/07/2026 – 25/07/2026)*
  > Conduct load testing (1,000 VUs via Locust/k6), security penetration testing against RCE, and verify DLQ failover behavior.

* **Phase 5: Cost Optimization & Official Go-Live** *(26/07/2026 – 31/07/2026)*
  > Optimize Lambda RAM/Timeout configurations, configure CloudWatch Budgets alarms, and officially **GO-LIVE on July 31, 2026**.

### Phase Breakdown

| Phase | Timeline | Key Tasks | Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1: Infrastructure & IaC Setup** | **15/06/2026 – 24/06/2026** *(10 days)* | - Design architecture adhering to AWS Well-Architected framework.<br>- Write AWS SAM / Terraform scripts to provision S3, DynamoDB, SQS, IAM.<br>- Setup CI/CD pipeline using GitHub Actions. | - AWS Dev environment provisioned.<br>- Complete IaC SAM Template repository. |
| **Phase 2: Frontend & Backend Core Development** | **25/06/2026 – 05/07/2026** *(11 days)* | - Develop React + Vite UI (Code Editor, Problem filtering, User profile).<br>- Build FastAPI backend endpoints for Auth, Problems, and Submissions.<br>- Containerize Lambda API Handler; integrate API Gateway & CloudFront. | - Web UI deployed on S3 + CloudFront.<br>- RESTful APIs functional on Lambda & DynamoDB. |
| **Phase 3: Asynchronous Pipeline & Lambda Sandbox** | **06/07/2026 – 16/07/2026** *(11 days)* | - Implement submission queuing via Amazon SQS.<br>- Develop isolated Lambda Sandbox execution for 4 languages.<br>- Connect SQS Event Source Mapping to Worker Lambda. | - Automated async grading pipeline operational.<br>- RCE prevention verified in Lambda Sandbox. |
| **Phase 4: Load Testing & Security Hardening** | **17/07/2026 – 25/07/2026** *(9 days)* | - Perform load testing up to 1,000 VUs using Locust/k6.<br>- Conduct security penetration testing against RCE, SQLi, XSS.<br>- Test DLQ failover behavior and retry policies. | - Load test report meeting target SLAs.<br>- 100% High/Critical security vulnerabilities patched. |
| **Phase 5: Cost Optimization & Go-Live** | **26/07/2026 – 31/07/2026** *(6 days)* | - Configure CloudWatch Alarms & Cost Budgets Alert.<br>- Tune AWS Lambda RAM/Timeout parameters for cost efficiency.<br>- Cut over to Production and finalize project documentation. | - **Project OFFICIALLY GOES LIVE on July 31, 2026.**<br>- Architecture & Operations handbook finalized. |

---

## 9. BUDGET ESTIMATION & COST OPTIMIZATION

### 1. Monthly Budget Estimation

Estimates are calculated based on an average workload of **100,000 code submissions/month** and **500,000 API requests/month**.

| AWS Service | Expected Monthly Utilization | Unit Price Reference (ap-southeast-1) | Estimated Monthly Cost (USD) |
| :--- | :--- | :--- | :---: |
| **AWS Lambda** | 500,000 API Requests + 100,000 Worker executions (512MB RAM, 800ms avg) | $0.20 / 1M Requests + Compute time | **$3.80** |
| **Amazon API Gateway** | 500,000 HTTP API calls | $1.00 / 1M Requests | **$0.50** |
| **Amazon SQS** | 200,000 SQS Requests (SendMessage + ReceiveMessage) | $0.40 / 1M Requests | **$0.08** |
| **Amazon DynamoDB** | 1,000,000 Read/Write Units (On-Demand) + 5GB Storage | $0.25 / 1M WCU, $0.05 / 1M RCU | **$3.20** |
| **Amazon S3** | 15GB Storage (Testcases + User Media + Web Assets) + 100k GET/PUT | $0.023 / GB | **$0.65** |
| **Amazon CloudFront** | 50GB Data Transfer Out + 500k HTTPS Requests | $0.09 / GB | **$4.50** |
| **AWS WAF** | 1 Web ACL + 2 Rules (Rate Limiting & Core Rule Set) + 500k Requests | $5.00/Web ACL + $1.00/Rule + $0.60/1M Requests | **$7.30** |
| **AWS ECR** | 5GB Storage for Container Images (Lambda Sandbox & API Handler) | $0.10 / GB Storage / month | **$0.50** |
| **Amazon SNS** | ~100 Email notifications triggered from CloudWatch Alarms | First 1,000 Emails & 1M Publish requests free | **$0.00** |
| **Amazon CloudWatch** | 3GB Ingestion Logs + 5 Custom Metrics + 3 Alarms | $0.57 / GB Logs | **$2.70** |
| **AWS IAM** | All IAM Users, Roles, and Policies | Free | **$0.00** |
| **TOTAL ESTIMATED MONTHLY COST:** | | | **~$23.23 USD / month** |

> 💡 *Note:* Under the **AWS Free Tier** during the first 12 months (1M Lambda requests/mo, 1M API Gateway requests/mo, 25GB DynamoDB storage, 5GB S3 storage, 1,000 SNS Emails/mo), actual out-of-pocket costs will remain **< $8.50 USD/month** (primarily AWS WAF Base ACL).

---

### 2. Cost Optimization Strategy

1. **Pure Serverless Pay-As-You-Go Architecture:**
   - Utilizing **AWS Lambda** and **API Gateway HTTP APIs** (70% cheaper than REST APIs) eliminates 24/7 idle server costs.

2. **DynamoDB On-Demand vs Provisioned Capacity:**
   - Uses **On-Demand Capacity** during initial launch, transitioning core tables to **Provisioned Capacity + Auto Scaling** as traffic stabilizes to save an additional 40%.

3. **S3 Lifecycle Rules & Compression:**
   - Implements **S3 Lifecycle Rules** transitioning logs older than 90 days to **S3 Glacier Flexible Retrieval** (saving 85% storage cost).
   - Compresses testcase files with Gzip before S3 upload to reduce data transfer bandwidth.

4. **SQS Long Polling:**
   - Configures SQS `ReceiveMessageWaitTimeSeconds = 20` (Long Polling) to cut empty receive request charges by up to 90%.

5. **ECR Storage & WAF Rule Optimization:**
   - Enforces an **ECR Lifecycle Policy** auto-deleting untagged container images and maintaining only the 3 latest images to keep ECR storage below 5GB.
   - Combines **AWS WAF** with CloudFront Caching and Rate Limiting to block malicious traffic at Edge locations, safeguarding the Lambda backend from costly spikes.

6. **AWS Lambda Power Tuning:**
   - Leverages *AWS Lambda Power Tuning* to select optimal memory/vCPU ratios for Lambda API & Worker functions, minimizing execution time and billing duration.

---

## 10. RISK ASSESSMENT & MITIGATION STRATEGIES

| No. | Risk Category | Risk Analysis | Severity | Mitigation Strategy |
| :---: | :--- | :--- | :---: | :--- |
| **1** | **Security** | **RCE in Sandbox:** Malicious user code attempting file deletion, fork bombs, or internal VPC probing. | **CRITICAL** | - Execute code in non-root **Lambda Isolated Sandbox**.<br>- Disable external network access (`VPC Network: Disabled / Strict Security Groups`) in Worker.<br>- Enforce hard limits: RAM (512MB), CPU (1 Core), Timeout (5s), Process limit (20 pids). |
| **2** | **Performance** | **SQS Backlog or Lambda Cold Start:** High submission concurrency causing evaluation delay during contests. | **HIGH** | - Enable **Provisioned Concurrency** for critical Lambdas during live contest hours.<br>- Auto-scale Worker instances based on SQS `ApproximateNumberOfMessagesVisible`. |
| **3** | **Security** | **DDoS / API Spam:** Malicious traffic exhausting AWS budget. | **HIGH** | - Enable **AWS WAF** and **API Gateway Throttling / Rate Limiting** (max 20 req/min per IP).<br>- Bind CloudFront Geo Blocking and AWS Shield Standard. |
| **4** | **Operations** | **Submission Loss due to Crash:** Worker crashes mid-grading. | **MEDIUM** | - Configure appropriate SQS `VisibilityTimeout`.<br>- Enable **Dead-Letter Queue (DLQ)** to retain failed messages after 3 retries for developer inspection. |
| **5** | **Cost** | **Unexpected Cost Spike:** Infinite loops in code or runaway CloudWatch logging. | **MEDIUM** | - Set **AWS Budgets Alerts** notifying via Email when cost exceeds $20/month.<br>- Set CloudWatch Log Retention to 14 days maximum. |

---

## 11. EXPECTED OUTCOMES

Upon completion on **July 31, 2026**, the **CodExecute** system expects to achieve:

### Technical KPIs
* **Availability SLA:** Minimum **99.9%** uptime via Multi-AZ Serverless infrastructure.
* **API Response Latency:** < 200ms for standard API read/write operations.
* **Submission Processing Latency:** < 2.0 seconds from Submit click to result display (for testcases under 50MB).
* **Concurrent Capacity:** Smoothly handles **1,000 concurrent submissions** without request drops.
* **Zero RCE Vulnerabilities:** 100% of untrusted user code isolated inside Lambda Sandbox.

### Business & Operational Outcomes
* **75% Infrastructure Cost Savings** compared to traditional EC2/Dedicated server hosting.
* **High Maintainability:** 100% Infrastructure as Code (IaC SAM/CloudFormation) enabling environment recreation in under 15 minutes.
* **Empowering Developers:** Provides developers with a standardized, reliable algorithm evaluation platform to hone coding skills.