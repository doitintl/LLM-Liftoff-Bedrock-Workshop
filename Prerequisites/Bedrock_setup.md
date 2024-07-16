# Amazon Bedrock Setup
In this workshop, we will be using Amazon Bedrock to access foundation models. 
Below, we will configure model access in Amazon Bedrock in order to build and run generative AI applications.
Amazon Bedrock provides a variety of foundation models from several providers.

## Steps
1. Find Amazon Bedrock by searching in the AWS console.
![Find Bedrock](/Images/Bedrock_setup_image1.png)

2. Expand the side menu.
![Expand Menu](/Images/Bedrock_setup_image2.png)

3. From the side menu, select Model access.
![Select Model](/Images/Bedrock_setup_image3.png)

4. Select the Enable specific models button.
![Enable Model](/Images/Bedrock_setup_image4.png)

5. Select the checkboxes listed below to activate the models. If running from your own account, there is no cost to activate the models - you only pay for what you use during the labs.
Review the applicable EULAs as needed.
   - Amazon (select Amazon to automatically select all Amazon Titan models)
   - Anthropic > Claude 3 Sonnet
   - Cohere > Command
   - Meta > Llama 3 70B Instruct
   - Mistral AI > Mixtral 8x7B Instruct
![Activate Model](/Images/Bedrock_setup_image5.png)

6. On the Review and submit page, select the Submit button.
![Next](/Images/Bedrock_setup_image6.png)

7. Monitor the model access status. It may take a few minutes for the models to move from In Progress to Access granted status. You can use the Refresh button to periodically check for updates.
![Review](/Images/Bedrock_setup_image7.png)

8.Verify that the model access status is Access granted for the previously selected models.
![Monitor](/Images/Bedrock_setup_image8.png)

