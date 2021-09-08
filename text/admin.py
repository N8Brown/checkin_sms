from django.contrib import admin
from .models import Registration, RegistrationInviteCode, UserClient, UserProfile


admin.site.register(Registration)
admin.site.register(RegistrationInviteCode)
admin.site.register(UserClient)
admin.site.register(UserProfile)