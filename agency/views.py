from decimal import Decimal
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_204
from agency.models import Agency
from django.db.models import Q, Sum, F, Case, When, Value, DecimalField, Avg
from django.db.models import F
from agency.serializers import AgencyPostSerializer, AgencyRatingSerializer, AgencySearchSerializer
from rest_framework.pagination import PageNumberPagination
from rating.models import Rating

from rating.serializers import RatingGetSerializer
# Create your views here.


class Agencies(generics.GenericAPIView):
    serializer_class = AgencyPostSerializer

    def get(self, request):
        try:
            agencies = Agency.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                agencies, request)

            serialized_results = AgencyRatingSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No agencies found', [])
        except Exception as e:
            print(e)
            return error_500('internal server error')

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_201('successfully created', serializer.data)
        except Exception as e:
            print(e)
            return error_400(e)


class AgencyDetail(generics.GenericAPIView):
    serializer_class = AgencyRatingSerializer

    def get_agency(self, id):
        try:
            return Agency.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        agency = self.get_agency(id)
        if agency:
            serializer = self.serializer_class(agency)
            return success_200('', serializer.data)
        return error_404(f'Agency with id: {id} not found.')

    def put(self, request, id):
        agency = self.get_agency(id)
        if agency == None:
            return error_404(f'agency with id: {id} not found.')
        serializer = AgencyPostSerializer(agency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        agency = self.get_agency(id)
        if agency == None:
            return error_404(f'Agency with id: {id} not found.')
        agency.delete()
        return success_204()


class SearchAgencies(generics.GenericAPIView):
    serializer_class = AgencyRatingSerializer

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
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            channel_name = request.GET.get('channel_name')
            conditions = {
                'production': request.GET.get('production', 'false'),
                'peak_hour': request.GET.get('peak_hour', 'false'),
                'normal': 'true',
            }

            agencies = Agency.objects.all()

            if query:
                agencies = agencies.filter(Q(channel_name__icontains=query) | Q(production__icontains=query) | Q(
                    normal__icontains=query) | Q(peak_hour__icontains=query))

            if channel_name:
                agencies = agencies.filter(
                    media_agency_id__user__role=channel_name)

            filtered_agencies = agencies

            if (min_price and max_price):
             # Generate dynamic annotation and filter based on conditions
                annotation, filter_condition = self.generate_annotation_and_filter(
                    conditions, min_price, max_price)
                filtered_agencies = agencies.annotate(
                    total_sum=annotation).filter(filter_condition)

            results = filtered_agencies.annotate(
                average_rating=Avg('ratings__rating')).values(
                'id',
                'image',
                'media_agency_id_id',
                'channel_name',
                'peak_hour',
                'normal',
                'production',
                'average_rating'
            )

            for result in results:
                if result['average_rating']:
                    result['average_rating'] = float(result['average_rating'])
                else:
                    result['average_rating'] = 0.0

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(results, request)

            serialized_results = AgencySearchSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])
        except Exception as e:
            print(e)
            return error_500(e)


class AgencyRecommendation(generics.GenericAPIView):
    serializer_class = AgencySearchSerializer

    def get(self, request):
        try:
            agencies = Agency.objects.all()
            results = agencies.annotate(
                average_rating=Avg('ratings__rating')).values(
                'id',
                'image',
                'media_agency_id_id',
                'channel_name',
                'peak_hour',
                'normal',
                'production',
                'average_rating'
            )
            for result in results:
                if result['average_rating']:
                    result['average_rating'] = float(result['average_rating'])
                else:
                    result['average_rating'] = 0.0
                result['average_rating'] = result['average_rating'] or 0.0
            print(results, 'results')
            # Calculate the sum of all average_ratings
            sum_of_average_ratings = results.aggregate(
                sum_of_average_ratings=Sum('average_rating'))['sum_of_average_ratings']
            print(sum_of_average_ratings, 'avg')

            # # Calculate the sum of all normal
            # sum_of_normal = results.aggregate(
            #     sum_of_normal=Sum('normal'))['sum_of_normal']
            # print(sum_of_normal, )

            # # Get the size of the results list
            # size = len(results)

            # # Calculate the average of average_ratings
            # average_of_average_ratings = sum_of_average_ratings / size

            # # Calculate the average of normal
            # average_of_normal = sum_of_normal / size

            # print(average_of_average_ratings, average_of_normal)

            # result1 = [
            #     result for result in results if result['average_rating'] >= average_of_average_ratings
            # ]
            # result2 = [
            #     result for result in results if result['normal'] <= average_of_normal
            # ]
            # result12 = [
            #     result for result in results if
            #     (result['average_rating'] >= average_of_average_ratings and
            #      result['normal'] <= average_of_normal)
            # ]
            # if result12:
            #     results = result12
            # elif result2:
            #     results = result2
            # else:
            #     results = result1

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                results, request)

            serialized_results = AgencySearchSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500(e)


class AgencyRating(generics.GenericAPIView):
    serializer_class = RatingGetSerializer

    def get(self, request, id):
        try:
            ratings = Rating.objects.filter(
                agency_id=id)
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
