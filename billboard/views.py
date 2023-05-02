from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, success_200, success_201, success_204
from billboard.models import Billboard
from rest_framework.parsers import MultiPartParser, FormParser

from billboard.serializers import BillboardSerializer
# Create your views here.


class Billboards(generics.GenericAPIView):
    serializer_class = BillboardSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        billboards = Billboard.objects.all()
        return success_200('sucess', billboards)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        print(serializer.errors)
        return error_400(serializer.errors)


class BillboardDetail(generics.GenericAPIView):
    serializer_class = BillboardSerializer
    parser_classes = (MultiPartParser,)

    def get_billboard(self, id):
        try:
            return Billboard.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        billboard = self.get_billboard(id)
        if billboard:
            return success_200('sucess', billboard)
        return error_404(f'Billboard with id: {id} not found.')

    def put(self, request, id):
        billboard = self.get_billboard(id)
        if billboard == None:
            return error_404(f'Billboard with id: {id} not found.')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', billboard)
        return error_400(serializer.errors)

    def delete(self, request, id):
        billboard = self.get_billboard(id)
        if billboard == None:
            return error_404(f'Billboard with id: {id} not found.')
        billboard.delete()
        return success_204()


class SearchBillboards(generics.GenericAPIView):
    def get(self, request):
        return
