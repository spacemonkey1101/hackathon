from typing import Collection, Text
import slack
import os
import pathlib

from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter


env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_TOKEN'],'/event', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
bot_id = client.api_call("auth.test")['user_id']


'''@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    if event.get('user') != bot_id:
        channel =  event.get('channel')
        print(event)
        client.chat_postMessage(channel=channel, text='Hello Friend')'''

@slack_event_adapter.on('app_mention')
def app_mentions(payload):
    event = payload.get('event', {})
    user = event.get('user')
    if event.get('user') != bot_id:
        channel =  event.get('channel')
        
        
        client.chat_postMessage(channel=channel, text=f'Hello @{user} ')

if __name__ == "__main__":
    app.run(debug=True,port=3000)