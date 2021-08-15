from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django_twilio.decorators import twilio_view
from functools import wraps
from twilio import twiml
from twilio.request_validator import RequestValidator
from .forms import ClientForm
from .models import Client

import os


def home(request):
    context = {}
    return render(request, 'text/checkinsms.html', context)


def user_register(request):
    context = {}
    return render(request, 'text/register.html', context)


def user_login(request):
    
    if request.method == "POST":
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user_dashboard', user.username.lower())
        else:
            messages.warning(request, ('Username or password is incorrect. Please try again.'))
            return redirect('user_login')

    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            context = {}            
            return render(request, 'text/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def user_dashboard(request, username):
    current_user = request.user
    if current_user.username == username:
        context = {}
        return render(request, 'text/dashboard.html', context)
    else:
        return redirect('user_login')


def client_form(request):
    if request.method == 'POST':
        print(request.POST)
        form = ClientForm(request.POST or None)
        if form.is_valid():
            form.save()
            phone_list = Client.objects.filter(is_active=True)
            context = {
                'phone_list':phone_list,
            }

            return redirect('client_confirmation')
        else:
            context = {
                'form':form,
            }
            return render(request.lower(), 'text/client_form.html', context)
    else:
        context = {}
        return render(request.lower(), 'text/client_form.html', context)
    


def client_form_confirmation(request):
    context = {}
    return render(request, 'text/client_confirmation.html', context)



def validate_twilio_request(func):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(func)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorated_function




# def checkin(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = PhoneForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             messages.success(request, ('Your phone number has been successfully added to the list!'))

#             phone_list = Phone.objects.filter(is_active=True)
#             context = {
#                 'phone_list':phone_list,
#             }

#             return redirect(checkin)
#         else:
#             phone_list = Phone.objects.filter(is_active=True)
#             context = {
#                 'form':form,
#                 'phone_list':phone_list,
#             }
#             return render(request, 'text/checkin.html', context)

#     else:
#         phone_list = Phone.objects.filter(is_active=True)
#         context = {
#             'phone_list':phone_list,
#         }
#         return render(request, 'text/checkin.html', context)



@twilio_view
# @validate_twilio_request
def incoming(request):

    print(request.POST)
    user_reply = request.POST.get('Body')
    user_phone = request.POST.get('From')

    user = Phone.objects.filter(phone=user_phone)

    if user:
        if user_reply.lower() == 'y' or user_reply.lower() == 'yes':
            send_mail(
                f'Daily Check-in Response From {user[0].first_name.title()} {user[0].last_name.title()}',
                f'{user[0].first_name.title()} {user[0].last_name.title()} is still actively looking for a job.',
                None,
                ['nathan.a.brown@outlook.com',],
                fail_silently=False, 
            )
        elif user_reply.lower() == 'n' or user_reply.lower() == 'no':
            user[0].is_active = False
            user[0].save()
            print(user[0].is_active)

    return HttpResponse('<Response></Response>')