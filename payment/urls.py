from django.urls import path
from payment.views import Payments

urlpatterns = [
    path('', Payments.as_view(), name='payments'),
]
