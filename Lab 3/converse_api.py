import boto3, json

# Establish a session with AWS services (assumes credentials are configured)
session = boto3.Session()

# Create a client for the Bedrock Runtime service, which is used for interacting with models
bedrock = session.client(service_name='bedrock-runtime')

# Initialize an empty list to store conversation messages
message_list = []

# Start an interactive loop
while True:
    # Get user input
    inp = input("User: ")

    # Check for exit condition
    if inp == "exit":
        break

    # Structure the user's message into the format required by the model
    initial_message = {
        "role": "user", 
        "content": [
            { "text": inp }  # Embed the input text within a "text" object
        ],
    }

    # Add the user's message to the conversation history
    message_list.append(initial_message)

    # Call the Bedrock Runtime API to get a response from the model
    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0", # Specify the model to use (Claude)
        messages=message_list,   # Pass the conversation history
        inferenceConfig={         # Configure model parameters
            "maxTokens": 2000,      # Maximum tokens in the response
            "temperature": 0       # Controls randomness (0 = deterministic)
        },
    )

    # Extract the model's response message from the API response
    response_message = response['output']['message']
    # print(json.dumps(response_message, indent=4))  # Optionally print raw response for debugging

    # Add the model's response to the conversation history
    message_list.append(response_message)

    # Extract the actual text content of the model's response
    response_message = response['output']['message']['content'][0]['text']

<<<<<<< HEAD
    # Print the model's response
    print("System", response_message) 
=======
    print("System", response_message)
>>>>>>> 25b1ea29b7b798393667d22108628a342632399b
