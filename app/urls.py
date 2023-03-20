from django.contrib import admin
from django.urls import path
from app.views.user_views import *

urlpatterns = [
    path('auth/signup', SignUpAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/user', UserAPI.as_view()),
    path('forgot-password', ForgotPasswordAPI.as_view()),
    path('reset-password/<token>/',
         ResetPassword, name='reset-password'),
]
