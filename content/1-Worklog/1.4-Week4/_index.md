---
title: "Week 4 Worklog"
date: 2026-07-06
weight: 4
chapter: false
pre: " <b> 1.4. </b> "
includeInReport: true
reportTableColumns:
  - Day
  - Task
  - Completion Date
reportHeadings:
  - Week 4 Objectives
  - Tasks to be carried out this week
  - Week 4 Achievements
reportType: worklog
---

### Week 4 Objectives:

* Learn NoSQL Database (Amazon DynamoDB) & testcase dataset management techniques on Amazon S3.
* Design DynamoDB Single-Table schema, provision GSIs, and configure cost-optimized S3 Lifecycle Rules.

### Tasks to be carried out this week:
| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Learn Amazon DynamoDB: Partition Key, Sort Key, Global Secondary Index (GSI), and On-Demand Capacity mode | 07/06/2026 | 07/06/2026 | <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html> |
| 3 | - Learn S3 Lifecycle Rules, S3 Glacier Flexible Retrieval archiving, and Gzip compression for large testcase files | 07/07/2026 | 07/07/2026 | <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html> |
| 4 | - **Practice:** <br>&emsp; + Design data schema for `Users`, `Problems`, `Submissions`, `Posts`, and `UserFollows` entities <br>&emsp; + Provision DynamoDB table and GSI `SubmissionUserIndex` | 07/08/2026 | 07/08/2026 | <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html> |
| 5 | - **Practice:** <br>&emsp; + Write Python (boto3) scripts to perform CRUD operations on problems and user data <br>&emsp; + Benchmark low-latency data queries (Single-digit ms) | 07/09/2026 | 07/09/2026 | <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html> |
| 6 | - **Practice:** <br>&emsp; + Upload sample Testcase input/output files to Amazon S3 <br>&emsp; + Configure S3 Lifecycle Rule to archive testcase logs older than 90 days to Glacier | 07/10/2026 | 07/10/2026 | <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html> |


### Week 4 Achievements:

* Designed and deployed DynamoDB On-Demand schema supporting grading evaluation and developer social network features.
* Programmed CRUD data operations using DynamoDB Python SDK (boto3).
* Uploaded and managed problem testcase files on Amazon S3 with automated cost-saving lifecycle rules.
