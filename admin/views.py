from django.shortcuts import render
from rest_framework import generics
from admin.serializers import AdminBlockUserSerializer, AdminStatsSerializer
from advertisement_platform.errors import error_500, success_200, success_201, error_400, error_404, success_204
from user.models import User
# Create your views here.


class Admins(generics.GenericAPIView):
    serializer_class = AdminStatsSerializer

    def get(self, request):
        try:
            users = User.objects.filter(role='customer')
            landowners = User.objects.filter(role='landowner')
            tvs = User.objects.filter(role='TV')
            radios = User.objects.filter(role='RADIO')
            employees = User.objects.filter(role='Employee')

            total_user = users.count()
            total_landowner = landowners.count()
            total_tv = tvs.count()
            total_radio = radios.count()
            total_employee = employees.count()

            data = {
                'total_user': total_user,
                'total_landowner': total_landowner,
                'total_tv': total_tv,
                'total_radio': total_radio,
                'total_employee': total_employee,
            }

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                return success_200('Admin statistics retrieved successfully', serializer.data)
            return error_400(serializer.errors)

        except Exception as e:
            print(e)
            return error_500(e)


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
