import json
import boto3

session = boto3.Session()

#create a Bedrock client
bedrock = session.client(service_name='bedrock-runtime') 

#set the foundation model

bedrock_model_id = "ai21.j2-ultra-v1" 

prompt = "What is the largest city in New Hampshire?" #the prompt to send to the model

#build the request payload
body = json.dumps({
    "prompt": prompt, #AI21
    "maxTokens": 1024, 
    "temperature": 0, 
    "topP": 0.5, 
    "stopSequences": [], 
    "countPenalty": {"scale": 0 }, 
    "presencePenalty": {"scale": 0 }, 
    "frequencyPenalty": {"scale": 0 }
}) 

# send the payload to Bedrock
# use Bedrock's invoke_model function to make the call.
response = bedrock.invoke_model(body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json') 

response_body = json.loads(response.get('body').read()) # read the response

response_text = response_body.get("completions")[0].get("data").get("text") #extract the text from the JSON response

print(response_text)