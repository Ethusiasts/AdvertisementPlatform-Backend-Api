import datetime
import jwt
from rest_framework.views import APIView
from advertisement_platform.settings import SECRET_KEY
from app.models.user_models import User
from app.serializers.user_serializers import LoginSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
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
