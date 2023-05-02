from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import success_200, success_201, error_400, error_404, success_204
from contract.models import Contract
from contract.serializers import ContractSerializer
# Create your views here.


class Contracts(generics.GenericAPIView):
    serializer_class = ContractSerializer

    def get(self, request):
        contracts = Contract.objects.all()
        return success_200('sucess', contracts)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        print(serializer.errors)
        return error_400(serializer.errors)


class ContractDetail(generics.GenericAPIView):

    serializer_class = ContractSerializer

    def get_contract(self, id):
        try:
            return Contract.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        contract = self.get_contract(id)
        if contract:
            return success_200('sucess', contract)
        return error_404(f'Contract with id: {id} not found.')

    def put(self, request, id):
        contract = self.get_contract(id)
        if contract == None:
            return error_404(f'Contract with id: {id} not found.')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', contract)
        return error_400(serializer.errors)

    def delete(self, request, id):
        contract = self.get_contract(id)
        if contract == None:
            return error_404(f'Contract with id: {id} not found.')
        contract.delete()
        return success_204()
