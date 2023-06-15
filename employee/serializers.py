from rest_framework import serializers
from billboard.serializers import BillboardGetSerializer

from employee.models import Employee


class EmployeePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'billboard_id']


class EmployeeGetSerializer(serializers.ModelSerializer):
    billboard_id = BillboardGetSerializer()

    class Meta:
        model = Employee
        fields = '__all__'
