### Steps to Deploy the 2FA-Solution:

1. **Clone the Repository:**
  - Access the Solution directory by navigating to /KR91-2FA-CCL-Assessment.
Clone the repository to your local machine by running the following commands`.
  - Clone the repository to your local machine by running the following command:
     ```bash
     git clone https://github.com/Mabdullahofficial/KR91-2FA-Cybernetic-Controls-Limited-Asseessment.git  
     cd KR91-2FA-Cybernetic-Controls-Limited-Asseessment/KR91-2FA-CCL-Assessment  
     ```

2. **Build and Push Docker Images:**
  - Run the following commands.
  - 1. Build and push the Token Generation service:
     ```bash
     cd token-generation  
      docker build -t <your-dockerhub-username>/token-generation .  
      docker push <your-dockerhub-username>/token-generation  
     ```
  - 2. Build and push the Token Generation service:
     ```bash
     cd ../token-validation  
      docker build -t <your-dockerhub-username>/token-validation .  
      docker push <your-dockerhub-username>/token-validation  
     ```

3. **Deploy Infrastructure using AWS Console:**
  - Go to the AWS Management Console and navigate to the CloudFormation service.
  - Click on "Create stack" and select "With new resources (standard)".
  - Upload the 2FA-CloudFormationtemplate.yaml CloudFormation template from the repository.
  - Provide the necessary parameters like `EnvironmentName`, `DynamoDBTableName`, `SNSTopicName`, `TokenGenerationImageURI`, `TokenValidationImageURI`, and `ClusterName`. 
  - Proceed with the stack creation by following the on-screen instructions.
  - Once the stack creation is complete, the infrastructure components including the DynamoDB table, ECS Cluster, and API Gateway will be deployed.

3. **Testing:**

    **Generate Token**
   
  - Copy the TokenCreationAPIURL from the CloudFormation stack outputs.
  - Use Postman or curl to call the API:
    ```bash
        curl -X POST -H "Content-Type: application/json" \
        -d '{"user_id": "user123", "phone_number": "+1234567890"}' \
        <TokenCreationAPIURL>  
  - The API will return the token in the response and send it to the user's phone number via SNS.
  
     **Validate Token:** 
   
  - Copy the TokenValidationAPIURL from the CloudFormation stack outputs.
   - Use Postman or curl to validate the token:
   ```bash
        curl -X POST -H "Content-Type: application/json" \
        -d '{"token": "<token_received_via_sms>"}' \
        <TokenValidationAPIURL>
       - The API will verify the token and return the result (success or error).
 ```
**Important Note:**
- AWS Credentials: Ensure your local machine is configured with the necessary AWS credentials.
- SNS Configuration: Verify that the phone numbers receiving the messages are confirmed in Amazon SNS.
- Replace placeholders such as `your-dockerhub-username`, `TokenCreationAPIURL`, and `TokenValidationAPIURL` with your actual values.
- To verify token we can call `tokenVerfication` api by copying its link from the outputs with key as `TokenVerificationAPIURL` and provide a verification code in the body as `{"verification_code": "code"}`
- This verify the token or gave error based on the token value.
