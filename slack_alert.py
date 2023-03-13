from flask import Flask, request
from flask_caching import Cache
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv()


config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 86400  #24 hours
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

@app.route("/", methods=['POST'])
def slack_alert():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json_payload = request.json

        if json_payload.get('Type') == 'SpamNotification':
            email = json_payload.get('Email')
            slack_token = os.environ['SLACK_BOT_TOKEN']
            client = WebClient(token=slack_token)
            alert_text = f":warning: Spam Alert for {email}!"
            channel_id = os.environ['CHANNEL_ID'] 
            try:
                if not cache.get(email):
                    response = client.chat_postMessage(
                        channel=channel_id,
                        text=alert_text
                    )
                    cache.set(email,response.data['ts'])
    
                else:
                    ts = cache.get(email)
                    response = client.chat_postMessage(
                        channel=channel_id,
                        thread_ts=ts,
                        text=alert_text)

                return "Spam Alert Sent!" 

            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                # assert e.response["error"]
                return e.response["error"]

            return "Not Spam"
    else:
        return "Content-Type should be application/json"                       
    

   


