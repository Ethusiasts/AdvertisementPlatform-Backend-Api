from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_204
from agency.models import Agency
from agency.serializers import AgencyPostSerializer
from billboard.models import Billboard
from billboard.serializers import BillboardGetSerializer, BillboardGetSerializer
from contract.models import Contract
from contract.serializers import ContractDetailSerializer
from media_agency.models import MediaAgency
from django.core.serializers import serialize
from rest_framework.pagination import PageNumberPagination
import json
from media_agency.serializers import MediaAgencyGetSerializer, MediaAgencyPostSerializer, MediaAgencyStatsSerializer
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
        serializer = MediaAgencyPostSerializer(
            media_agency, data=request.data, partial=True)
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
                media_agency_id=id).order_by('-created_at')
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
            return error_500(e)


class MediaAgencyAgencies(generics.GenericAPIView):
    serializer_class = AgencyPostSerializer

    def get(self, request, id):
        try:
            agencies = Agency.objects.filter(
                media_agency_id=id).order_by('-created_at')
            serialized_results = agencies
            if agencies:
                serializer = self.serializer_class(agencies, many=True)
                paginator = PageNumberPagination()
                paginator.page_size = 6
                paginated_results = paginator.paginate_queryset(
                    agencies, request)

                serialized_results = self.serializer_class(
                    paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500(e)


class MediaAgencyProposals(generics.GenericAPIView):
    serializer_class = ProposalDetailSerializer

    def get(self, request, id):
        try:
            proposals = Proposal.objects.filter(
                media_agency_id=id).order_by('-created_at')
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
                media_agency_id=id).order_by('-created_at')
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


class MediaAgencyStats(generics.GenericAPIView):
    serializer_class = MediaAgencyStatsSerializer

    def get(self, request, id):
        try:
            contracts = Contract.objects.filter(
                media_agency_id=id)
            proposals = Proposal.objects.filter(
                media_agency_id=id)
            billboards = Billboard.objects.filter(
                media_agency_id=id)

            total_contracts = contracts.count()
            total_proposals = proposals.count()
            total_billboards = billboards.count()
            print(total_billboards)

            data = {
                'total_contracts': total_contracts,
                'total_proposals': total_proposals,
                'total_billboards': total_billboards,
            }

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                return success_200('MediaAgency statistics retrieved successfully', serializer.data)
            return error_400(serializer.errors)

        except Exception as e:
            print(e)
            return error_500(e)
