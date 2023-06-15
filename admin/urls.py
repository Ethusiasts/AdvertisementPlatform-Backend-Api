from django.urls import path
from admin.views import AdminDetail, Admins

urlpatterns = [
    path('<int:id>', AdminDetail.as_view()),
    path('', Admins.as_view()),

]
