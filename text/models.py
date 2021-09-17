from django.contrib.auth.models import User
from django.db import models
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_url = models.CharField(max_length=200)
    user_phone_limit = models.IntegerField(default=1)
    user_phone = models.CharField(max_length=14, blank=True)
    message_frequency = models.IntegerField(default=1)
    message_count = models.IntegerField(default=0)
    message_limit = models.IntegerField(default=1000)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class UserClient(models.Model):
    client_of = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=254)
    is_active = models.BooleanField(default=True)
    signed_up = models.DateField(blank=True, default=date.today)
    last_message_received = models.DateField(blank=True, null=True)
    last_message_reply = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = [['phone', 'client_of'],]

    def __str__(self):
        return self.phone


class Registration(models.Model):
    invite_required = models.BooleanField(default=True)

    def __str__(self):
        return f'Invite Code Required: {self.invite_required}'


class RegistrationInviteCode(models.Model):
    invite_code = models.CharField(max_length=12, unique=True)
    is_used = models.BooleanField(default=False)
    redeemed_by = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Registration Invite Codes'

    def __str__(self):
        return self.invite_code
