from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('beta-test/', views.client_form, name='client_form'),
    path('confirmation/', views.client_form_confirmation, name='client_confirmation'),
    path('incoming', views.incoming, name='incoming'),
]
