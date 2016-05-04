#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import View
from django.views.generic import RedirectView

from django.utils.translation import ugettext as _

from .forms import UserRegisterForm, UserLoginForm

class UserRegisterFormView(View):
    """
    Users registration view
    """
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        """
        Display blank form if user is not loged
        """
        if request.user.is_authenticated():
            return redirect('box:index')

        form = self.form_class(None) # No context
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Process form data
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('box:index')

        return render(request, self.template_name, {'form': form})


class UserLogInFormView(View):
    """
    Users log in view
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
        """
        Display blank form if user is not loged
        """
        if request.user.is_authenticated():
            return redirect('box:index')

        form = self.form_class(None) # No context
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Process form data
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.GET:
                        return redirect(request.GET['next'])
                    else:
                        return redirect('box:index')

                else:
                    return render(request, self.template_name, {'error_message': _('Your account has been disabled'), 'form': form})
            else:
                return render(request, self.template_name, {'error_message': _('Invalid username/password'), 'form': form})

        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    """
    Users log out view
    """
    template_name = 'users/logout.html'
    
    def get(self, request):
        """
        Log out and show the logout template
        """
        logout(self.request)
        return redirect('home:index')
