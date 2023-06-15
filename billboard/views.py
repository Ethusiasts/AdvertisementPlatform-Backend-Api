from decimal import Decimal
import math
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_204
from billboard.models import Billboard
from django.db.models import Q, F, Sum, Avg
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from billboard.serializers import BillboardGetSerializer, BillboardPostSerializer, BillboardPutSerializer, BillboardRatingSerializer, BillboardSearchSerializer
from rest_framework.pagination import PageNumberPagination
from employee.models import Employee

from rating.models import Rating
from rating.serializers import RatingGetSerializer
from user.models import User
# Create your views here.


class Billboards(generics.GenericAPIView):
    serializer_class = BillboardPostSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def get(self, request):
        try:
            billboards = Billboard.objects.filter(paid=True)

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                billboards, request)

            serialized_results = BillboardRatingSerializer(
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
                user = User.objects.get(id=11)
                billboard = serializer.save()
                billboard_result = Billboard.objects.get(id=billboard.id)
                employee = Employee(user=user, billboard_id=billboard_result)
                employee.save()
                return success_201('successfully created', serializer.data)
        except Exception as e:
            print(e)
            return error_400(e)


class BillboardDetail(generics.GenericAPIView):
    serializer_class = BillboardGetSerializer

    def get_billboard(self, id):
        try:
            return Billboard.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        billboard = self.get_billboard(id)
        if billboard:
            serializer = BillboardRatingSerializer(billboard)
            return success_200('', serializer.data)
        return error_404(f'Billboard with id: {id} not found.')

    def put(self, request, id):
        billboard = self.get_billboard(id)
        if billboard == None:
            return error_404(f'billboard with id: {id} not found.')
        serializer = BillboardGetSerializer(
            billboard, data=request.data, partial=True)
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
    serializer_class = BillboardRatingSerializer

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
            latitude = request.GET.get('latitude')
            longitude = request.GET.get('longitude')
            radius = float(request.GET.get('radius', '1'))
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            size_filter = request.GET.get('size')

            conditions = {
                'production': request.GET.get('production', 'false'),
                'daily_rate_per_sq': 'true',
            }
            # billboards = Billboard.objects.all()
            billboards = Billboard.objects.all()
            if query:
                billboards = billboards.filter(Q(latitude__icontains=query) | Q(longitude__icontains=query) | Q(width__icontains=query) | Q(
                    height__icontains=query) | Q(daily_rate_per_sq__icontains=query)
                    | Q(production__icontains=query) | Q(status__icontains=query) | Q(description__icontains=query))

            if latitude and longitude:
                latitude = float(latitude)
                longitude = float(longitude)
                # Approximate latitude degrees per kilometer
                min_latitude = latitude - (radius / 111)
                max_latitude = latitude + (radius / 111)
                # Approximate longitude degrees per kilometer
                min_longitude = longitude - \
                    (radius / (111 * abs(math.cos(math.radians(latitude)))))
                max_longitude = longitude + \
                    (radius / (111 * abs(math.cos(math.radians(latitude)))))

                # Filter the search within the bounding box of the coordinates
                billboards = billboards.filter(latitude__gte=min_latitude,
                                               latitude__lte=max_latitude,
                                               longitude__gte=min_longitude,
                                               longitude__lte=max_longitude)

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

            results = filtered_billboards.annotate(
                average_rating=Avg('ratings__rating')).values(
                'id',
                'latitude',
                'longitude',
                'width',
                'height',
                'image',
                'daily_rate_per_sq',
                'production',
                'status',
                'description',
                'average_rating'
            )

            for result in results:
                if result['average_rating']:
                    result['average_rating'] = float(result['average_rating'])
                else:
                    result['average_rating'] = 0.0

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                results, request)

            serialized_results = BillboardSearchSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])
        except Exception as e:
            print(e)
            return error_500(e)


class BillboardRating(generics.GenericAPIView):
    serializer_class = RatingGetSerializer

    def get(self, request, id):
        try:
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


class BillboardRecommendation(generics.GenericAPIView):
    serializer_class = BillboardSearchSerializer

    def get(self, request):
        try:
            billboards = Billboard.objects.filter(paid=True)
            results = billboards.annotate(
                average_rating=Avg('ratings__rating')).values(
                'id',
                'latitude',
                'longitude',
                'width',
                'height',
                'image',
                'daily_rate_per_sq',
                'production',
                'status',
                'description',
                'average_rating'
            )
            for result in results:
                if result['average_rating']:
                    result['average_rating'] = float(result['average_rating'])
                else:
                    result['average_rating'] = 0.0
                result['average_rating'] = result['average_rating'] or 0.0

            # Calculate the sum of all average_ratings
            sum_of_average_ratings = results.aggregate(
                sum_of_average_ratings=Sum('average_rating'))['sum_of_average_ratings']

            # Calculate the sum of all daily_rate_per_sq
            sum_of_daily_rate_per_sq = results.aggregate(
                sum_of_daily_rate_per_sq=Sum('daily_rate_per_sq'))['sum_of_daily_rate_per_sq']

            # Get the size of the results list
            size = len(results)

            # Calculate the average of average_ratings
            average_of_average_ratings = sum_of_average_ratings / size

            # Calculate the average of daily_rate_per_sq
            average_of_daily_rate_per_sq = sum_of_daily_rate_per_sq / size

            print(average_of_average_ratings, average_of_daily_rate_per_sq)

            result1 = [
                result for result in results if result['average_rating'] >= average_of_average_ratings
            ]
            result2 = [
                result for result in results if result['daily_rate_per_sq'] <= average_of_daily_rate_per_sq
            ]
            result12 = [
                result for result in results if
                (result['average_rating'] >= average_of_average_ratings and
                 result['daily_rate_per_sq'] <= average_of_daily_rate_per_sq)
            ]
            if result12:
                results = result12
            elif result2:
                results = result2
            else:
                results = result1

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                results, request)

            serialized_results = BillboardSearchSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500(e)
