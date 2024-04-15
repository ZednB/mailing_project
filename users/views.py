from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('mail:base')


class UserLogoutView(LogoutView):
    pass
