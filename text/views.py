from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django_twilio.decorators import twilio_view
from functools import wraps
# from twilio import twiml
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from .forms import UserClientForm, UserRegistrationForm, UserEditUserForm
from .models import UserClient, UserProfile

import os


def home(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return redirect('user_dashboard')
        else:
            return redirect('admin/')
    else:
        context = {}
        return render(request, 'text/checkinsms.html', context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            user_url = f'https://checkinsms.com/{username.lower()}/signup'
            profile = UserProfile(user=user, user_url=user_url)
            profile.save()

            return redirect('user_dashboard', username.lower())
        else:
            messages.warning(request, ('There is an error...'))
            context = {
                'form': form,
            }
            return render(request, 'text/register.html', context)
    else:
        form = UserRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'text/register.html', context)


def user_login(request):
    
    if request.method == "POST":
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.warning(request, ('Username or password is incorrect. Please try again.'))
            return redirect('user_login')

    else:
        if request.user.is_authenticated:
            return redirect('user_dashboard')
        else:
            context = {}            
            return render(request, 'text/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def user_dashboard(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            user = User.objects.get(username=request.user.username)
            user_profile = UserProfile.objects.get(user=request.user)
            client_list = UserClient.objects.filter(client_of=request.user.username)

            context = {
                'user':user,
                'user_profile':user_profile,
                'client_list':client_list,
            }
            return render(request, 'text/dashboard.html', context)
        else:
            return redirect('home')

    else:
        return redirect('user_login')


@login_required
def user_edit_user(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            if request.method == 'POST':
                form = UserEditUserForm(request.POST, instance=request.user,)
                form.save()
                return redirect('user_dashboard')
            else:
                form = UserEditUserForm(instance=request.user)
                context = {
                    'form':form,
                }
                return render(request, 'text/edit_user.html', context)

        else:
            return redirect('home')

    else:
        return redirect('user_login')


@login_required
def user_add_phone(request):
    if request.user.is_authenticated:

        if not request.user.is_staff:
            if request.method == 'POST':
                account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
                auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
                client = Client(account_sid, auth_token)
                local = client.available_phone_numbers('US').local.list(area_code=int(request.POST['area_code']), limit=10)

                available_numbers = [record.friendly_name for record in local]
                # for record in local:
                #     print(record.friendly_name)
                context = {
                    'available_numbers':available_numbers,
                }

                return render(request, 'text/add_phone.html', context)
            else:
                context = {}
                return render(request, 'text/add_phone.html', context)
        else:
            return redirect('home')
    else:
        return redirect('user_login')




def client_form(request, username):
    if request.method == 'POST':
        print(request.POST)
        form = UserClientForm(request.POST or None)
        if form.is_valid():
            form.save()
            phone_list = UserClient.objects.filter(is_active=True)
            context = {
                'phone_list':phone_list,
            }

            return redirect('client_confirmation')
        else:
            context = {
                'username':username,
                'form':form,
            }
            return render(request, 'text/client_form.html', context)
    else:
        if User.objects.filter(username=username, is_staff=False):
            form = UserClientForm()
            context = {
                'username':username,
                'form':form,
            }
            return render(request, 'text/client_form.html', context)
        else:
            return redirect('home')
    


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







@twilio_view
# @validate_twilio_request
def incoming(request):

    print(request.POST)
    user_reply = request.POST.get('Body')
    user_phone = request.POST.get('From')

    user = Client.objects.filter(phone=user_phone)

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