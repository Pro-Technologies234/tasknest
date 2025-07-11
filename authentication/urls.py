from django.urls import path
from .views import login_user, register_user, logout_user, get_user_profile, update_user

urlpatterns = [
    path('login_user', login_user, name="login_user"),
    path('register_user', register_user, name="register_user"),
    path('logout_user', logout_user, name="logout_user"),
    path('get_user_profile', get_user_profile, name="get_user_profile"),
    path('update_user', update_user, name="update_user"),
]
