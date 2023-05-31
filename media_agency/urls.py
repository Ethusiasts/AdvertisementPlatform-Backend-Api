from django.urls import path
from media_agency.views import MediaAgencyBillboards, MediaAgencyDetail, MediaAgencies

urlpatterns = [
    path('', MediaAgencies.as_view(), name="media-agencies"),
    path('<int:id>/billboards/', MediaAgencyBillboards.as_view(),
         name="media-agency-billboards"),
    path('<int:id>', MediaAgencyDetail.as_view(), name="media-agency")
]
