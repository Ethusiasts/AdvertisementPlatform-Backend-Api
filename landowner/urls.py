from django.urls import path
from landowner.views import LandownerDetail, Landowners

urlpatterns = [
    path('', Landowners.as_view()),
    path('<int:id>', LandownerDetail.as_view())
]
