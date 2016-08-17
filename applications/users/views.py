#-*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.utils.timezone import now as tznow
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic import View

from applications.box.views import handler401
from .forms import UserRegisterForm, UserLoginForm, UserUpdateProfileForm
from .models import User


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

        form = self.form_class(None)  # No context
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


class UserDetailView(generic.DetailView):
    template_name = "users/detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(
            today = tznow(),
            **kwargs
        )
        return context

    def get(self, request, **kwargs):
        # Check if the user is trying to get his profile page or another user page
        if not request.user.id == User.objects.get(slug=kwargs['slug']).id:
            return handler401(request)

        return super(UserDetailView, self).get(request)


class UserUpdateView(generic.UpdateView):
    template_name = "users/user_profile_form.html"
    form_class = UserUpdateProfileForm
    model = User

    def form_valid(self, form):
        form.instance.user = self.request.user

        user = form.save(commit=False) # Creates an object from the form but doesn't save it into db yet

        # Save into db
        user.save()

        return super(UserUpdateView, self).form_valid(form)
