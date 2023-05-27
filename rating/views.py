from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, success_200, success_201, success_204
from rating.models import Rating
from django.db.models import Q
from django.db.models import F
from rest_framework.parsers import MultiPartParser, FormParser
from rating.serializers import RatingSerializer
from django.db.models import Avg
# Create your views here.


# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()
# first image name to be displayed on the database then image name that you want it to be upload to firebase
# storage.child(".test1.jpg").put("./media/rating2.jpg")

# url = storage.child(".test1.jpg").get_url(None)
# print(url)


class Ratings(generics.GenericAPIView):
    serializer_class = RatingSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        try:
            ratings = Rating.objects.all()
            serializer = self.serializer_class(ratings, many=True)
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


class RatingDetail(generics.GenericAPIView):
    serializer_class = RatingSerializer
    parser_classes = (MultiPartParser,)

    def get_rating(self, id):
        try:
            return Rating.objects.get(id=id, many=True)
        except:
            return None

    def get(self, request, id):
        entity_type = request.GET.get('entity_type')
        try:
            if entity_type == 'Billboard':
                average_rating = Rating.objects.filter(
                    billboard_id=id, entity_type=entity_type).aggregate(Avg('rating'))['rating__avg']
            elif entity_type == 'Agency':
                average_rating = Rating.objects.filter(
                    agency_id=id, entity_type=entity_type).aggregate(Avg('rating'))['rating__avg']
            else:
                return error_404('Invalid entity type')

            response = {'average_rating': average_rating}

            return JsonResponse(response, status=200)
        except Exception as e:
            print(e)
            return error_404(f'Rating with id: {id} not found.')

    def put(self, request, id):
        rating = self.get_rating(id)
        if rating == None:
            return error_404(f'rating with id: {id} not found.')
        serializer = self.serializer_class(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        rating = self.get_rating(id)
        if rating == None:
            return error_404(f'Rating with id: {id} not found.')
        rating.delete()
        return success_204()
