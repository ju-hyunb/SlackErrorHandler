import os
import inspect

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



def raiseerror():

	try:
		print(message)

	except Exception as e:
		ExceptionHandler(e)
		




if __name__ == "__main__":
	
	slack_error_handler = SetSlack()
	raiseerror()

	
	


