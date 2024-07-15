markdown
# Download and configure the assets for the labs

1. In the AWS Cloud9 IDE, select the *bash terminal*.

![Bash Terminal](/Images/Lab_setup_image1.png)

2. Paste and run the following into the terminal to download and unzip the code.
    ```bash
    cd ~/environment/
    curl 'https://static.us-east-1.prod.workshops.aws/public/f386b794-934e-41f1-999f-750d1bb98bd0/assets/workshop.zip' 
    unzip workshop.zip
    ```
    
Once completed, you should see the unzip results in the terminal.

![Unzip Result](/Images/Lab_setup_image2.png)

3. Install the dependencies for the labs.
   
```bash
    pip3 install -r ~/environment/workshop/setup/requirements.txt -U
```

   If everything worked properly, you should see a success message (you can disregard a warning like below).

![Success Message](/Images/Lab_setup_image3.png)


4. Verify configuration by pasting and running the following into the AWS Cloud9 terminal:
   
```bash
    cd ~/environment/
    python ~/environment/workshop/completed/api/bedrock_api.py
```    
If everything is working properly, you should see a response about Manchester, New Hampshire.

![Final Result](/Images/Lab_setup_image4.png)
