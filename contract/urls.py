from django.urls import path
from contract.views import ContractDetail, Contracts

urlpatterns = [
    path('', Contracts.as_view()),
    path('<int:id>', ContractDetail.as_view())
]
