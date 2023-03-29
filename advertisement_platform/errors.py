from rest_framework.response import Response
from rest_framework import status


def success_200(message, data):
    return Response({
                    'status': 200,
                    'message': message,
                    'data': data
                    }, status=status.HTTP_200_OK)


def success_login_200(message, data):
    return Response({
                    'status': 200,
                    'message': message,
                    'token': data
                    }, status=status.HTTP_200_OK)


def success_201(message, data):
    return Response({
                    'status': 201,
                    'message': message,
                    'data': data
                    }, status=status.HTTP_201_CREATED)


def success_204():
    return Response({}, status=status.HTTP_204_NO_CONTENT)


def error_400(message):
    return Response({
                    'status': 400,
                    'message': message,
                    }, status=status.HTTP_400_BAD_REQUEST)


def error_401(message):
    return Response({
                    'status': 401,
                    'message': message,
                    }, status=status.HTTP_401_UNAUTHORIZED)


def error_403(message):
    return Response({
                    'status': 403,
                    'message': message,
                    }, status=status.HTTP_403_FORBIDDEN)


def error_404(message):
    return Response({
                    'status': 404,
                    'message': message,
                    }, status=status.HTTP_404_NOT_FOUND)


def error_500(message):
    return Response({
                    'status': 500,
                    'message': message,
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
