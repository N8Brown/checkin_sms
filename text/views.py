from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django_twilio.decorators import twilio_view
from functools import wraps
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from .forms import UserAddPhoneForm, UserClientForm, UserEditMessageForm, UserEditUserForm, UserRegistrationForm 
from .models import Registration, RegistrationInviteCode, UserClient, UserProfile

import os

# Views that don't require authentication

def home(request):
    '''
    Check to see if the request is made by an authenticated user.

    Authenticated users with an "is_staff" status of True get redirected to the Django admin page.

    Authenticated users with an "is_staff" status of False get redirected to the user dashboard view.

    Unauthenticated users will able to view the home page. 
    '''
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
            user_url = f'https://checkinsms.com/{username.lower()}/signup'
            profile = UserProfile(user=user, user_url=user_url)
            profile.save()
            login(request, user)
            return redirect('user_dashboard')
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


def client_form(request, username):
    if request.method == 'POST':
        form = UserClientForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('client_confirmation')
        else:
            context = {
                'username':username,
                'form':form,
            }
            return render(request, 'text/client_form.html', context)
    else:
        if User.objects.filter(username=username, is_staff=False):
            user = User.objects.get(username=username)
            form = UserClientForm()
            context = {
                'user':user,
                'username':username,
                'form':form,
            }
            return render(request, 'text/client_form.html', context)
        else:
            return redirect('home')
    

def client_form_confirmation(request):
    context = {}
    return render(request, 'text/client_confirmation.html', context)


# Views that require authentication

@login_required
def user_dashboard(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            user = User.objects.get(username=request.user.username)
            user_profile = UserProfile.objects.get(user=request.user)
            print(bool(user_profile.user_phone))
            client_list = UserClient.objects.filter(client_of=request.user.id)
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
            return redirect('admin/')
    else:
        return redirect('user_login')


@login_required
def user_edit_message(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            if request.method == 'POST':
                user_profile = UserProfile.objects.get(user=request.user)
                form = UserEditMessageForm(request.POST, instance=user_profile,)
                form.save()
                return redirect('user_dashboard')
            else:
                user_profile = UserProfile.objects.get(user=request.user)
                form = UserEditMessageForm(instance=user_profile)
                context = {
                    'form':form,
                }
                return render(request, 'text/edit_message.html', context)
        else:
            return redirect('admin/')
    else:
        return redirect('user_login')


@login_required
def user_search_phone(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.user_phone:
                return redirect('user_dashboard')
            else:
                if request.method == 'POST':
                    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
                    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
                    client = Client(account_sid, auth_token)
                    local = client.available_phone_numbers('US').local.list(area_code=int(request.POST['area_code']), limit=5)
                    available_numbers = [record.friendly_name for record in local]
                    context = {
                        'available_numbers':available_numbers,
                    }
                    return render(request, 'text/search_phone.html', context)
                else:
                    if Registration.objects.filter().last().invite_required:
                        if RegistrationInviteCode.objects.filter(redeemed_by=request.user.username):
                            context = {}
                            return render(request, 'text/search_phone.html', context)
                        else:
                            return redirect('user_invitation')
                    else:
                        context = {}
                        return render(request, 'text/search_phone.html', context)
        else:
            return redirect('admin/')
    else:
        return redirect('user_login')


@login_required
def user_invitation(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            if request.method == 'POST':
                invite_code = RegistrationInviteCode.objects.filter(invite_code=request.POST['invite_code'], is_used=False)
                if invite_code:
                    invite_code[0].is_used = True
                    invite_code[0].redeemed_by = request.user.username
                    invite_code[0].save()
                    return redirect('user_search_phone')
                else:
                    messages.warning(request, ('The invitation code that was entered is invalid. Please try again.'))
                    context = {
                        'invite_code':request.POST['invite_code'],
                    }
                    return render(request, 'text/invitation_code.html', context)

            else:
                context = {}
                return render(request, 'text/invitation_code.html', context)
        else:
            return redirect('admin/')
    else:
        return redirect('user_login')


@login_required
def user_add_phone(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            if request.method == 'POST':
                user_profile = UserProfile.objects.get(user=request.user)
                form = UserAddPhoneForm(request.POST, instance=user_profile)
                if form.is_valid():
                    form.save()
                # Add and else statement for error handling

                return redirect('user_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            return redirect('admin/')
    else:
        return redirect('user_login')


@login_required
def user_delete_client(request, client_id):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            if request.method == 'POST':
                client = UserClient.objects.get(pk=client_id)
                client.delete()
                return redirect('user_dashboard')
            else:
                client = UserClient.objects.get(id=client_id)
                context = {
                    'client':client
                }
                return render(request, 'text/delete_client.html', context)
        else:
            return redirect('admin/')
    else:
        return redirect('user_login')


# Twilio specific views

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