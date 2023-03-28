from django import forms


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        max_length=128, widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(
        max_length=128, widget=forms.PasswordInput, required=True)
