from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Phone
from twilio.rest import Client
import os


def auto_text():    
    phone_list = Phone.objects.filter(is_active=True)

    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    for entry in phone_list:
        message = client.messages \
                        .create(
                            body="This is a daily check-in test",
                            from_=os.environ.get('TWILIO_FROM'),
                            to=entry.phone
                        )

        print(message.sid)
    
    return HttpResponse('<Response></Response>')

