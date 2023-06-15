from django.urls import path
from admin.views import AdminDetail

urlpatterns = [
    path('<int:id>', AdminDetail.as_view()),
]
