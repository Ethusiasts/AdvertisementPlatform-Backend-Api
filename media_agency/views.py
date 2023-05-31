from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_204
from billboard.models import Billboard
from billboard.serializers import BillboardSerializer
from media_agency.models import MediaAgency
from django.core.serializers import serialize
from rest_framework.pagination import PageNumberPagination
import json
from media_agency.serializers import MediaAgencySerializer
# Create your views here.


class MediaAgencies(generics.GenericAPIView):
    serializer_class = MediaAgencySerializer

    def get(self, request):
        media_agencies = MediaAgency.objects.all()
        serializer = self.serializer_class(media_agencies, many=True)
        return success_200('sucess', serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        return error_400(serializer.errors)


class MediaAgencyDetail(generics.GenericAPIView):
    serializer_class = MediaAgencySerializer

    def get_media_agency(self, id):
        try:
            return MediaAgency.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        media_agency = self.get_media_agency(id)
        if media_agency:
            serializer = self.serializer_class(media_agency)
            return success_200('', serializer.data)
        return error_404(f'MediaAgency with id: {id} not found.')

    def put(self, request, id):
        media_agency = self.get_media_agency(id)
        if media_agency == None:
            return error_404(f'media_agency with id: {id} not found.')
        serializer = self.serializer_class(media_agency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        media_agency = self.get_media_agency(id)
        if media_agency == None:
            return error_404(f'MediaAgency with id: {id} not found.')
        media_agency.delete()
        return success_204()


class MediaAgencyBillboards(generics.GenericAPIView):
    serializer_class = BillboardSerializer

    def get(self, request, id):
        try:
            billboards = Billboard.objects.filter(
                media_agency_id=id)
            if billboards:
                serializer = self.serializer_class(billboards, many=True)
                paginator = PageNumberPagination()
                paginator.page_size = 6
                paginated_results = paginator.paginate_queryset(
                    billboards, request)

                serialized_results = self.serializer_class(
                    paginated_results, many=True).data

                if serialized_results:
                    return paginator.get_paginated_response(serialized_results)
                else:
                    return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500('Something went wrong')
