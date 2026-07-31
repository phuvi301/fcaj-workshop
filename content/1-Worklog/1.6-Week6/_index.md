---
title: "Week 6 Worklog"
date: 2026-07-20
weight: 6
chapter: false
pre: " <b> 1.6. </b> "
includeInReport: true
reportTableColumns:
  - Day
  - Task
  - Completion Date
reportHeadings:
  - Week 6 Objectives
  - Tasks to be carried out this week
  - Week 6 Achievements
reportType: worklog
---

### Week 6 Objectives:

* Understand Amazon SQS asynchronous message queuing and isolated Sandbox execution design on AWS Lambda.
* Deploy secure, asynchronous automated code evaluation pipeline protected against Remote Code Execution (RCE) with Dead-Letter Queue (DLQ) error handling.

### Tasks to be carried out this week:
| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Learn Amazon SQS: Standard Queue, Message Retention, Long Polling (`WaitTime=20s`), Visibility Timeout, and Dead-Letter Queue (DLQ) | 07/20/2026 | 07/20/2026 | <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html> |
| 3 | - Learn resource limits & Sandbox isolation techniques (Memory, CPU, Timeout, Process PIDs) preventing RCE in Lambda Workers | 07/21/2026 | 07/21/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html> |
| 4 | - **Practice:** <br>&emsp; + Provision SQS Queue `codexecute-submission-queue` with DLQ `codexecute-submission-dlq` <br>&emsp; + Configure Lambda API Handler to push code submission messages to SQS | 07/22/2026 | 07/22/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html> |
| 5 | - **Practice:** <br>&emsp; + Build Lambda Code Executor Sandbox (Python/Docker on ECR) triggered automatically by SQS <br>&emsp; + Worker fetches testcases from S3, executes code (C++, Java, Python, JS), and updates evaluation results to DynamoDB | 07/23/2026 | 07/23/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/services-sqs.html> |
| 6 | - **Practice:** <br>&emsp; + Test malicious payload execution, infinite loops (TLE), and high memory overflow (MLE) <br>&emsp; + Verify complete Sandbox security isolation | 07/24/2026 | 07/24/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/security-isolation.html> |


### Week 6 Achievements:

* Built SQS message queue buffering submission traffic spikes and preventing platform overload.
* Deployed isolated Lambda Code Executor Sandbox supporting automated multi-language evaluation (C++, Java, Python, JavaScript).
* Effectively handled malicious scripts and runtime timeouts (TLE/MLE) without impacting shared infrastructure.
