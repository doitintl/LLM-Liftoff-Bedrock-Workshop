# Lab F-2: InvokeModel API

If running from your own account, please complete the Prerequisites section before starting this lab.

Lab introduction

## Final product:

![Final Result](/Images/Lab2_Image1.png)

In this lab, we will show how to make a basic API call directly to Bedrock.
You can build the application code by copying the code snippets below and pasting into the indicated Python file.

## Create the Python script

1. Navigate to the workshop/labs/api folder, and create a new file `bedrock_api.py` if it's not there. If it is already created for you then go to step 7

2. Add the import statements.
    - These statements allow us to use the AWS Boto3 library to call Amazon Bedrock.
    - You can use the copy button in the box below to automatically copy its code:
    ```python
    import json
    import boto3
    ```
    
3. Initialize the Bedrock client library.
   - This creates a Bedrock client.
   ```python
   session = boto3.Session()
   bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
   ```
4. Build the payload for the API call.
   - Here we are identifying the model to use, the prompt, and the inference parameters for the specified model.
   ```python
   bedrock_model_id = "ai21.j2-ultra-v1" #set the foundation model
   prompt = "What is the largest city in New Hampshire?" #the prompt to send to the model
   body = json.dumps({
       "prompt": prompt, #AI21
       "maxTokens": 1024,
       "temperature": 0,
       "topP": 0.5,
       "stopSequences": [],
       "countPenalty": {"scale": 0 },
       "presencePenalty": {"scale": 0 },
       "frequencyPenalty": {"scale": 0 }
   }) #build the request payload
   ```
5. Call the Bedrock API.
   - We use Bedrock’s invoke_model function to make the call.
   
```python
   response = bedrock.invoke_model(body=body, modelId=bedrock_model_id, 
   accept='application/json', contentType='application/json') #send the payload to Bedrock
```

6. Display the response.
   - This extracts & prints the returned text from the model’s response JSON.
   ```python
      response_body = json.loads(response.get('body').read()) # read the response
      response_text = response_body.get("completions")[0].get("data").get("text") 
      
      #extract the text from the JSON response
      print(response_text)
   ```
7. Save the file.
Great! Now you are ready to run the script!

## Run the script

1. Select the bash terminal in AWS Cloud9 and change directory.
   
```bash
    cd ~/environment/workshop/labs/api
```    
    
2. Run the script from the terminal.
   
```bash
    python bedrock_api.py
```    
    
3. The results should be displayed in the terminal.

![Final Result](/Images/Lab2_Image2.png)



