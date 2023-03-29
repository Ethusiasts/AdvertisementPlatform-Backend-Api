from django.urls import path
from billboard.views import Billboards, BillboardDetail

urlpatterns = [
    path('', Billboards.as_view()),
    path('<int:id>', BillboardDetail.as_view())
]
