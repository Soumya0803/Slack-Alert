from flask import Flask, request
import os
from slack_sdk.webhook import WebhookClient
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/", methods=['POST'])
def slack_alert():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json_payload = request.json

        if json_payload.get('Type') == 'SpamNotification':
            email = json_payload.get('Email')
            url = os.getenv('SLACK_WEBHOOK_URL')
            webhook = WebhookClient(url)
            alert_text = f":warning: Spam Alert for {email}!"
            response = webhook.send(text=alert_text)
            assert response.status_code == 200  
            assert response.body == "ok"
            return "Spam Alert Sent!"
           
        return "Not Spam"
    else:
        return "Content-Type should be application/json"                       
    

        

