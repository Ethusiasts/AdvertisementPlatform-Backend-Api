import datetime
from django import forms
from django.shortcuts import render
import jwt
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework.views import APIView
from advertisement_platform.settings import SECRET_KEY
from app.errors import error_400, error_500, sucess_200, sucess_201, sucess_login_200
from app.forms import ResetPasswordForm
from app.helpers import find_role, send_email, valid_role
from app.models.user_models import User, user_reset_password_token
from app.serializers.user_serializers import ForgotPasswordSerializer, LoginSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class SignUpAPI(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                role = request.data['role']
                if valid_role(role):
                    kwargs = {'first_name': request.data['first_name'],
                              'last_name': request.data['last_name'], 'role': role}
                    user = User.objects.create_user(
                        request.data['email'], request.data['password'], **kwargs)
                    token = user_reset_password_token._create_token(user)
                    verification_link = request.build_absolute_uri(
                        reverse('activate-account', kwargs={'token': token}))
                    send_email('Activate your user account',
                               'Please click the following link to activate your account', request.data['email'], verification_link)

                    return sucess_200(
                        'Account activation link has been sent to your email. Please go ahead and click the link to activate your account', serializer.data
                    )

                return error_400('unknown user role')

            return error_400('user already exist')

        except Exception as e:
            return error_500('something went wrong')


class LoginAPI(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = request.data['email']
                password = request.data['password']
                user = authenticate(email=email, password=password)
            if user is None:
                return error_400('email or password is incorrect')

            if not user.is_verified:
                return error_400('your account is not activated')

            payload = ({
                'id': user.id,
                'role': user.role,
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            })

            token = jwt.encode(payload, SECRET_KEY,
                               algorithm='HS256')

            return sucess_login_200(
                'You are successfully loged in.', token
            )

        except Exception as e:
            return error_400('bad request')


class ForgotPasswordAPI(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            token = user_reset_password_token._create_token(user)
            reset_password_link = request.build_absolute_uri(
                reverse('reset-password', kwargs={'token': token}))

            send_email('Reset Your Password',
                       'Please click the following link to reset your password', email, reset_password_link)
            return sucess_200(
                'A link to reset your password has been sent to your email.'
            )
        return error_400('bad request')


def ActivateAccount(request, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(pk=token_obj.user_id)
        if user is not None and token:
            user.is_verified = True
            user.save()
            return sucess_200('Account sucessfully activated.')

        return error_400('user not found')

    except Exception as e:
        return error_400('bad request')


def ResetPassword(request, token):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = request.POST['new_password1']
            confirm_password = request.POST['new_password2']
            try:
                token_obj = Token.objects.get(key=token)
            except Token.DoesNotExist:
                return render(request, '')

            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

            user = User.objects.get(pk=token_obj.user_id)
            user.set_password(password)
            user.save()
        return render(request, 'app/reset_password.html', {'form': form})

    return render(request, "app/reset_password.html")


# Code below is for test only.


class UserAPI(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        if not token:
            return Response({'message': 'unauthenticated user'})

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        except Exception as e:
            print(e)
            return Response({'message': 'something went wrong'})

        return Response(payload['id'])


class DeleteUser(APIView):
    def delete(self, request, id):
        if request.method == 'DELETE':
            try:
                user = User.objects.get(id=id)
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                print(e)
                return Response({'message': 'something went wrong'})
