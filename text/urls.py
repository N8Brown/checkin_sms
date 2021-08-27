from django.contrib.auth.models import User
from django.urls import path
from os import name
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/', views.user_edit_user, name='user_edit_user'),
    path('phone/', views.user_add_phone, name='user_add_phone'),
    path('<username>/signup/', views.client_form, name='client_form'),
    path('confirmation/', views.client_form_confirmation, name='client_confirmation'),
    path('incoming', views.incoming, name='incoming'),
]

# users = User.objects.all()

# for user in users:
#     urlpatterns.append(path(f'{user.username}/dashboard/', views.user_dashboard, name='user_dashboard'))

