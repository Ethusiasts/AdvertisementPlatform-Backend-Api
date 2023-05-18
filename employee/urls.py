from django.urls import path
from employee.views import EmployeeDetail, Employees

urlpatterns = [
    path('', Employees.as_view()),
    path('<int:id>', EmployeeDetail.as_view())
]
