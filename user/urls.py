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

    path('<int:id>/advertisements/', UserAdvertisements.as_view(),
         name="media-agency-advertisements"),
    path('<int:id>/contracts/', UserContracts.as_view(),
         name="media-agency-contracts"),
    path('<int:id>/proposals/', UserProposals.as_view(),
         name="media-agency-proposals"),



    # Only for test
    path('user/<int:id>', DeleteUser.as_view()),
    path('users', GetUser.as_view()),

]
