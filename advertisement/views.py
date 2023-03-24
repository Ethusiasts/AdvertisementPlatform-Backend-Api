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


class AdvertisementDetailsAPIView(generics.RetrieveAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer


class AdvertisementUpdateAPIView(generics.UpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def perform_update(self, serializer):
        return serializer.save()


class AdvertisementDeleteAPIView(generics.DestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
