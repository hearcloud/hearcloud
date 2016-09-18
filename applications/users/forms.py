from django import forms
from .models import User

from django.utils.translation import ugettext as _

class UserRegisterForm(forms.ModelForm):
    #password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username' : forms.TextInput(attrs = 
                {
                'class' : 'form-control user-form-control'
                }),
            'email' : forms.TextInput(attrs = 
                {
                'type' : 'email',
                'class' : 'form-control user-form-control'
                }),
            'password' : forms.TextInput(attrs =
                {
                'type' : 'password',
                'class' : 'form-control user-form-control'
                }),
        }
        labels = {
            'username' : _("Choose an username:"),
            'email' : _("What's your email address?"),
            'password': _("Choose a password:"),
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=40, 
                label = "Type your username",
                widget = forms.TextInput(attrs = {
                    'class' : 'form-control user-form-control'
                    }))
    password = forms.CharField(max_length=30,
                label = "Type your password",
                widget = forms.TextInput(attrs = {
                    'type' : 'password',
                    'class' : 'form-control user-form-control'
                    }))

class UserUpdateProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'picture' ]
        widgets = {
            'first_name': forms.TextInput(attrs = {'class' : 'form-control'}),
            'last_name': forms.TextInput(attrs = {'class' : 'form-control'}),
        }
        labels = {
            'first_name': _("First name:"),
            'last_name': _("Last name:"),
            'picture': _("Avatar:"),
        }

class UserUpdateSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username' : forms.TextInput(attrs = 
                {
                'class' : 'form-control'
                }),
            'email' : forms.TextInput(attrs = 
                {
                'type' : 'email',
                'class' : 'form-control'
                }),
            'password' : forms.TextInput(attrs =
                {
                'type' : 'password',
                'class' : 'form-control'
                }),
        }
        labels = {
            'username' : _("Choose an username:"),
            'email' : _("What's your email address?"),
            'password': _("Choose a password:"),
        }
