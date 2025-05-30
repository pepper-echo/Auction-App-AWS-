Serverless auction platform built using AWS services: Lambda, API Gateway, DynamoDB, S3, and Step Functions. It allows users to place bids on items, validating each bid with a multi-step process.

Features
- Fully serverless architecture using AWS
- Proxy integration with API Gateway
- Step Functions for validating bids
- S3-hosted frontend with CORS enabled
- Real-time validation of bids against reserve prices and user balance
- CloudWatch logging for debugging
- Postman-tested RESTful API endpoints
  
Architecture
- Frontend: Hosted on Amazon S3 (static website hosting)
- Backend: AWS Lambda (Node.js/Python), API Gateway with proxy integration
- State Management: AWS Step Functions
- Database: Amazon DynamoDB (Users, Bids, Auctions)
- Logging/Debugging: AWS CloudWatch

Workflows
1. Place Bid
- Endpoint: `POST /bid?auction=<auctionId>`
- Integration: Proxy integration (API Gateway)
- Step Function Flow:
  1. Validate user balance
  2. Validate bid amount against current highest + reserve
  3. Write bid to DynamoDB if valid

Other Functionalities
- Upload item to auction
- Close auction
- Retrieve bids and auction status

Testing
- Used **Postman** to test all routes locally and in production
- CORS was configured on API Gateway to allow frontend S3 access
- Debugging and tracing done using **CloudWatch logs**

Technologies Used
- **Python** / **Node.js** (AWS Lambda)
- **AWS Lambda**
- **API Gateway (proxy integration)**
- **DynamoDB**
- **Amazon S3**
- **Step Functions**
- **CloudWatch**
- **Postman**
