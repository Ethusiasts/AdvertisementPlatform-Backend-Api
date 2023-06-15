from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_500, success_200, success_201, error_400, error_404, success_204
from billboard.models import Billboard
from billboard.serializers import BillboardGetSerializer
from employee.models import Employee
from rest_framework.pagination import PageNumberPagination


from employee.serializers import EmployeeGetSerializer, EmployeePostSerializer
from user.models import User

# Create your views here.


class Employees(generics.GenericAPIView):
    serializer_class = EmployeePostSerializer

    def get(self, request):
        try:
            employees = Employee.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                employees, request)

            serialized_results = EmployeeGetSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No employees found', [])
        except Exception as e:
            print(e)
            return error_400(serialized_results.errors)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        print(serializer.errors)
        return error_400(serializer.errors)


class EmployeeDetail(generics.GenericAPIView):
    serializer_class = EmployeeGetSerializer

    def get_employee(self, id):
        try:
            return Employee.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        employee = self.get_employee(id)
        if employee:
            serializer = self.serializer_class(employee)
            return success_200('sucess', serializer.data)
        return error_404(f'Employee with id: {id} not found.')

    def put(self, request, id):
        employee = self.get_employee(id)
        if employee == None:
            return error_404(f'Employee with id: {id} not found.')

        serializer = EmployeePostSerializer(
            employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        employee = self.get_employee(id)
        if employee == None:
            return error_404(f'Employee with id: {id} not found.')
        employee.delete()
        return success_204()


class EmployeeBillboards(generics.GenericAPIView):
    serializer_class = EmployeeGetSerializer

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            employees = Employee.objects.filter(
                user=user)
            serialized_results = employees
            if employees:
                serializer = self.serializer_class(employees, many=True)
                paginator = PageNumberPagination()
                paginator.page_size = 6
                paginated_results = paginator.paginate_queryset(
                    employees, request)

                serialized_results = self.serializer_class(
                    paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500(e)
