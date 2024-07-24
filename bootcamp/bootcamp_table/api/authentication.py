from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework import HTTP_HEADER_ENCODING, exceptions

# class CreateUpdateDeleteAuthorize(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         auth = request.META.get('HTTP_AUTHORIZATION', b'')
#         token = auth[6:]

#         return (request.user, token)
        
    