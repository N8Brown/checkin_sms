from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from text.models import Phone as Email

class Command(BaseCommand):
    help = 'A task to retrieve all active users from the database and send and email to each one'

    def handle(self, *args, **kwargs):
        email_list = Email.objects.filter(is_active=True)

        if email_list:
            for user in email_list:
                send_mail(
                    f'Daily Check-in Response From {user.first_name.title()} {user.last_name.title()}',
                    f'{user.first_name.title()} {user.last_name.title()} is still actively looking for a job.',
                    None,
                    ['nathan.a.brown@outlook.com',],
                    fail_silently=False, 
                )