from rest_framework import generics, permissions, authentication

from advertisement_platform.errors import error_400, error_404, success_200, success_201, success_204
from .models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class Advertisements(generics.GenericAPIView):
    serializer_class = AdvertisementSerializer

    def get(self, request):
        try:
            advertisements = Advertisement.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                advertisements, request)

            serialized_results = self.serializer_class(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No advertisements found', [])
        except Exception as e:
            print(e)
            return error_400(serialized_results.errors)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_201('successfully created', serializer.data)
        except Exception as e:
            print(e)
            return error_400(e)


class AdvertisementDetail(generics.GenericAPIView):
    serializer_class = AdvertisementSerializer

    def get_billboard(self, id):
        try:
            return Advertisement.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        billboard = self.get_billboard(id)
        if billboard:
            serializer = self.serializer_class(billboard)
            return success_200('', serializer.data)
        return error_404(f'Advertisement with id: {id} not found.')

    def put(self, request, id):
        billboard = self.get_billboard(id)
        if billboard == None:
            return error_404(f'billboard with id: {id} not found.')
        serializer = self.serializer_class(billboard, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        billboard = self.get_billboard(id)
        if billboard == None:
            return error_404(f'Advertisement with id: {id} not found.')
        billboard.delete()
        return success_204()
