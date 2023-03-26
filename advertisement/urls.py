from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.AdvertisementListCreateAPIView.as_view()),
    path('<int:pk>/', views.AdvertisementDetailsAPIView.as_view(),
         name='advertisement-detail'),
    path('<int:pk>/update/', views.AdvertisementUpdateAPIView.as_view()),
    path('<int:pk>/delete/', views.AdvertisementDeleteAPIView.as_view())




]
