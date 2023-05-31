from django.urls import path
from billboard.views import Billboards, BillboardDetail, SearchBillboards, BillboardRating

urlpatterns = [
    path('', Billboards.as_view(), name='billboards'),
    path('<int:id>', BillboardDetail.as_view(), name='billboard'),
    path('<int:id>/ratings/', BillboardRating.as_view(), name='billboard-rating'),
    path('search', SearchBillboards.as_view(), name='search')

]
