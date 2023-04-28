from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import success_200, success_201, error_400, error_404, success_204
from agency.models import Agency

from agency.serializers import AgencySerializer
# Create your views here.


class Agencies(generics.GenericAPIView):
    serializer_class = AgencySerializer

    def get(self, request):
        agencies = Agency.objects.all()
        return success_200('sucess', agencies)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        print(serializer.errors)
        return error_400(serializer.errors)


class AgencyDetail(generics.GenericAPIView):
    serializer_class = AgencySerializer

    def get_agency(self, id):
        try:
            return Agency.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        agency = self.get_agency(id)
        if agency:
            return success_200('sucess', agency)
        return error_404(f'Agency with id: {id} not found.')

    def put(self, request, id):
        agency = self.get_agency(id)
        if agency == None:
            return error_404(f'Agency with id: {id} not found.')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', agency)
        return error_400(serializer.errors)

    def delete(self, request, id):
        agency = self.get_agency(id)
        if agency == None:
            return error_404(f'Agency with id: {id} not found.')
        agency.delete()
        return success_204()
