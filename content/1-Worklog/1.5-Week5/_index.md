---
title: "Week 5 Worklog"
date: 2026-07-13
weight: 5
chapter: false
pre: " <b> 1.5. </b> "
includeInReport: true
reportTableColumns:
  - Day
  - Task
  - Completion Date
reportHeadings:
  - Week 5 Objectives
  - Tasks to be carried out this week
  - Week 5 Achievements
reportType: worklog
---

### Week 5 Objectives:

* Understand Serverless Web Application architecture (AWS Lambda, API Gateway) and container packaging with Docker & ECR.
* Develop Backend RESTful APIs (FastAPI) for CodExecute, integrating JWT authentication and DynamoDB persistence.

### Tasks to be carried out this week:
| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Learn Serverless Web API architecture: Mangum ASGI Adapter, API Gateway HTTP API Proxy Integration | 07/13/2026 | 07/13/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html> |
| 3 | - Learn JWT Token authentication mechanisms & OAuth Providers (Google/GitHub login) | 07/14/2026 | 07/14/2026 | <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html> |
| 4 | - **Practice:** <br>&emsp; + Containerize FastAPI backend into Docker image & push to AWS ECR repository <br>&emsp; + Provision AWS Lambda function (API Handler) from ECR image | 07/15/2026 | 07/15/2026 | <https://docs.aws.amazon.com/lambda/latest/dg/images-create.html> |
| 5 | - **Practice:** <br>&emsp; + Create API Gateway HTTP API linked to Lambda API Handler <br>&emsp; + Configure CORS policies allowing access from React Frontend | 07/16/2026 | 07/16/2026 | <https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html> |
| 6 | - **Practice:** <br>&emsp; + Develop API Endpoints: Auth API, Problemset List, Code Run API, Post/Comment APIs <br>&emsp; + Test endpoints via Postman | 07/17/2026 | 07/17/2026 | <https://fastapi.tiangolo.com/> |


### Week 5 Achievements:

* Containerized FastAPI backend application on AWS ECR and deployed to AWS Lambda.
* Created and configured API Gateway HTTP API for seamless Frontend to Backend routing.
* Completed RESTful API backend handling problem management, developer social posts, and sample code execution.
