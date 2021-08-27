from django.contrib import admin
from .models import UserClient, UserProfile


admin.site.register(UserClient)
admin.site.register(UserProfile)