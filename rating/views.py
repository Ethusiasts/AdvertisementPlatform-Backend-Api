from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import success_200, error_404, success_201, error_400, success_204
from rating.models import Rating

from rating.serializers import RatingSerializer
# Create your views here.


class Ratings(generics.GenericAPIView):
    serializer_class = RatingSerializer

    def get(self, request):
        ratings = Rating.objects.all()
        return success_200('sucess', ratings)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        print(serializer.errors)
        return error_400(serializer.errors)


class RatingDetail(generics.GenericAPIView):

    serializer_class = RatingSerializer

    def get_rating(self, id):
        try:
            return Rating.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        rating = self.get_rating(id)
        if rating:
            return success_200('sucess', rating)
        return error_404(f'Rating with id: {id} not found.')

    def put(self, request, id):
        rating = self.get_rating(id)
        if rating == None:
            return error_404(f'Rating with id: {id} not found.')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', rating)
        return error_400(serializer.errors)

    def delete(self, request, id):
        rating = self.get_rating(id)
        if rating == None:
            return error_404(f'Rating with id: {id} not found.')
        rating.delete()
        return success_204()
