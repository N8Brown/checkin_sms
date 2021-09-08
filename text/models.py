from django.contrib.auth.models import User
from django.db import models

import secrets, random



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_url = models.CharField(max_length=200)
    user_phone_limit = models.IntegerField(default=1)
    user_phone = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return self.user.username


class UserClient(models.Model):
    client_of = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=254)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [['phone', 'client_of'],]

    def __str__(self):
        return self.phone


class Registration(models.Model):
    invite_required = models.BooleanField(default=True)


def invite_code_generator(size=12, chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'):
        return ''.join(random.choice(chars) for _ in range(size))


class RegistrationInviteCode(models.Model):
    invite_code = models.CharField(max_length=12, unique=True, default=invite_code_generator())

    # def __init__(self):
    #     super(RegistrationInviteCode, self).__init__()
    #     self.invite_code = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(12))

    def __str__(self):
        return self.invite_code

    