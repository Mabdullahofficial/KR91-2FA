Steps to Deploy the Solution:

1. Clone the Repository
Access the Solution directory by navigating to /KR91-2FA-CCL-Assessment.
Clone the repository to your local machine by running the following commands:
bash
git clone https://github.com/Mabdullahofficial/KR91-2FA-Cybernetic-Controls-Limited-Asseessment.git  
Cd KR91-2FA-Cybernetic-Controls-Limited-Asseessment/KR91-2FA-CCL-Assessment  
2. Build and Push Docker Images
Use the provided Dockerfiles to build and push the container images for the token generation and validation services.
Run the following commands:
Build and push the Token Generation service:
bash

cd token-generation  
docker build -t <your-dockerhub-username>/token-generation .  
docker push <your-dockerhub-username>/token-generation  

Build and push the Token Validation service:
bash

cd ../token-validation  
docker build -t <your-dockerhub-username>/token-validation .  
docker push <your-dockerhub-username>/token-validation  
3. Deploy the Infrastructure Using AWS CloudFormation
Go to the AWS Management Console and navigate to the CloudFormation service.
Click on "Create stack" and select "With new resources (standard)".
Upload the ecsFargateDynamoDbSnsSolution.yaml CloudFormation template from the repository.
Provide the necessary parameters:
EnvironmentName: Example - dev
DynamoDBTableName: Example - Tokens
SNSTopicName: Example - 2FA-SNSTopic
TokenGenerationImageURI: URI of the token-generation image pushed to Docker Hub or ECR.
TokenValidationImageURI: URI of the token-validation image pushed to Docker Hub or ECR.
ClusterName: Name of your ECS cluster.
Proceed with the stack creation by following the on-screen instructions.
Once the stack creation is complete, the following infrastructure components will be deployed:
An ECS cluster with two Fargate tasks for token generation and validation.
A DynamoDB table to store and manage tokens.
An SNS topic to send tokens to user email or phone numbers.
API Gateway for exposing RESTful APIs to interact with the services.

4. Test the Solution
Generate Token:
Copy the TokenCreationAPIURL from the CloudFormation stack outputs.
Use Postman or curl to call the API:
bash

curl -X POST -H "Content-Type: application/json" \
-d '{"user_id": "user123", "phone_number": "+1234567890"}' \
<TokenCreationAPIURL>  
The API will return the token in the response and send it to the user's phone number via SNS.
Validate Token:
Copy the TokenValidationAPIURL from the CloudFormation stack outputs.
Use Postman or curl to validate the token:
bash

curl -X POST -H "Content-Type: application/json" \
-d '{"token": "<token_received_via_sms>"}' \
<TokenValidationAPIURL>  
The API will verify the token and return the result (success or error).
Note
AWS Credentials: Ensure your local machine is configured with the necessary AWS credentials.
SNS Configuration: Verify that the phone numbers receiving the messages are confirmed in Amazon SNS.
Replace placeholders such as <your-dockerhub-username>, <TokenCreationAPIURL>, and <TokenValidationAPIURL> with your actual values.
Review and customize the parameters in the CloudFormation template (ecsFargateDynamoDbSnsSolution.yaml) as per your requirements.

