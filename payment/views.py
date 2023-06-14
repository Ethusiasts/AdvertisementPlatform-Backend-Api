from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse
from advertisement_platform.errors import error_400, error_404, error_500, success_201
from django.utils import timezone
import requests


from payment.serializers import PaymentIntilizeSerializer, PaymentSerializer


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
                return error_400(serializer.errors)

        except Exception as e:
            print(e)
            return error_500(e)


class PaymentInitialize(generics.GenericAPIView):
    serializer_class = PaymentIntilizeSerializer

    def post(self, request):

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                url = 'https://api.chapa.co/v1/transaction/initialize'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer CHASECK_TEST-odEJX60r1yQdEuJ7Z9roYGKj8uZMEhGp',
                }
                # data = {
                #     "first_name": "tolosa",
                #     "last_name": "mitiku",
                #     "email": "se.tolosa.mitiku@gmail.com",
                #     "phone_number": "0936490437",
                #     "tx_ref": "1-4-bnngsdfsdbm89bsdf",
                #     "amount": "150",
                #     "currency": "ETB",
                #     "callback_url": "https://advertisementplatform-0xpy.onrender.com/api/v1/payments/"
                # }

                response = requests.post(
                    url, headers=headers, json=request.data)
                if response.status_code == 200:
                    # Request succeeded, process the response
                    json_response = response.json()
                    checkout_url = json_response["data"]["checkout_url"]
                    # Handle the response data
                    return success_201('successfully created', checkout_url)
                else:
                    # Request failed, handle the error
                    error_message = response.text
                    # Handle the error message
                    return error_404(error_message)

            else:
                return error_400(serializer.errors)

        except Exception as e:
            print(e)
            return error_500(e)
