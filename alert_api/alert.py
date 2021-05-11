from twilio.rest import Client
from constants import account_sid, auth_token, FROM_NO, TO_NO

def alert_user(msg):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"{msg}",
        from_=FROM_NO,
        to=TO_NO
    )
    print(message.status)
    return message.status
