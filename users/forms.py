from django import forms
from .models import User

class UserRegisterForm(forms.ModelForm):
    #password = forms.CharField(widget = forms.PasswordInput)

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
            'username' : "Choose an username:",
            'email' : "What's your email address?",
            'password': "Choose a password:",
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=40, 
                label = "Type your username",
                widget = forms.TextInput(attrs = {
                    'class' : 'form-control'
                    }))
    password = forms.CharField(max_length=30,
                label = "Type your password",
                widget = forms.TextInput(attrs = {
                    'type' : 'password',
                    'class' : 'form-control'
                    }))
