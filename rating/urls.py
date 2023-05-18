from django.urls import path
from rating.views import RatingDetail, Ratings

urlpatterns = [
    path('', Ratings.as_view()),
    path('<int:id>', RatingDetail.as_view())
]
