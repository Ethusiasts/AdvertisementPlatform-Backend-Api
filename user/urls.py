from django.contrib import admin
from django.urls import path
from user.views import *

urlpatterns = [
    path('signup', SignUpAPI.as_view(), name="register"),
    path('login', LoginAPI.as_view(), name="login"),
    path('forgot-password', ForgotPasswordAPI.as_view(), name='forgot-password'),
    path('reset-password/<token>/',
         ResetPassword, name='reset-password'),
    path('activate/<token>/',
         ActivateAccountView.as_view(), name='activate'),
    path('profiles', UserProfileAPI.as_view(), name="profile"),
    path('profiles/<int:id>', UserProfileDetailAPI.as_view(), name="profile_detail"),



    # Only for test
    path('user/<int:id>', DeleteUser.as_view()),
    path('user', GetUser.as_view()),

]
