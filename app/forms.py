from django import forms

from app.models.user_models import User
from django.contrib.auth.password_validation import CommonPasswordValidator, NumericPasswordValidator, UserAttributeSimilarityValidator


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        max_length=128, widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(
        max_length=128, widget=forms.PasswordInput, required=True)
