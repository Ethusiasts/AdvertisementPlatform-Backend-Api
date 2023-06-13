from rest_framework import generics, permissions, authentication
from advertisement.predict import checkImage
# from advertisement.predict import checkImage

from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_204
from .models import Advertisement
from .serializers import AdvertisementGetSerializer, AdvertisementPostSerializer, ImageCheckerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Advertisements(generics.GenericAPIView):
    serializer_class = AdvertisementPostSerializer

    def get(self, request):
        try:
            advertisements = Advertisement.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                advertisements, request)

            serialized_results = AdvertisementGetSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No advertisements found', [])
        except Exception as e:
            print(e)
            return error_500('internal server error')

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_201('successfully created', serializer.data)
            else:
                print(serializer.errors)
        except Exception as e:
            print(e)
            return error_500('internal server error')


class AdvertisementDetail(generics.GenericAPIView):
    serializer_class = AdvertisementPostSerializer

    def get_advertisement(self, id):
        try:
            return Advertisement.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        advertisement = self.get_advertisement(id)
        if advertisement:
            serializer = AdvertisementGetSerializer(advertisement)
            return success_200('', serializer.data)
        return error_404(f'Advertisement with id: {id} not found.')

    def put(self, request, id):
        advertisement = self.get_advertisement(id)
        if advertisement == None:
            return error_404(f'advertisement with id: {id} not found.')
        serializer = self.serializer_class(advertisement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        advertisement = self.get_advertisement(id)
        if advertisement == None:
            return error_404(f'Advertisement with id: {id} not found.')
        advertisement.delete()
        return success_204()


class ImageCkecker(generics.GenericAPIView):
    serializer_class = ImageCheckerSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def post(self, request):
        # print(request.data['image'])
        try:
            print('innnn')
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                image_url = serializer.validated_data['image']
                result = checkImage(image_url)
                if result == 0:
                    return success_200('successfully checked', False)
                elif result == 1:
                    return success_200('successfully checked', True)
                else:
                    return error_400("Image couldn't be loadded")
            else:
                print(serializer.errors)

        except Exception as e:
            print(e)
            return error_400(e)
