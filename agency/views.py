from decimal import Decimal
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, success_200, success_201, success_204
from agency.models import Agency
from django.db.models import Q
from django.db.models import F
from agency.serializers import AgencySerializer
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class Agencies(generics.GenericAPIView):
    serializer_class = AgencySerializer

    def get(self, request):
        try:
            agencies = Agency.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                agencies, request)

            serialized_results = self.serializer_class(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No agencies found', [])
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
            serializer = self.serializer_class(agency)
            return success_200('', serializer.data)
        return error_404(f'Agency with id: {id} not found.')

    def put(self, request, id):
        agency = self.get_agency(id)
        if agency == None:
            return error_404(f'agency with id: {id} not found.')
        serializer = self.serializer_class(agency, data=request.data)
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


# class SearchAgencies(generics.GenericAPIView):
#     serializer_class = AgencySerializer

#     def get(self, request):
#         try:
#             query = request.GET.get('q')
#             location_filter = request.GET.get('location')
#             has_production = request.GET.get('has_production')
#             min_price = request.GET.get('min_price')
#             max_price = request.GET.get('max_price')
#             size_filter = request.GET.get('size')
#             agencies = Agency.objects.all()
#             if query:
#                 agencies = agencies.filter(Q(location__icontains=query) | Q(width__icontains=query) | Q(
#                     height__icontains=query) | Q(monthly_rate_per_sq__icontains=query))

#             if location_filter:
#                 agencies = agencies.filter(
#                     location__icontains=location_filter)
#             if has_production:
#                 has_production = has_production.lower() == 'true'
#                 agencies = agencies.filter(production=has_production)
#             if min_price:
#                 min_price = Decimal(min_price)
#                 agencies = agencies.filter(
#                     monthly_rate_per_sq__gte=min_price)
#             if max_price:
#                 max_price = Decimal(max_price)
#                 agencies = agencies.filter(
#                     monthly_rate_per_sq__lte=max_price)
#             if size_filter:
#                 size_filter = int(size_filter)
#                 agencies = agencies.annotate(
#                     area=F('width') * F('height')).filter(area__lte=size_filter)

#             results = agencies.values(
#                 'location',
#                 'width',
#                 'height',
#                 'rate',
#                 'image',
#                 'monthly_rate_per_sq',
#                 'production'
#             )

#             paginator = PageNumberPagination()
#             paginator.page_size = 6
#             paginated_results = paginator.paginate_queryset(results, request)

#             serialized_results = self.serializer_class(
#                 paginated_results, many=True).data

#             if serialized_results:
#                 return paginator.get_paginated_response(serialized_results)
#             else:
#                 return success_200('No results found', [])
#         except Exception as e:
#             print(e)
#             return error_404('Page not found.')
