from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, success_200, success_201
from landowner.models import Landowner

from landowner.serializers import LandownerSerializer
# Create your views here.


class Landowners(generics.GenericAPIView):
    serializer_class = LandownerSerializer

    def get(self, request):
        landowners = Landowner.objects.all()
        return success_200('sucess', landowners)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        return error_400(serializer.errors)


class LandownerDetail(generics.GenericAPIView):
    serializer_class = LandownerSerializer

    def get_landowner(self, id):
        try:
            return Landowner.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        landowner = self.get_landowner(id)
        if landowner:
            return success_200('sucess', landowner)
        return error_404(f'Landowner with id: {id} not found.')

    def put(self, request, id):
        landowner = self.get_landowner(id)
        if landowner == None:
            return error_404(f'landowner with id: {id} not found.')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', landowner)
        return error_400(serializer.errors)
