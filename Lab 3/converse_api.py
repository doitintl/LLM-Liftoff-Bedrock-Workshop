import boto3, json

session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

message_list = []

while True:
    inp = input("User: ")

    if inp == "exit":
        break

    initial_message = {
        "role": "user",
        "content": [
            { "text": inp } 
        ],
    }

    message_list.append(initial_message)

    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=message_list,
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0
        },
    )

    response_message = response['output']['message']
    # print(json.dumps(response_message, indent=4))

    message_list.append(response_message)

    response_message = response['output']['message']['content'][0]['text']

    print("System", response_message)
