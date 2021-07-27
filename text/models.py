from django.db import models

class Phone(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14, unique=True)
    email = models.CharField(max_length=254)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.phone
