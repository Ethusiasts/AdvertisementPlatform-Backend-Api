from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_500, success_200, success_201, error_400, error_404, success_204
from proposal.models import Proposal
from rest_framework.pagination import PageNumberPagination

from proposal.serializers import ProposalSerializer
# Create your views here.


class Proposals(generics.GenericAPIView):
    serializer_class = ProposalSerializer

    def get(self, request):
        try:
            proposals = Proposal.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                proposals, request)

            serialized_results = self.serializer_class(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No proposals found', [])
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


class ProposalDetail(generics.GenericAPIView):
    serializer_class = ProposalSerializer

    def get_proposal(self, id):
        try:
            return Proposal.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        proposal = self.get_proposal(id)
        if proposal:
            return success_200('sucess', proposal)
        return error_404(f'Proposal with id: {id} not found.')

    def put(self, request, id):
        proposal = self.get_proposal(id)
        if proposal == None:
            return error_404(f'Proposal with id: {id} not found.')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', proposal)
        return error_400(serializer.errors)

    def delete(self, request, id):
        proposal = self.get_proposal(id)
        if proposal == None:
            return error_404(f'Proposal with id: {id} not found.')
        proposal.delete()
        return success_204()
