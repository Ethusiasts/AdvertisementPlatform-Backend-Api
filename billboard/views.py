from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, success_200, success_201, success_204
from billboard.models import Billboard
from rest_framework.parsers import MultiPartParser, FormParser
import pyrebase
from advertisement_platform.settings import config
from billboard.serializers import BillboardSerializer
# Create your views here.


# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()
# first image name to be displayed on the database then image name that you want it to be upload to firebase
# storage.child(".test1.jpg").put("./media/billboard2.jpg")

# url = storage.child(".test1.jpg").get_url(None)
# print(url)


class Billboards(generics.GenericAPIView):
    serializer_class = BillboardSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        billboards = Billboard.objects.all()
        serializer = self.serializer_class(billboards, many=True)
        return success_200('sucess', serializer.data)

    def post(self, request):
        image = request.data['image']
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        uploaded_image = storage.put(image)
        image_name = uploaded_image['name']
        image_url = storage.child(image_name).get_url(None)
        request.data['image'] = image_url
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
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
            serializer = self.serializer_class(billboard)
            return success_200('', serializer.data)
        return error_404(f'Billboard with id: {id} not found.')

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
            return error_404(f'Billboard with id: {id} not found.')
        billboard.delete()
        return success_204()


class SearchBillboards(generics.GenericAPIView):
    def get(self, request):
        return
