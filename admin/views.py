from django.shortcuts import render
from rest_framework import generics
from admin.serializers import AdminBlockUserSerializer
from advertisement_platform.errors import error_500, success_200, success_201, error_400, error_404, success_204
from user.models import User
# Create your views here.


class AdminDetail(generics.GenericAPIView):
    serializer_class = AdminBlockUserSerializer

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            if user == None:
                return error_404(f'User with id: {id} not found.')

            serializer = AdminBlockUserSerializer(user, data=request.data)
            if serializer.is_valid():
                user.is_blocked = serializer.validated_data.get(
                    'is_blocked', user.is_blocked)
                user.save()
                return success_200('sucess', serializer.data)
            return error_400(serializer.errors)
        except Exception as e:
            print(e)
            return error_500(e)
