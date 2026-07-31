---
title: "Week 7 Worklog"
date: 2026-07-27
weight: 7
chapter: false
pre: " <b> 1.7. </b> "
includeInReport: true
reportTableColumns:
  - Day
  - Task
  - Completion Date
reportHeadings:
  - Week 7 Objectives
  - Tasks to be carried out this week
  - Week 7 Achievements
reportType: worklog
---

### Week 7 Objectives:

* Automate end-to-end CodExecute infrastructure via Infrastructure as Code (AWS SAM/Terraform), perform load testing, and optimize operating costs.
* Audit system-wide security, defend Capstone project solution, and complete the final 7-week internship documentation.

### Tasks to be carried out this week:
| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Write AWS SAM Template (`template.yaml`) defining Serverless infrastructure (Lambda, API Gateway, SQS, DynamoDB, S3, IAM Roles) | 07/27/2026 | 07/27/2026 | <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html> |
| 3 | - **Practice:** <br>&emsp; + Automate stack deployment for CodExecute project using AWS SAM CLI <br>&emsp; + Verify resource state and permission boundaries post-deployment | 07/28/2026 | 07/28/2026 | <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html> |
| 4 | - **Practice:** <br>&emsp; + Conduct load testing using Locust/k6 (sustaining up to 1,000 concurrent users) <br>&emsp; + Configure CloudWatch Alarms & SNS Notifications for real-time alerting | 07/29/2026 | 07/29/2026 | <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html> |
| 5 | - Summarize performance benchmarks, monthly operational cost breakdown (~$23.23/month), and finalize 7-week internship report | 07/30/2026 | 07/30/2026 |  |
| 6 | - Present CodExecute Capstone Project to FCAJ mentors, defend architecture design, and graduate from internship program | 07/31/2026 | 07/31/2026 |  |


### Week 7 Achievements:

* Automated 100% of CodExecute project infrastructure using IaC scripts (AWS SAM).
* System successfully passed load testing, serving 1,000 concurrent users without bottlenecks.
* Successfully completed all 7 weeks of the FCAJ internship program, finalized report documentation, and received capstone evaluation.
