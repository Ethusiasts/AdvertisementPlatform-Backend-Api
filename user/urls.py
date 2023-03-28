from django.contrib import admin
from django.urls import path
from user.views import *

urlpatterns = [
    path('auth/signup', SignUpAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('forgot-password', ForgotPasswordAPI.as_view()),
    path('reset-password/<token>/',
         ResetPassword, name='reset-password'),
    path('auth/activate/<token>/',
         ActivateAccount, name='activate-account'),

    # Only for test
    path('user/<int:id>', DeleteUser.as_view()),

]
