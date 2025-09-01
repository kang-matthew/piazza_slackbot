"""
Ze Xuan Ong
15 Jan 2019

Adapted from t-davidson's piazza-slackbot
URL: https://github.com/t-davidson/piazza-slackbot/blob/master/slackbot.py

This is a simple Slackbot that will poll Piazza every minute

Every time a new post is observed a notification will be sent out
"""

import os
import re
import logging

from piazza_api import Piazza
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_sdk.web import WebClient
from time import sleep
from dotenv import load_dotenv, find_dotenv

from piazza_post import PiazzaPost


# Config object to collect all required environment and config vars
class Config():

    # Environment variables
    PIAZZA_ID = ""          # Piazza forum id
    PIAZZA_EMAIL = ""       # User account email
    PIAZZA_PASSWORD = ""    # User account password
    SLACK_TOKEN = ""        # Slack API token
    SLACK_CHANNEL = ""      # Slack channel name
    SLACK_BOT_NAME = ""     # Slack bot name

   
    

    def __init__(self, pid, pemail, ppass, stoken, schannel, sbot):
        self.PIAZZA_ID = pid
        self.PIAZZA_EMAIL = pemail
        self.PIAZZA_PASSWORD = ppass
        self.SLACK_TOKEN = stoken
        self.SLACK_CHANNEL = schannel
        self.SLACK_BOT_NAME = sbot        


# Main method
def main():

    # Read all relevant config variables
    conf = config_env()

    # Setup Piazza
    piazza = Piazza()
    piazza.user_login(email=conf.PIAZZA_EMAIL, password=conf.PIAZZA_PASSWORD)
    network = piazza.network(conf.PIAZZA_ID)

    # Setup Slack
    client = WebClient(token=conf.SLACK_TOKEN)
    #bot = Slacker(conf.SLACK_TOKEN)

    # Get the last posted_id
    #last_id = get_max_id(network.get_feed()['feed'])
    last_id = 424
    
    # Run loop
    check_for_new_posts(network, client, conf, last_id)


# Collect env vars
def config_env():

    # Get environment variables from .env file if exists
    load_dotenv(find_dotenv())

    # Piazza specific
    PIAZZA_ID = os.getenv("PIAZZA_ID")
    PIAZZA_EMAIL = os.getenv("PIAZZA_EMAIL")
    PIAZZA_PASSWORD = os.getenv("PIAZZA_PASSWORD")

    if not PIAZZA_ID or not PIAZZA_EMAIL or not PIAZZA_PASSWORD:
        print("Missing Piazza credentials")
        exit(1)

    # Slack specific
    SLACK_TOKEN = os.getenv("SLACK_TOKEN")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
    SLACK_BOT_NAME = os.getenv("SLACK_BOT_NAME")

    if not SLACK_TOKEN or not SLACK_CHANNEL or not SLACK_BOT_NAME:
        print("Missing Slack credentials")
        exit(1)

    return Config(PIAZZA_ID, PIAZZA_EMAIL, PIAZZA_PASSWORD,
                  SLACK_TOKEN, SLACK_CHANNEL, SLACK_BOT_NAME)


def get_max_id(feed):
    max_id = -1
    for post in feed:
        if ("note" not in post["type"] and
            "Pinned" not in post["bucket_name"] and
            "must-reads" not in post["bucket_name"]):
            max_id = max(max_id, post["nr"])
    return max_id


# Method that polls Piazza in constant interval and posts new posts
# to Slack
def check_for_new_posts(network, client, config, last_id, interval=60):
    LAST_ID = last_id

    # Keep looping
    while True:
        try:
            UPDATED_LAST_ID = get_max_id(network.get_feed()['feed'])
            print(f"UPDATED_LAST_ID: {UPDATED_LAST_ID}")

            # For all the new posts
            while UPDATED_LAST_ID > LAST_ID:

                LAST_ID += 1

                # Fetch post
                print(f"fetching post ID: {LAST_ID}")
                post = network.get_post(LAST_ID)
                
                if not post.get('type', '') == 'question':
                    continue
                
                subject = post['history'][0]['subject']

                # Create post message
                start_post(subject, LAST_ID, client, config)
                    
            print("Slack bot is up!")
            sleep(interval)
        except Exception as e:
            print(f"Error when attempting to get Piazza and post: {e}")
            sleep(interval)


def start_post(subject, post_id, client, config):
    # Create a new piazza post
    piazza_post = PiazzaPost(subject, post_id, config)
    
    # Get the message payload
    message = piazza_post.get_message_payload()
    
    # Post the onboarding message in Slack
    response = client.chat_postMessage(**message)

    return piazza_post
    
            
# Main
if __name__ == '__main__':
    main()

