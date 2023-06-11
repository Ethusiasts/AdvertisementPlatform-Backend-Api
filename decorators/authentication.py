# import jwt
# from django.conf import settings
# from functools import wraps
# from rest_framework.response import Response


# def validate_token(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

#         try:
#             decoded_token = jwt.decode(
#                 token, settings.SECRET_KEY, algorithms=['HS256'])
#             user_id = decoded_token.get('id')
#             user_role = decoded_token.get('role')

#             # Perform additional validation checks if required

#             # Set user and role in the request object for access in the view function
#             request.user_id = user_id
#             request.user_role = user_role

#             return view_func(request, *args, **kwargs)
#         except jwt.ExpiredSignatureError:
#             return Response('Token has expired', status=401)
#         except jwt.DecodeError:
#             return Response('Invalid token', status=401)
#         except Exception as e:
#             return Response(str(e), status=401)

#     return wrapper
