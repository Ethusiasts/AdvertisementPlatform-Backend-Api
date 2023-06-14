from django.urls import path
from payment.views import PaymentInitialize, Payments

urlpatterns = [
    path('',
         Payments.as_view(), name='payments'),
    path('initialize',
         PaymentInitialize.as_view(), name='payment-intialize'),
]
