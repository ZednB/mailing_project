import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail

from config import settings
from users.forms import UserRegisterForm, UserForm

from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('mail:base')


class UserLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        new_token = ''.join([str(random.randint(0,9)) for i in range(10)])
        new_user.token = new_token
        message = f"Для подтвеждения регистрации перейдите по ссылке: \
        http://127.0.0.1:8000/users/verify/?token={new_token}"
        send_mail(
            subject='Поздравляем с регистрацией.',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        return super().form_valid(form)


def activate_user(request):
    key = request.GET.get('token')
    current_user = User.objects.filter(is_active=False)
    for user in current_user:
        if str(user.token) == str(key):
            user.is_active = True
            user.token = None
            user.save()
    response = redirect(reverse_lazy('users:login'))
    return response


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('newsletter_list')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_all_users'

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk).exclude(is_superuser=True)


@permission_required('users.block_user')
def toggle_activity(request, pk):
    user = get_object_or_404(User, pk=pk)
    # user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:user_list'))


