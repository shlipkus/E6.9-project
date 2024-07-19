from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator
from .validators import validate_size

from .models import User


class RegForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    def clean(self):
        if User.objects.filter(username=self.cleaned_data.get('username')):  #проверяем есть ли в базе такой username
            raise forms.ValidationError('This username already in use.')
        pass1 = self.cleaned_data.get('password')  #проверка совпадения пароля
        pass2 = self.cleaned_data.get('password_confirm')
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('Password do not match')
        return pass2


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class EditForm(forms.Form):
    nickname = forms.CharField(label='Никнэйм', max_length=64)
    avatar = forms.ImageField(required=False, validators=[FileExtensionValidator(allowed_extensions=['png']),
                                                          validate_size(200, 200)],
                              help_text='only png')
