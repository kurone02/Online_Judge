from django import forms
from django.contrib.auth.models import User
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(label = 'Username ', max_length = 30)
    email = forms.EmailField(label = 'Email ')
    password = forms.CharField(label = 'Password ', widget = forms.PasswordInput())
    repass = forms.CharField(label = 'Repass ', widget = forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Your username contains special characters!")
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Your username has already existed!")

    def clean_repass(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            repass = self.cleaned_data['repass']
            if password == repass and password:
                return repass
        raise forms.ValidationError('Password is invalid!')

    def save(self):
        User.objects.create_user(username = self.cleaned_data['username'], email = self.cleaned_data['email'], password = self.cleaned_data['password'])