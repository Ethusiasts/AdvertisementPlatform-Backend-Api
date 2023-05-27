from django.urls import path
from rating.views import Ratings, RatingDetail

urlpatterns = [
    path('', Ratings.as_view()),
    path('<int:id>', RatingDetail.as_view())
]
