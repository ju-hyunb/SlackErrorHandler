import os
import sys
import json
import datetime
import socket
import logging

import inspect
import traceback

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SlackAlertError():
	
	def __init__(self, bot_name: str, channel_name: str, title: str, file_name:str):
		self.SLACK_BOT_NAME=bot_name
		self.SLACK_CHANNEL=channel_name
		self.SLACK_API_TOKEN=self.get_bot_token()
		self.slack_client = WebClient(token=self.SLACK_API_TOKEN)

		self.TITLE = title
		self.FILE_NAME = file_name


	def get_bot_token(self) -> str:

		try:
			with open("slack.config.json", 'r') as f:
				bot_config_file = json.load(f)

				for bot in bot_config_file.get('bots', []):
					if bot['bot_name'] == self.SLACK_BOT_NAME:
						return bot['bot_token']

			raise ValueError(f"Bot name {self.SLACK_BOT_NAME} not found in the configuration file")
		except Exception as e:
			logging.error(f"Failed to get bot token: {e}")
			raise


	def create_slack_format(self, function_name, error_name) -> list:

		nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		hostname_and_ip = f"{socket.gethostname()} - {socket.gethostbyname(socket.gethostname())}"

		formatted_msg = f"*[Now Datetime]* _{nowtime}_\n*[Server and IP]* _{hostname_and_ip}_\n*[Function Name]* `{function_name}`\n*[Error Name]*: `{error_name}`"
		stack_trace = traceback.format_exc()

		max_trace_length = 2500
		if len(stack_trace) > max_trace_length:
			stack_trace = stack_trace[:max_trace_length] + "\n... (stack trace truncated)"


		blocks = [
					{
						"type": "header",
						"text": {
							"type": "plain_text",
							"text": f":warning:  {self.TITLE}  :warning:"
						}
					},
					{
						"type": "divider"
					},
					{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": f"`/{self.FILE_NAME}`"
						}
					},
					{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": f"{formatted_msg}"
                    	}
                	},
					{
						"type": "section",
						"text": {
							"type": "mrkdwn",
							"text": f"*Stack Trace:*\n```{stack_trace}```"
                    	}
                	}
				]

		return blocks


	def send_message(self, function_name, error_msg):
		try:
			blocks = self.create_slack_format(function_name, error_msg)
			response = self.slack_client.chat_postMessage(
				channel=self.SLACK_CHANNEL,
				blocks=blocks,
				text="none")
				
			logging.info(f"Message sent: {response['message']['text']}")
			
		except SlackApiError as e:
			logging.error(f"Failed to send message to Slack: {e.response['error']}")
			
		except Exception as e:
			logging.error(f"An unexpected error occurred: {e}")

