from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, success_200, success_201
from media_agency.models import MediaAgency

from media_agency.serializers import MediaAgencySerializer
# Create your views here.


class MediaAgencies(generics.GenericAPIView):
    serializer_class = MediaAgencySerializer

    def get(self, request):
        media_agencies = MediaAgency.objects.all()
        return success_200('sucess', media_agencies)

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
            return success_200('sucess', media_agency)
        return error_404(f'MediaAgency with id: {id} not found.')

    def put(self, request, id):
        media_agency = self.get_media_agency(id)
        if media_agency == None:
            return error_404(f'media_agency with id: {id} not found.')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', media_agency)
        return error_400(serializer.errors)
