# SlackErrorHandler
Error Handling Using Slack

### 1. set config file
To be managed Slack bots information (name, token)

_slack.config.json_
```
{
    "bots": [{"bot_name": "LogBot",
				"bot_token" : "your-slack-token1"},

				{"bot_name": "VoteBot",
				"bot_token" : "your-slack-token2"},

				{"bot_name": "AlarmBot",
				"bot_token" : "your-slack-token3"}
			]
}
```

---
### 2. Python File to handle error

```
from SendMessageSlack import SlackAlertError

def SetSlack():
	bot_name = "LogBot"
	channel_name = "#test"
	title = "[Project Name] test"
	file_name = os.path.basename(__file__)

	slack_error_handler = SlackAlertError(bot_name, channel_name, title, file_name)

	return slack_error_handler


def ExceptionHandler(e):
	call_function_name = inspect.stack()[1].function
	exception_type = type(e).__name__

	slack_error_handler.send_message(call_function_name, exception_type)
```
send error message to slack

```
def raiseerror():

	try:
		print(message)

	except Exception as e:
		ExceptionHandler(e)

```
---
### 3. Example

![스크린샷 2024-06-07 170447](https://github.com/ju-hyunb/SlackErrorHandler/assets/104177526/ed6cf4d1-2c23-417c-a956-5880b2f811a4)


