from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        return f'+1{"".join(char for char in phone if char.isdigit())}'