from decimal import Decimal
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_204
from billboard.models import Billboard
from django.db.models import Q, F, Sum, Avg
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from billboard.serializers import BillboardSerializer
from rest_framework.pagination import PageNumberPagination

from rating.models import Rating
from rating.serializers import RatingSerializer
# Create your views here.


class Billboards(generics.GenericAPIView):
    serializer_class = BillboardSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def get(self, request):
        try:
            billboards = Billboard.objects.annotate(
                average_rating=Avg('rating__rating')).all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                billboards, request)

            serialized_results = self.serializer_class(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No billboards found', [])
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

    def generate_annotation_and_filter(self, conditions, min_price, max_price):
        annotation = None
        filter_condition = None

        for key, value in conditions.items():
            if value == 'true':
                if annotation is None:
                    annotation = Sum(key)
                else:
                    annotation += Sum(key)

        filter_condition = Q(
            total_sum__range=(min_price, max_price))

        return annotation, filter_condition

    def get(self, request):
        try:
            query = request.GET.get('q')
            location_filter = request.GET.get('location')
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            size_filter = request.GET.get('size')

            conditions = {
                'has_production': request.GET.get('has_production', 'false'),
                'daily_rate_per_sq': 'true',
            }
            billboards = Billboard.objects.annotate(
                average_rating=Avg('rating__rating')).all()
            if query:
                billboards = billboards.filter(Q(location__icontains=query) | Q(width__icontains=query) | Q(
                    height__icontains=query) | Q(daily_rate_per_sq__icontains=query)
                    | Q(production__icontains=query) | Q(status__icontains=query))

            if location_filter:
                billboards = billboards.filter(
                    location__icontains=location_filter)

            if size_filter:
                size_filter = int(size_filter)
                billboards = billboards.annotate(
                    area=F('width') * F('height')).filter(area__lte=size_filter)

            filtered_billboards = billboards
            if (min_price and max_price):
                # Generate dynamic annotation and filter based on conditions
                annotation, filter_condition = self.generate_annotation_and_filter(
                    conditions, min_price, max_price)
                filtered_billboards = billboards.annotate(
                    total_sum=annotation).filter(filter_condition)

            results = filtered_billboards.values(
                'location',
                'width',
                'height',
                'rate',
                'image',
                'daily_rate_per_sq',
                'production',
                'status',
                'description',
                'average_rating'
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
        except Exception as e:
            print(e)
            return error_404('Page not found.')


class BillboardRating(generics.GenericAPIView):
    serializer_class = RatingSerializer

    def get(self, request, id):
        try:
            print('innnn')
            ratings = Rating.objects.filter(
                billboard_id=id)
            serialized_results = ratings
            if ratings:
                serializer = self.serializer_class(ratings, many=True)
                paginator = PageNumberPagination()
                paginator.page_size = 6
                paginated_results = paginator.paginate_queryset(
                    ratings, request)

                serialized_results = self.serializer_class(
                    paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500('Something went wrong')
