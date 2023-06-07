from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.Advertisements.as_view()),
    path('<int:id>', views.AdvertisementDetail.as_view(),
         name='advertisement-detail'),
    # path('image', views.ImageCkecker.as_view()),


]
