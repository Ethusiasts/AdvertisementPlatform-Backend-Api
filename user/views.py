import datetime
from django import forms
from django.shortcuts import render
import jwt
from django.urls import reverse
from rest_framework.views import APIView
from advertisement_platform.settings import SECRET_KEY
from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_login_200
from user.forms import ResetPasswordForm
from advertisement_platform.helpers import send_email, valid_role
from user.models import User, UserProfile, user_reset_password_token
from user.serializers import ForgotPasswordSerializer, LoginSerializer, UserProfileSerializer, UserSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser


class SignUpAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                role = request.data['role']
                if valid_role(role):
                    kwargs = {'first_name': request.data['first_name'],
                              'last_name': request.data['last_name'], 'role': role}
                    user = User.objects.create_user(
                        request.data['email'], request.data['password'], **kwargs)
                    token = user_reset_password_token._create_token(user)
                    verification_link = request.build_absolute_uri(
                        reverse('activate', kwargs={'token': token}))
                    send_email('Activate your user account',
                               'Please click the following link to activate your account', request.data['email'], verification_link)

                    return success_200(
                        'Account activation link has been sent to your email. Please go ahead and click the link to activate your account', serializer.data
                    )

                return error_400('unknown user role')

            return error_400('user already exist')

        except Exception as e:
            print(e)
            return error_500(e)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
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

            return success_login_200(
                'You are successfully logged in.', token
            )

        except Exception as e:
            return error_400('bad request')


class ActivateAccountView(APIView):
    def get(self, request, token):
        try:
            token_obj = Token.objects.get(key=token)
            user = User.objects.get(pk=token_obj.user_id)
            if user is not None and token:
                user.is_verified = True
                user.save()
                return success_200('Account successfully activated.', '')

            return error_400('user not found')

        except Exception as e:
            print(e)
            return error_400('bad request')


class ForgotPasswordAPI(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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
            return success_200(
                'A link to reset your password has been sent to your email.', ''
            )
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


class UserProfileAPI(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        return error_400(serializer.errors)


class UserProfileDetailAPI(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request, id):
        user_profile = UserProfile.objects.get(id=id)
        if user_profile:
            serializer = self.serializer_class(user_profile)
            return success_200('sucess', serializer.data)
        return error_404(f'Userprofile with id: {id} not found.')

    def put(self, request, id):
        user_profile = UserProfile.objects.get(id=id)
        if user_profile == None:
            return error_404(f'User profile with id: {id} not found.')
        serializer = self.serializer_class(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)


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
