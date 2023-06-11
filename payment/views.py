from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse
from advertisement_platform.errors import error_404, error_500, success_201
from django.utils import timezone


from payment.serializers import PaymentSerializer


# Create your views here.
class Payments(generics.GenericAPIView):
    serializer_class = PaymentSerializer

    def post(self, request):

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                instance = serializer.create(validated_data)
                return success_201('successfully created', serializer.data)
            else:
                return error_404('page not found', serializer.errors)

        except Exception as e:
            print(e)
            return error_500(e)
