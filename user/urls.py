from django.contrib import admin
from django.urls import path
from user.views import *

urlpatterns = [
    path('auth/signup', SignUpAPI.as_view(), name="register"),
    path('auth/login', LoginAPI.as_view(), name="login"),
    path('forgot-password', ForgotPasswordAPI.as_view(), name='forgot-password'),
    path('reset-password/<token>/',
         ResetPassword, name='reset-password'),
    path('auth/activate/<token>/',
         ActivateAccountView.as_view(), name='activate'),

    # Only for test
    path('user/<int:id>', DeleteUser.as_view()),

]
