from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_204
from billboard.models import Billboard
from billboard.serializers import BillboardGetSerializer, BillboardGetSerializer
from contract.models import Contract
from contract.serializers import ContractDetailSerializer, ContractSerializer
from media_agency.models import MediaAgency
from django.core.serializers import serialize
from rest_framework.pagination import PageNumberPagination
import json
from media_agency.serializers import MediaAgencyGetSerializer, MediaAgencyPostSerializer
from proposal.models import Proposal
from proposal.serializers import ProposalDetailSerializer, ProposalGetSerializer
# Create your views here.


class MediaAgencies(generics.GenericAPIView):
    serializer_class = MediaAgencyPostSerializer

    def get(self, request):
        try:
            media_agencies = MediaAgency.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                media_agencies, request)

            serialized_results = MediaAgencyGetSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No media agencies found', [])
        except Exception as e:
            print(e)
            return error_400(serialized_results.errors)

    def post(self, request):
        serializer = MediaAgencyPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        return error_400(serializer.errors)


class MediaAgencyDetail(generics.GenericAPIView):
    serializer_class = MediaAgencyPostSerializer

    def get_media_agency(self, id):
        try:
            return MediaAgency.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        media_agency = self.get_media_agency(id)
        if media_agency:
            serializer = MediaAgencyGetSerializer(media_agency)
            return success_200('', serializer.data)
        return error_404(f'MediaAgency with id: {id} not found.')

    def put(self, request, id):
        media_agency = self.get_media_agency(id)
        if media_agency == None:
            return error_404(f'media_agency with id: {id} not found.')
        serializer = MediaAgencyPostSerializer(media_agency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        media_agency = self.get_media_agency(id)
        if media_agency == None:
            return error_404(f'MediaAgency with id: {id} not found.')
        media_agency.delete()
        return success_204()


class MediaAgencyBillboards(generics.GenericAPIView):
    serializer_class = BillboardGetSerializer

    def get(self, request, id):
        try:
            billboards = Billboard.objects.filter(
                media_agency_id=id)
            serialized_results = billboards
            if billboards:
                serializer = self.serializer_class(billboards, many=True)
                paginator = PageNumberPagination()
                paginator.page_size = 6
                paginated_results = paginator.paginate_queryset(
                    billboards, request)

                serialized_results = self.serializer_class(
                    paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500('Something went wrong')


class MediaAgencyProposals(generics.GenericAPIView):
    serializer_class = ProposalDetailSerializer

    def get(self, request, id):
        try:
            proposals = Proposal.objects.filter(
                media_agency_id=id)
            serialized_results = proposals
            if proposals:
                # serializer = self.serializer_class(proposals, many=True)
                paginator = PageNumberPagination()
                paginator.page_size = 6
                paginated_results = paginator.paginate_queryset(
                    proposals, request)

                serialized_results = self.serializer_class(
                    paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500('Something went wrong')


class MediaAgencyContracts(generics.GenericAPIView):
    serializer_class = ContractDetailSerializer

    def get(self, request, id):
        try:
            contracts = Contract.objects.filter(
                media_agency_id=id)
            serialized_results = contracts
            if contracts:
                serializer = self.serializer_class(contracts, many=True)
                paginator = PageNumberPagination()
                paginator.page_size = 6
                paginated_results = paginator.paginate_queryset(
                    contracts, request)

                serialized_results = self.serializer_class(
                    paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500('Something went wrong')
