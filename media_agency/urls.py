from django.urls import path
from media_agency.views import MediaAgencyAgencies, MediaAgencyBillboards, MediaAgencyContracts, MediaAgencyDetail, MediaAgencies, MediaAgencyProposals, MediaAgencyStats

urlpatterns = [
    path('', MediaAgencies.as_view(), name="media-agencies"),
    path('<int:id>/billboards/', MediaAgencyBillboards.as_view(),
         name="media-agency-billboards"),
    path('<int:id>/agencies/', MediaAgencyAgencies.as_view(),
         name="media-agency-agencies"),
    path('<int:id>/contracts/', MediaAgencyContracts.as_view(),
         name="media-agency-contracts"),
    path('<int:id>/proposals/', MediaAgencyProposals.as_view(),
         name="media-agency-proposals"),
    path('<int:id>', MediaAgencyDetail.as_view(), name="media-agency"),
    path('<int:id>/stats/', MediaAgencyStats.as_view(),
         name="media-agency-stats"),
]
