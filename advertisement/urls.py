from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.AdvertisementListCreateAPIView.as_view()),
    path('<int:pk>/update/', views.AdvertisementUpdateAPIView.as_view())



]
