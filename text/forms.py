from django import forms
from .models import Phone

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        return f'+1{"".join(char for char in phone if char.isdigit())}'