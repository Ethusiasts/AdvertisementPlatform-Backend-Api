import datetime
from django import forms
from django.shortcuts import render
import jwt
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from rest_framework.views import APIView
from advertisement_platform.settings import SECRET_KEY
from app.forms import ResetPasswordForm
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
                kwargs = {'first_name': request.data['first_name'],
                          'last_name': request.data['last_name']}
                User.objects.create_user(
                    request.data['email'], request.data['password'], **kwargs)
                return Response({
                    'status': 200,
                    'message': 'registration successful',
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            return Response({'sucess': False}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = request.data['email']
                password = request.data['password']
                user = authenticate(email=email, password=password)

            if user is None:
                return Response({
                    'status': 400,
                    'message': 'email or password is incorrect',
                    'data': {}
                })

            payload = ({
                'id': user.id,
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            })

            token = jwt.encode(payload, SECRET_KEY,
                               algorithm='HS256')

            return Response({
                'status': 200,
                'message': 'sucess',
                'token': token
            }
            )

        except Exception as e:
            print(e)
            return Response({'sucess': False}, status=status.HTTP_400_BAD_REQUEST)


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
            send_mail(
                'Reset Your Password',
                f'Please click the following link to reset your password: {reset_password_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'message': ' A link to reset your password has been sent to your email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# This code if for test only.


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
