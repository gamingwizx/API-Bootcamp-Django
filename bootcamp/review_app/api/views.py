from django.shortcuts import render
from rest_framework import (authentication, permissions, generics, mixins)
from rest_framework.response import Response
from review_app.api import serializer
from bootcamp_table import models

# Create your views here.
class DestroyUpdateReviewAV(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = serializer.ReviewSerializer
    queryset = models.Review.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        Review = models.Review.objects.filter(id=self.kwargs['pk'])
        if (Review.exists() == False):
            return Response({"error": "Review not found!"}, status=404)
        
        Review = Review.get(id=self.kwargs['pk'])

        if (Review.user.id != request.user.id and request.user.role.upper() != "ADMIN"):
            return Response({"error": "Only Admin or Owner can update Review!"}, status=403)
        
        request.data["user"] = request.user.id
        bc_serializer = serializer.ReviewSerializer(data=request.data)
        if(bc_serializer.is_valid() is False):
            return Response({"Error": bc_serializer.errors})
        
        bc_serializer.save()
        return Response({ "data": bc_serializer.data})
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        Review = models.Review.objects.filter(id=self.kwargs['pk'])
        if (Review.exists() == False):
            return Response({"error": "Review not found!"}, status=404)
        
        Review = Review.get(id=self.kwargs['pk'])

        if (Review.user.id != request.user.id):
            return Response({"error": "Only Admin or Owner can update Review!"}, status=403)
        
        Review.delete()

        return Response({ "Success": True, "Message": "Successfully deleted!"})

class CreateReviewAV(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = serializer.ReviewSerializer
    queryset = models.Review.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):

        if (request.user.role.upper() != "USER" and request.user.role.upper() != "ADMIN"):
            return Response({"error": "Only User or Admin can add Review!"}, status=403)

        Review = models.Review.objects.filter(user__email=request.user.email)    
        if (Review is not None and Review.exists()):
            return Response({"error": "User can only publish one Review!"}, status=403)

        request.data["user"] = request.user.id
        return self.create(request, *args, **kwargs)

class ListReviewAV(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializer.ReviewSerializer
    queryset = models.Review.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class GetReviewAV(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = serializer.ReviewSerializer
    queryset = models.Review.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)