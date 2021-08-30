from django.contrib.auth.models import User
from django.db import models



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
