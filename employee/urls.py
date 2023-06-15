from django.urls import path
from employee.views import EmployeeBillboards, EmployeeDetail, Employees

urlpatterns = [
    path('', Employees.as_view()),
    path('<int:id>', EmployeeDetail.as_view()),
    path('<int:id>/billboards', EmployeeBillboards.as_view(),
         name="employee-billboards"),
]
