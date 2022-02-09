from  twilio.rest import  Client
from django.conf import settings


def send_sms(phone):
    account = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account, auth_token)
    client.messages.create(
        body='your account has been verified',
        from_=settings.PHONE_NUMBER,
        to=phone
    )