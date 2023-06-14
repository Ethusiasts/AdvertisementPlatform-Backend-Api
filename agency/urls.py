from django.urls import path
from agency.views import AgencyDetail, Agencies, AgencyRating, AgencyRecommendation, SearchAgencies

urlpatterns = [
    path('', Agencies.as_view()),
    path('<int:id>', AgencyDetail.as_view()),
    path('<int:id>/ratings/', AgencyRating.as_view(), name='agency-rating'),
    path('search', SearchAgencies.as_view(), name='search'),
    path('recommendations', AgencyRecommendation.as_view(), name='recommendation')

]
