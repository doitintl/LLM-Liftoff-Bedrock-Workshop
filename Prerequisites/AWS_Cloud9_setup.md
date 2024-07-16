markdown
# AWS Cloud9 setup

We will be using AWS Cloud9 as our integrated development environment for this workshop. AWS Cloud9 is one option for building applications with Amazon Bedrock.

Below we will configure an AWS Cloud9 environment in order to build and run generative AI applications. An environment is a web-based integrated development environment for editing code and running terminal commands.

## Assumptions for the following instructions

- AWS Cloud9 will be run from the same account and region where Bedrock foundation models have been enabled.
- The account and region have a default VPC configured (this is the AWS default).

If you have any challenges below, you may need to access Bedrock from your desktop environment, or create an alternate configuration.

## AWS Cloud9 setup instructions

1. In the AWS console, select the region that has Amazon Bedrock foundation models enabled.

![Region Select](/Images/Cloud9_setup_image1.png)


2. In the AWS console, search for Cloud9.
   - Select Cloud9 from the search results.

![Cloud9](/Images/Cloud9_setup_image2.png)

3. Select Create environment.

![Create Environment](/Images/Cloud9_setup_image3.png)

4. Set the environment details.
   - Set Name to `bedrock-environment`.

   ![Set Environment](/Images/Cloud9_setup_image4.png)

5. Set the EC2 instance details.
   - Set Instance type to `t3.small`
   - Set Platform to `Ubuntu Server 22.04 LTS`
   - Set Timeout to `4 hours`

![Select EC2](/Images/Cloud9_setup_image5.png)

*Did you select Ubuntu as your platform?*

Please double-check that you set Platform to `Ubuntu Server 22.04 LTS`. This ensures that you will have a Python version that can support LangChain and other critical libraries.

6. Select the Create button.

![Create EC2](/Images/Cloud9_setup_image6.png)

7. Wait for the environment to be created.
   - You should get a "Successfully created bedrock-environment" message in the top banner when ready.
   - In the Environments list, click the Open link. This will launch the AWS Cloud9 IDE in a new tab.

![Create Env](/Images/Cloud9_setup_image7.png)

*Handling environment creation errors*

- If you get an error message about the selected instance type not being available in the availability zone, delete the environment. Try provisioning again with a different size instance type.

8. Confirm that the AWS Cloud9 environment is loaded properly.
   - You can close the Welcome tab
   - You can drag tabs around to the position you want them in.

![Confirm](/Images/Cloud9_setup_image8.png)   

