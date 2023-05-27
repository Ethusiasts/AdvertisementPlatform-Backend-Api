from decimal import Decimal
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, success_200, success_201, success_204
from billboard.models import Billboard
from django.db.models import Q
from django.db.models import F
from rest_framework.parsers import MultiPartParser, FormParser
from billboard.serializers import BillboardSerializer
from rest_framework.pagination import PageNumberPagination
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
            location_filter = request.GET.get('location')
            has_production = request.GET.get('has_production')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            size_filter = request.GET.get('size')
            billboards = Billboard.objects.all()
            if query:
                billboards = billboards.filter(Q(location__icontains=query) | Q(width__icontains=query) | Q(
                    height__icontains=query) | Q(monthly_rate_per_sq__icontains=query))

            if location_filter:
                billboards = billboards.filter(
                    location__icontains=location_filter)
            if has_production:
                has_production = has_production.lower() == 'true'
                billboards = billboards.filter(production=has_production)
            if min_price:
                min_price = Decimal(min_price)
                billboards = billboards.filter(
                    monthly_rate_per_sq__gte=min_price)
            if max_price:
                max_price = Decimal(max_price)
                billboards = billboards.filter(
                    monthly_rate_per_sq__lte=max_price)
            if size_filter:
                size_filter = int(size_filter)
                billboards = billboards.annotate(
                    area=F('width') * F('height')).filter(area__lte=size_filter)

            results = billboards.values(
                'location',
                'width',
                'height',
                'rate',
                'image',
                'monthly_rate_per_sq',
                'production'
            )

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(results, request)

            serialized_results = self.serializer_class(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])
            # if results:
                # return success_200('sucess', results)
            # else:
                # return success_200('No results found', [])
        except Exception as e:
            print(e)
            return error_404('Page not found.')
