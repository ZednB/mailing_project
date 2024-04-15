from django.urls import path
from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, RegisterView, UserUpdateView, activate_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('verify/', activate_user),
]