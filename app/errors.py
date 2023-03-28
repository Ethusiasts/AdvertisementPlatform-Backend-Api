from rest_framework.response import Response
from rest_framework import status


def sucess_200(message, data):
    return Response({
                    'status': 200,
                    'message': message,
                    'data': data
                    }, status=status.HTTP_200_BAD_REQUEST)


def sucess_login_200(message, data):
    return Response({
                    'status': 200,
                    'message': message,
                    'token': data
                    }, status=status.HTTP_200_BAD_REQUEST)


def sucess_201(message, data):
    return Response({
                    'status': 201,
                    'message': message,
                    'data': data
                    }, status=status.HTTP_201_BAD_REQUEST)


def sucess_204():
    return Response({}, status=status.HTTP_204_BAD_REQUEST)


def error_400(message):
    return Response({
                    'status': 400,
                    'message': message,
                    }, status=status.HTTP_400_BAD_REQUEST)


def error_401(message):
    return Response({
                    'status': 401,
                    'message': message,
                    }, status=status.HTTP_401_BAD_REQUEST)


def error_403(message):
    return Response({
                    'status': 403,
                    'message': message,
                    }, status=status.HTTP_403_BAD_REQUEST)


def error_404(message):
    return Response({
                    'status': 404,
                    'message': message,
                    }, status=status.HTTP_404_BAD_REQUEST)


def error_500(message):
    return Response({
                    'status': 400,
                    'message': message,
                    }, status=status.HTTP_500_BAD_REQUEST)
