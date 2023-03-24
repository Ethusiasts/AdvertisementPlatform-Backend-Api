from rest_framework import generics, permissions, authentication
from .models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class AdvertisementListCreateAPIView(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def perform_create(self, serializer):

        return serializer.save()


class AdvertisementUpdateAPIView(generics.UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def perform_update(self, serializer):
        return serializer.save()
