from django.urls import path
from agency.views import AgencyDetail, Agencies

urlpatterns = [
    path('', Agencies.as_view()),
    path('<int:id>', AgencyDetail.as_view())
]
