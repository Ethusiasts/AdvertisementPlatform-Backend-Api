from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_500, success_200, success_201, error_400, error_404, success_204
from contract.models import Contract
from contract.serializers import ContractDetailSerializer, ContractGetSerializer, ContractPostSerializer
from rest_framework.pagination import PageNumberPagination


# Create your views here.


class Contracts(generics.GenericAPIView):
    serializer_class = ContractPostSerializer

    def get(self, request):
        try:
            contracts = Contract.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                contracts, request)

            serialized_results = ContractGetSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No contracts found', [])
        except Exception as e:
            print(e)
            return error_400(serialized_results.errors)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        print(serializer.errors)
        return error_400(serializer.errors)


class ContractDetail(generics.GenericAPIView):

    serializer_class = ContractPostSerializer

    def get_contract(self, id):
        try:
            return Contract.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        try:
            contract = self.get_contract(id)
            if contract:
                serializer = ContractDetailSerializer(contract)
                return success_200('sucess', serializer.data)
            return error_404(f'Contract with id: {id} not found.')
        except Exception as e:
            print(e)
            return error_500('internal server error')

    def put(self, request, id):
        try:
            contract = self.get_contract(id)
            if contract == None:
                return error_404(f'Contract with id: {id} not found.')
            serializer = self.serializer_class(contract, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_200('sucess', serializer.data)
            return error_400(serializer.errors)
        except Exception as e:
            print(e)
            return error_500('internal server error')

    def delete(self, request, id):
        contract = self.get_contract(id)
        if contract == None:
            return error_404(f'Contract with id: {id} not found.')
        contract.delete()
        return success_204()
