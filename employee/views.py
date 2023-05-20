from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import success_200, success_201, error_400, error_404, success_204
from employee.models import Employee

from employee.serializers import EmployeeSerializer

# Create your views here.


class Employees(generics.GenericAPIView):
    serializer_class = EmployeeSerializer

    def get(self, request):
        employees = Employee.objects.all()
        return success_200('sucess', employees)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        print(serializer.errors)
        return error_400(serializer.errors)


class EmployeeDetail(generics.GenericAPIView):
    serializer_class = EmployeeSerializer

    def get_employee(self, id):
        try:
            return Employee.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        employee = self.get_employee(id)
        if employee:
            return success_200('sucess', employee)
        return error_404(f'Employee with id: {id} not found.')

    def put(self, request, id):
        employee = self.get_employee(id)
        if employee == None:
            return error_404(f'Employee with id: {id} not found.')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', employee)
        return error_400(serializer.errors)

    def delete(self, request, id):
        employee = self.get_employee(id)
        if employee == None:
            return error_404(f'Employee with id: {id} not found.')
        employee.delete()
        return success_204()
