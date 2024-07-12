# Getting started with the Amazon Bedrock Converse API


Learn the basics of using the Amazon Bedrock Converse API with large language models on Amazon Bedrock.The Amazon Bedrock Converse API provides a consistent way to access large language models (LLMs) using Amazon Bedrock. It supports turn-based messages between the user and the generative AI model. It also provides a consistent format for tool definitions for the models that support tool use (aka “function calling”).Why is the Converse API so important? Previously, with the InvokeModel API, you needed to use different JSON request and response structures for each model provider. The Converse API allows us to use a single format for requests and responses across all large language models on Amazon Bedrock.Note that as of this article’s writing, the Converse API only supports text generation models.

1.  Add the import statements.
    * These statements allow us to use the AWS Boto3 library to call Amazon Bedrock.

          import boto3, json
          
2. Initialize the Bedrock client library.
    * This creates a Bedrock client.

          session = boto3.Session()

          bedrock = session.client(service_name='bedrock-runtime')

3. Create Initial message.
    * Here we create a list called message_list
    * Create initial_message and add it to the message_list

          message_list = []

          initial_message = {
              "role": "user",
              "content": [
                  { "text": "How are you today?" } 
              ],
          }

          message_list.append(initial_message)

4. Here we are identifying the model to use, the prompt, and the inference parameters for the specified model.
    * We use Bedrock’s invoke_model function to make the call.

          response = bedrock.converse(
              modelId="anthropic.claude-3-sonnet-20240229-v1:0",
              messages=message_list,
              inferenceConfig={
                  "maxTokens": 2000,
                  "temperature": 0
              },
          )

5. Here we create a JSON dump as the response from the model

          response_message = response['output']['message']
          print(json.dumps(response_message, indent=4))

6. Save the file (converse_api.py) & run the Script
    * Select the bash terminal in AWS Cloud9 and change directory.

          cd ~/environment/workshop/labs/api
 
    * Run the script from the terminal

          python converse_api.py

    * The results should be displayed in the terminal.
          
          {
              "role": "assistant",
              "content": [
                  {
                      "text": "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, harmless, and honest."
                  }
              ]
          }

    * If you want to get the list of conversation, simply do the following

          # comment out the previous print statement
          # print(json.dumps(response_message, indent=4))

          message_list.append(response_message)

          print(json.dumps(message_list, indent=4))

    * Save the file.
    * Run the script from the terminal.

          python converse_api.py

    * Now you will see the whole message chain like this

          [
              {
                  "role": "user",
                  "content": [
                      {
                          "text": "How are you today?"
                      }
                  ]
              },
              {
                  "role": "assistant",
                  "content": [
                      {
                          "text": "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, harmless, and honest."
                      }
                  ]
              }
          ]

* Reference Document: Getting started with the Amazon Bedrock Converse API
