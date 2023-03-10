from rest_framework.views import APIView
from app.models.user_models import User
from app.serializers.user_serializers import LoginSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response


class SignUpAPI(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
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
                email = serializer.data['email']
                password = serializer.data['password']

                user = User.objects.get(email=email, password=password)

                if user is None:
                    return Response({
                        'status': 400,
                        'message': 'invalid credential',
                        'data': {}
                    })

            return Response({
                'status': 200,
                'message': 'sucess',
                'data': serializer.data
            })
        except Exception as e:
            return Response({'sucess': False}, status=status.HTTP_400_BAD_REQUEST)
