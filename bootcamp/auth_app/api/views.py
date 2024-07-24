from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from rest_framework import (generics, permissions, status, mixins, viewsets)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from auth_app.api import serializer
from bootcamp_table.api.permissions import CustomPermission 
from auth_app import models
from django.conf import settings

class UserRegistrationJWT(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer

    def post(self, request, *args, **kwargs):
        response = Response()
        User = get_user_model()
        user_serializer=  self.serializer_class(data=request.data)
        if (user_serializer.is_valid()):
            user_serializer.save()
        else:
            response.error = user_serializer.errors
            return Response({"Success": False, "Error": response.error})


        user = User.objects.get(email=request.data["email"])

        token = get_token(user)
        response.data = user_serializer.data
        response.token = token

        return Response({"Success": True, "data": response.data, "token": response.token})

# Create your views here.
class UserRegistration(generics.CreateAPIView): 
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer

    def post(self, request, *args, **kwargs):
        response = Response()
        user_serializer = serializer.UserSerializer(data=request.data)
        user_serializer.is_valid()
        user_serializer.save()
        data = {}        
        token = Token.objects.get(user__username=request.data["username"]).key
        data["username"] = request.data["username"]
        data["email"] = request.data["email"]
        data["token"] = token
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=token,
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.data = {"Success": True, "data": data}
        
        return response
    
class UserList(generics.ListAPIView):
    User = get_user_model()
    serializer_class = serializer.UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class CreateRole(generics.CreateAPIView):
    serializer_class = serializer.RoleSerializer
    queryset = models.Role.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        response = Response()
        user = request.data["username"]
        password = request.data["password"]
        

        user = authenticate(username=user, password=password)

        if (user is not None):
            token = get_token(user)
            response.set_cookie(
                key = settings.SIMPLE_JWT["AUTH_COOKIE"],
                value = token["access"],
                expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            
            response.data = { "Success": True, "data": token}

            return response
        else:
            return Response({ "Success": False, "message": "User do not exist"})

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = serializer.LogoutSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        response = Response()
        response.delete_cookie("access_token")
        response.data = { "Success": True, }
        return response

class getCurrentUsersView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        response = Response()
        user = request.user.username
        email = request.user.email

        data = {
            "username": user,
            "email": email
        }
        response.data = { "Success": True, "data": data}
        return response
    
from django.utils.http import urlsafe_base64_decode    
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

import datetime

class RequestResetPasswordView(mixins.CreateModelMixin, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        User = get_user_model()
        email = request.data["email"]
        user = User.objects.get(email=email)

        reset_password_token = default_token_generator.make_token(user) 

        subject = "Request Password Reset"
        c = {
            "email": email,
            "uid": force_bytes(user.id),
            "token": reset_password_token,
            "user": user,
            'protocol': 'http',
            "root_url": request.resolver_match,
            "current_path": get_current_path(request) + "/reset-password"
        }
        email_template = render_to_string("test.html", c)

        try:
            send_mail(subject,email_template, settings.EMAIL_HOST_USER, html_message=email_template, recipient_list=[email], fail_silently=False)
            user.reset_password_token = reset_password_token
            user.reset_password_expiry = datetime.datetime.now() + datetime.timedelta(minutes=30)
            user.save()
            
            return Response({"Success": True, "Message": "Reset Password Email successfully sent."})
        except BadHeaderError:
            return Response({ "Success": False, "error": "Invalid header"})

class ResetPasswordView(mixins.CreateModelMixin, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        # Check the reset password token from the user table, check for the expiry ddate
        # then update the password based on the password passed from the body itself
        User = get_user_model()
        token = self.kwargs["token"]
        user = User.objects.get(reset_password_token=token)

        now = timezone.now()

        if (user.reset_password_expiry < now):
            return Response({ "Success": False, "Message": "Token has expired." })

        if (request.data["password"] != request.data["repeat_password"]):
            return Response({ "Success": False, "Message": "Passwords do not match." })

        user.set_password(request.data["password"])
        user.reset_password_token = None
        user.reset_password_expiry = None
        user.save()

        return Response({"Success": True, "Message": "Password reset successfully."})

class AdminOperationUserView(viewsets.ModelViewSet, generics.GenericAPIView):
    User = get_user_model()
    serializer_class = serializer.UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, CustomPermission]
    

class UpdateUserInfoView(mixins.UpdateModelMixin, generics.GenericAPIView):
    User = get_user_model()
    serializer_class = serializer.UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # get users information, and set it
        user = request.user
        User = get_user_model()
        # user = request.user
        u = User.objects.get(username=user.username)

        user_data = {
            "email": user.email,
            "password": request.data["password"],
            "repeat_password": request.data["repeat_password"],
            "role": user.role.id,
        }    

        user_serializer = self.get_serializer(u, data=user_data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save({"mode": "Save"})
        return Response({"Success": True, "Message": "User password changed successfully."})
        # self.perform_update(user_serializer)
        # return Response({"Success": True, "Message": "User information updated successfully."})

def homepage(request):
    return render(request, 'test.html')

def test_security(request):
    pre_url = get_previous_path(request)
    a = request.META.get('HTTP_REFERER', '/')
        
    return render(request, 'test_security.html', pre_url)

def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

def get_current_path(request):
    url = request.build_absolute_uri()
    current_request = url.split("/")[-1]
    base_url = url.replace(current_request, "") 
    return {
        'current_path': base_url
    }

def get_previous_path(request):
    current_path = get_current_path(request)["current_path"]
    previous_path = current_path.split("/")[-2]
    previous_directory = current_path.replace(previous_path, "")
    previous_directory = previous_directory[:-1]
    return {
        'previous_path': previous_directory
    } 