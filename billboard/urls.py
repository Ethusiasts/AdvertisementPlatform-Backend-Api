from django.urls import path
from billboard.views import Billboards, BillboardDetail

urlpatterns = [
    path('', Billboards.as_view(), name='billboards'),
    path('<int:id>', BillboardDetail.as_view(), name='billboard')
]
