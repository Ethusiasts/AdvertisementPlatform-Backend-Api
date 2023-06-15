from decimal import Decimal
from django.shortcuts import render
from rest_framework import generics
from advertisement.models import Advertisement
from advertisement_platform.errors import error_500, success_200, success_201, error_400, error_404, success_204
from proposal.models import Proposal
from rest_framework.pagination import PageNumberPagination

from proposal.serializers import MultipleProposalSerializer, ProposalDetailSerializer, ProposalGetSerializer, ProposalPostSerializer
# Create your views here.


class Proposals(generics.GenericAPIView):
    serializer_class = ProposalPostSerializer

    def get(self, request):
        try:
            proposals = Proposal.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                proposals, request)

            serialized_results = ProposalGetSerializer(
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


class MultipleProposals(generics.GenericAPIView):
    serializer_class = MultipleProposalSerializer

    def post(self, request):
        try:
            medias_data = request.data.get("medias", [])
            proposal = {}
            advertisement = Advertisement.objects.get(
                id=request.data['advertisement_id'])
            for media_data in medias_data:
                if 'daily_rate_per_sq' in media_data:
                    width = advertisement.width
                    height = advertisement.height
                    daily_rate_per_sq = media_data.get('daily_rate_per_sq')
                    total_price = round(
                        width * height * Decimal(daily_rate_per_sq), 2)
                    proposal = {
                        "name": request.data['name'],
                        "user_id": request.data['user_id'],
                        "billboard_id": media_data.get('id'),
                        "media_agency_id": media_data.get('media_agency_id'),
                        "advertisement_id": request.data['advertisement_id'],
                        "description": request.data['description'],
                        "production": request.data['production'],
                        "total_price": total_price
                    }
                else:
                    duration = advertisement.duration_in_hour
                    normal = Decimal(media_data.get('normal'))
                    total_price = round(duration * 60 * normal, 2)
                    proposal = {
                        "name": request.data['name'],
                        "user_id": request.data['user_id'],
                        "agency_id": media_data.get('id'),
                        "media_agency_id": media_data.get('media_agency_id'),
                        "advertisement_id": request.data['advertisement_id'],
                        "description": request.data['description'],
                        "production": request.data['production'],
                        "total_price": total_price
                    }
                serializer = ProposalPostSerializer(data=proposal)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    return error_400(serializer.errors)
            return success_201('successfully created', '')

        except Exception as e:
            print(e)
            return error_400(e)


class ProposalDetail(generics.GenericAPIView):
    serializer_class = ProposalPostSerializer

    def get_proposal(self, id):
        try:
            return Proposal.objects.get(id=id)
        except:
            return None

    def get(self, request, id):
        try:
            proposal = Proposal.objects.select_related(
                'billboard_id').get(id=id)

            if proposal:
                serializer = ProposalDetailSerializer(proposal)
                return success_200('sucess', serializer.data)
            return error_404(f'Proposal with id: {id} not found.')
        except Exception as e:
            print(e)
            return error_500('internal server error')

    def put(self, request, id):
        proposal = self.get_proposal(id)
        if proposal == None:
            return error_404(f'Proposal with id: {id} not found.')

        serializer = self.serializer_class(
            proposal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        proposal = self.get_proposal(id)
        if proposal == None:
            return error_404(f'Proposal with id: {id} not found.')
        proposal.delete()
        return success_204()
