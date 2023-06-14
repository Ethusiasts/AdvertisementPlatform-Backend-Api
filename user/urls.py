from django.contrib import admin
from django.urls import path
from user.views import *

urlpatterns = [
    path('signup', SignUpAPI.as_view(), name="register"),
    path('login', LoginAPI.as_view(), name="login"),
    path('forgot-password', ForgotPasswordAPI.as_view(), name='forgot-password'),
    path('reset-password',
         ResetPasswordAPI.as_view(), name='reset-password'),
    path('activate/<token>/',
         ActivateAccountView.as_view(), name='activate'),
    path('profiles', UserProfileAPI.as_view(), name="profile"),
    path('profiles/<int:id>', UserProfileDetailAPI.as_view(), name="profile_detail"),

    path('<int:id>/advertisements/', UserAdvertisements.as_view(),
         name="user-advertisements"),
    path('<int:id>/contracts/', UserContracts.as_view(),
         name="user-contracts"),
    path('<int:id>/proposals/', UserProposals.as_view(),
         name="user-proposals"),
    path('<int:id>/stats/', UserStats.as_view(),
         name="user-stats"),



    # Only for test
    path('user/<int:id>', DeleteUser.as_view()),
    path('users', GetUser.as_view()),

]
