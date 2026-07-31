---
title: "Week 2 Worklog"
date: 2026-06-22
weight: 2
chapter: false
pre: " <b> 1.2. </b> "
includeInReport: true
reportTableColumns:
  - Day
  - Task
  - Completion Date
reportHeadings:
  - Week 2 Objectives
  - Tasks to be carried out this week
  - Week 2 Achievements
reportType: worklog
---

### Week 2 Objectives:

* Understand AWS IAM core concepts: Users, Groups, Roles, and Policies.
* Design security policies for CodExecute: Least privilege execution roles for Lambda & S3 Bucket Policies.

### Tasks to be carried out this week:
| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Learn IAM fundamentals: IAM Users, Groups, Managed Policies vs Inline Policies | 06/22/2026 | 06/22/2026 | <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html> |
| 3 | - Design least-privilege architecture for Lambda API Handler, Lambda Executor Sandbox, S3, and DynamoDB | 06/23/2026 | 06/23/2026 | <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html> |
| 4 | - **Practice:** <br>&emsp; + Create S3 Buckets (`codexecute-static-web`, `codexecute-testcases`, `codexecute-user-avatars`) <br>&emsp; + Configure S3 Block Public Access & CORS | 06/24/2026 | 06/24/2026 | <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html> |
| 5 | - **Practice:** <br>&emsp; + Create IAM Execution Roles for Lambda API Handler and Lambda Sandbox Executor <br>&emsp; + Grant S3 Testcase ReadAccess & DynamoDB Result WriteAccess without long-term keys | 06/25/2026 | 06/25/2026 | <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html> |
| 6 | - Learn AWS Security Token Service (STS) & test IAM Role permissions via AWS CLI | 06/26/2026 | 06/26/2026 | <https://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html> |


### Week 2 Achievements:

* Mastered IAM Policy JSON structure (Effect, Action, Resource, Condition).
* Successfully created S3 Buckets for hosting static web assets, problem testcase files, and user avatars.
* Configured IAM Execution Roles following least-privilege principles for Serverless Lambda functions.
