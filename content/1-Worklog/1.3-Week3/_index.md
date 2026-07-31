---
title: "Week 3 Worklog"
date: 2026-06-29
weight: 3
chapter: false
pre: " <b> 1.3. </b> "
includeInReport: true
reportTableColumns:
  - Day
  - Task
  - Completion Date
reportHeadings:
  - Week 3 Objectives
  - Tasks to be carried out this week
  - Week 3 Achievements
reportType: worklog
---

### Week 3 Objectives:

* Understand Amazon Virtual Private Cloud (VPC) & Amazon CloudFront CDN architecture.
* Learn Multi-AZ Subnet planning, AWS WAF perimeter protection, and React Frontend distribution via CloudFront.

### Tasks to be carried out this week:
| Day | Task | Start Date | Completion Date | Reference Material |
| --- | --- | --- | --- | --- |
| 2 | - Learn VPC fundamentals: IPv4 CIDR Blocks (`10.0.0.0/16`), Subnet planning (2 Public Subnets & 2 Private Subnets across Multi-AZ) | 06/29/2026 | 06/29/2026 | <https://docs.aws.amazon.com/vpc/latest/userguide/configure-your-vpc.html> |
| 3 | - Learn Amazon CloudFront CDN: Edge Locations, Cache Behaviors, Custom Domain & HTTPS SSL/TLS Certificates | 06/30/2026 | 06/30/2026 | <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Welcome.html> |
| 4 | - **Practice:** <br>&emsp; + Create Custom VPC, attach Internet Gateway & configure Route Tables <br>&emsp; + Configure Security Groups for internal environment | 07/01/2026 | 07/01/2026 | <https://docs.aws.amazon.com/vpc/latest/userguide/vpc-subnets-routing.html> |
| 5 | - **Practice:** <br>&emsp; + Create CloudFront Distribution pointing to S3 Static Web Bucket for CodExecute React Frontend | 07/02/2026 | 07/02/2026 | <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DistributionConfig.html> |
| 6 | - **Practice:** <br>&emsp; + Configure CloudFront Cache Behavior forwarding `/api/*` to API Gateway <br>&emsp; + Enable AWS WAF Web ACL with Rate Limiting rules against DDoS/Spam | 07/03/2026 | 07/03/2026 | <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html> |


### Week 3 Achievements:

* Designed and built multi-AZ Custom VPC isolating Public and Private network environments.
* Successfully distributed React Frontend application via CloudFront CDN for low-latency Edge delivery.
* Configured API routing through CloudFront and enabled AWS WAF perimeter protection against Layer 7 attacks.
