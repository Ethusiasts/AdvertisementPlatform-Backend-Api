import datetime
from django import forms
from django.shortcuts import render
import jwt
from django.urls import reverse
from rest_framework.views import APIView
from advertisement.models import Advertisement
from advertisement.serializers import AdvertisementGetSerializer
from advertisement_platform import settings
from advertisement_platform.settings import PASSWORD_RESET_BASE_URL, SECRET_KEY
from advertisement_platform.errors import error_400, error_404, error_500, success_200, success_201, success_204, success_login_200
from contract.models import Contract
from contract.serializers import ContractDetailSerializer
from media_agency.models import MediaAgency
from proposal.models import Proposal
from proposal.serializers import ProposalDetailSerializer, ProposalGetSerializer
from user.forms import ResetPasswordForm
from advertisement_platform.helpers import send_email, valid_role
from user.models import User, UserProfile, user_reset_password_token
from user.serializers import ForgotPasswordSerializer, LoginSerializer, ResetPasswordSerializer, UserPostSerializer, UserProfileSerializer, UserGetSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.pagination import PageNumberPagination
from urllib.parse import urljoin


class SignUpAPI(generics.GenericAPIView):
    serializer_class = UserPostSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            print('inn')
            if serializer.is_valid():
                role = request.data['role']
                if valid_role(role):
                    kwargs = {'role': role}
                    user = User.objects.create_user(
                        request.data['email'], request.data['password'], **kwargs)
                    token = user_reset_password_token._create_token(user)
                    verification_link = settings.BASE_URL + \
                        reverse('activate', kwargs={'token': token})
                    send_email('Activate your user account',
                               'Please click the following link to activate your account', request.data['email'], verification_link)

                    return success_200(
                        'Account activation link has been sent to your email. Please go ahead and click the link to activate your account', serializer.data
                    )

                return error_400('unknown user role')
            return error_400(serializer.errors)

        except Exception as e:
            print(e)
            return error_500(e)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            firstTimeLogin = True
            serializer = self.serializer_class(data=request.data)
            has_profile = True
            if serializer.is_valid():
                email = request.data['email']
                password = request.data['password']
                user = authenticate(email=email, password=password)
                # Check if the user has a related profile

            if user is None:
                return error_400('email or password is incorrect')

            if not user.is_verified:
                return error_400('your account is not activated')

            if user.role == 'Customer':
                has_profile = UserProfile.objects.filter(user=user).exists()

            if (user.role == 'LANDOWNER' or user.role == 'TV' or user.role == 'RADIO'):
                has_profile = MediaAgency.objects.filter(user=user).exists()

            if has_profile:
                firstTimeLogin = False

            payload = ({
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
            })

            token = jwt.encode(payload, SECRET_KEY,
                               algorithm='HS256')

            return success_login_200(
                'You are successfully logged in.', token, firstTimeLogin
            )

        except Exception as e:
            print(e)
            return error_500('something went wrong')


class ActivateAccountView(APIView):
    def get(self, request, token):
        try:
            token_obj = Token.objects.get(key=token)
            user = User.objects.get(pk=token_obj.user_id)
            if user is not None and token:
                user.is_verified = True
                user.save()
                return success_200('Account successfully activated.', '')

            return error_400('user not found')

        except Exception as e:
            print(e)
            return error_400('bad request')


class ForgotPasswordAPI(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

                token = user_reset_password_token._create_token(user)
                reset_password_link = f'{PASSWORD_RESET_BASE_URL}/resetpassword/{token}'

                send_email('Reset Your Password',
                           'Please click the following link to reset your password', email, reset_password_link)
                return success_200(
                    'A link to reset your password has been sent to your email.', ''
                )
            return error_400('bad request')
        except Exception as e:
            print(e)
            return error_500(e)


class ResetPasswordAPI(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):

        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            if not token:
                return Response({'message': 'unauthenticated user'})

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data.get(
                    'new_password', '')
                try:
                    token_obj = Token.objects.get(key=token)

                except Token.DoesNotExist:
                    return error_400('Invalid token')

                user = User.objects.get(pk=token_obj.user_id)
                user.set_password(new_password)
                user.save()
                return success_200('password successfully updated', '')
            return error_400('bad request')

        except Exception as e:
            print(e)
            return error_500('internal server error')


class UserProfileAPI(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def get(self, request):
        try:
            billboards = UserProfile.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                billboards, request)

            serialized_results = UserProfileSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No profiles found', [])
        except Exception as e:
            print(e)
            return error_400(serialized_results.errors)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_201('successfully created', serializer.data)
        return error_400(serializer.errors)


class UserProfileDetailAPI(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, JSONParser)

    def get_user_profile(self, id):
        try:
            return UserProfile.objects.filter(user_id=id).first()
        except:
            return None

    def get(self, request, id):
        try:
            user_profile = self.get_user_profile(id)
            if user_profile:
                serializer = self.serializer_class(user_profile)
                return success_200('sucess', serializer.data)
            return error_404(f'Userprofile with id: {id} not found.')
        except Exception as e:
            print(e)
            return error_500('something went wrong')

    def put(self, request, id):
        user_profile = self.get_user_profile(id)
        if user_profile == None:
            return error_404(f"User with id: {id} doesn't have a profile.")
        serializer = self.serializer_class(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_200('sucess', serializer.data)
        return error_400(serializer.errors)

    def delete(self, request, id):
        try:
            userProfile = UserProfile.objects.get(id=id)
            if userProfile is None:
                return error_404(f'Billboard with id: {id} not found.')

            userProfile.delete()
            return success_204()
        except Exception as e:
            print(e)
            return Response({'message': 'something went wrong'})


# Code below is for test only.
class UserAPI(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        if not token:
            return Response({'message': 'unauthenticated user'})

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')

        except Exception as e:
            print(e)
            return Response({'message': 'something went wrong'})

        return Response(payload['id'])


class DeleteUser(APIView):
    def delete(self, request, id):
        if request.method == 'DELETE':
            try:
                user = User.objects.get(id=id)
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                print(e)
                return Response({'message': 'something went wrong'})


class GetUser(APIView):
    def get(self, request):
        try:
            users = User.objects.all()

            paginator = PageNumberPagination()
            paginator.page_size = 6
            paginated_results = paginator.paginate_queryset(
                users, request)

            serialized_results = UserGetSerializer(
                paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No users found', [])
        except Exception as e:
            print(e)
            return error_400(serialized_results.errors)


class UserAdvertisements(generics.GenericAPIView):
    serializer_class = AdvertisementGetSerializer

    def get(self, request, id):
        try:
            advertisements = Advertisement.objects.filter(
                user_id=id)
            serialized_results = advertisements
            if advertisements:
                serializer = self.serializer_class(advertisements, many=True)
                paginator = PageNumberPagination()
                paginator.page_size = 6
                paginated_results = paginator.paginate_queryset(
                    advertisements, request)

                serialized_results = self.serializer_class(
                    paginated_results, many=True).data

            if serialized_results:
                return paginator.get_paginated_response(serialized_results)
            else:
                return success_200('No results found', [])

        except Exception as e:
            print(e)
            return error_500('Something went wrong')


class UserProposals(generics.GenericAPIView):
    serializer_class = ProposalDetailSerializer

    def get(self, request, id):
        try:
            proposals = Proposal.objects.filter(
                user_id=id)
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


class UserContracts(generics.GenericAPIView):
    serializer_class = ContractDetailSerializer

    def get(self, request, id):
        try:
            contracts = Contract.objects.filter(
                user_id=id)
            serialized_results = contracts
            if contracts:
                # serializer = self.serializer_class(contracts, many=True)
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
