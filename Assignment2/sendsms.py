from twilio.rest import Client
from dotenv import dotenv_values

config = dotenv_values(".env")

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = config["ACCOUNT_SID"]
auth_token = config["AUTH_TOKEN"]
client = Client(account_sid, auth_token)

def send_twilio_alert():

	message = client.messages.create(
  	body="Hello your fridge door is open. See latest image here - http://fridgedoor.glitch.me/ ",
  	from_=config["FROM"],
  	to=config["TO"]
	)

	print(message.sid)
