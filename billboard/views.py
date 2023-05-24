from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, success_200, success_201, success_204
from billboard.models import Billboard
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
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
        try:
            billboards = Billboard.objects.all()
            serializer = self.serializer_class(billboards, many=True)
            return success_200('sucess', serializer.data)
        except Exception as e:
            print(e)
            return error_400(serializer.errors)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_201('successfully created', serializer.data)
        except Exception as e:
            print(e)
            return error_400(e)


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
    serializer_class = BillboardSerializer

    def get(self, request):
        try:
            query = request.GET.get('q')
            if query:
                results = Billboard.objects.filter(Q(location__icontains=query) | Q(width__icontains=query) | Q(
                    height__icontains=query) | Q(rate__icontains=query)).values('location', 'width', 'height', 'rate', 'image')
                return success_200('sucess', results)
            return success_200('No results found', [])
        except Exception as e:
            print(e)
            return error_404('Page not found.')
