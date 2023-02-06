# AWS Docusign Lambda Function

## **Local Setup:**
---

### **Requirements:**
    - aws cli
    - sam cli
#TODO 

## **VSCode Devcontainer Setup:**
---

### **Requirements:**
    - VSCode
    - Docker
    - VSCode Devcontainer

### **Setup:**

    1. In vscode click `File` and then click `Open Folder...`
    2. Open the `backend` folder
    3. Click `Ctrl + Shift + P` and then select `Dev Containers: Rebuild and Reopen in Container`

### **Making an AWS SSO Account**:
    This is a one time step for aws sso accounts. If you already did this step inside or outside of the container, you don't need to do this step.
    1. Make sure you are in the devcontainer
    2. Run the command `aws configure sso`
    3. Set the SSO session name to cpac-webmaster
    4. Set the SSO start URL to `https://castlepointanime.awsapps.com/start`
    5. Set the SSO region to `us-east-1`
    6. Set the SSO registration scopes to `account`
    7. Set the CLI default client region to `us-east-1`
    8. Set the CLI default output format to `json`
    9. Set the CLI profile name to `cpac-webmaster`

### **Connect to AWS SSO:**
    1. Click `Ctrl + Shift + P` and then select `AWS: Connect to AWS`
    2. Select `profile:cpac-webmaster`
    3. Wait a few seconds. On the bottom, `AWS: profile:cpac-webmaster` should appear and should not be red.
    
### **How to Push Code to AWS Lambda:**
    1. Make sure the `credentials.json` is in the `docusignLambda` folder. Ask the CPAC webmaster leader for this file or see this link to generate one: https://developers.google.com/drive/api/quickstart/go
    2. In the `lambdaFunctions` folder, run the script `./package.sh docusignLambda`. The script should say `Done!` at the end.
    3. Click `Ctrl + Shift + P` and then select `AWS: Upload Lambda...`
    4. Select region to 'us-east-1'
    5. Select 'ZIP Archive'
    6. Go to the directory 'backend/lambdaFunctions/docusignLambda/deployment.zip'
    7. Ente rthe lambda function name `docusignLambda`
    8. Wait a few seconds and on the bottom right, VSCode should say that the push was successful