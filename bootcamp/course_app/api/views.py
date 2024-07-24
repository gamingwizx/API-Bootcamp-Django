from django.shortcuts import render
from rest_framework import mixins,generics
from rest_framework import permissions as rest_permissions
from rest_framework import authentication as rest_authentication
from rest_framework.response import Response 
from course_app import models
from course_app.api import serializer
from bootcamp_table.api import (permissions, authentication)
# Create your views here.

class DestroyUpdateCourseVS(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = serializer.CourseSerializer
    queryset = models.Course.objects.all()
    authentication_classes = [rest_authentication.TokenAuthentication]
    permission_classes = [rest_permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        user = request.user.id
        request.data["user"] = user

        course = models.Course.objects.filter(id=self.kwargs["pk"])
        if (course.exists() is False):
            return Response({ "Success": False, "Error": "Course does not exist"})
        course = course.get(id=self.kwargs["pk"])

        if (course.user.id != user):
            return Response({ "Success": False, "Error": "Only owner can update this course"})

        course.delete()

        return Response({ "Success": True, "Error": "Course is deleted successfully"})

    def update(self, request, *args, **kwargs):
        user = request.user.id
        request.data["user"] = user

        course = models.Course.objects.filter(id=self.kwargs["pk"])
        if (course.exists() is False):
            return Response({ "Success": False, "Error": "Course does not exist"})
        course = course.get(id=self.kwargs["pk"])

        if (course.user.id != user):
            return Response({ "Success": False, "Error": "Only owner can update this course"})

        course_serializer = serializer.CourseSerializer(data=request.data)
        if(course_serializer.is_valid() is False):
            return Response({ "Success": False, "Error": course_serializer.errors})
        course_serializer.save()

        return Response({ "Success": True, "Course": course_serializer.data })

class GetCourseVS(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = serializer.CourseSerializer
    queryset = models.Course.objects.all()
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
class GetListCourseVS(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializer.CourseSerializer
    queryset = models.Course.objects.all()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class CreateCourseVS(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = serializer.CourseSerializer
    queryset = models.Course.objects.all()
    authentication_classes = [rest_authentication.TokenAuthentication]
    permission_classes = [rest_permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user.id
        request.data["user"] = user
        course_serializer = serializer.CourseSerializer(data=request.data)
        if(course_serializer.is_valid() is False):
            return Response({ "Success": False, "Error": course_serializer.errors})
        course_serializer.save()

        return Response({ "Success": True, "Course": course_serializer.data })