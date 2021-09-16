from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import HiddenInput, TextInput
from .models import UserClient, UserProfile


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), label='')
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), label='')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<small class="form-text text-muted">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = "<ul class='form-text text-muted small'><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul>"

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<small class="form-text text-muted">Enter the same password as before, for verification.</small>'


class UserEditUserForm(UserChangeForm):
    password = None
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control',}), label='')
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control',}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control',}), label='')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class UserAddPhoneForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_phone',)

    def clean_user_phone(self):
        user_phone = self.cleaned_data['user_phone']
        return f'+1{"".join(char for char in user_phone if char.isdigit())}'
    

class UserClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=TextInput(attrs={'class':'form-control', 'placeholder':'First Name', 'name':'first_name', 'aria-label':'First Name', 'required':'',}), label='')
    last_name = forms.CharField(max_length=100, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Last Name', 'name':'last_name', 'aria-label':'Last Name', 'required':'',}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address', 'name':'email', 'aria-label':'Email Address', 'required':'',}), label='')
    phone = forms.CharField(max_length=100, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number', 'name':'phone', 'aria-label':'Phone Number', 'pattern':'^[(]{0,1}[0-9]{3}[)]{0,1}[-\s.]{0,1}[0-9]{3}[-\s.]{0,1}[0-9]{4}$'}), label='')
    client_of = forms.CharField(max_length=100, widget=HiddenInput())

    class Meta:
        model = UserClient
        fields = ('first_name', 'last_name', 'email', 'phone','client_of',)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return f'+1{"".join(char for char in phone if char.isdigit())}'

    def clean_client_of(self):
        client_of = int(self.cleaned_data['client_of'])
        return User.objects.get(id=client_of)
    