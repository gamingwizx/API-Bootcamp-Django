from django.shortcuts import render
from rest_framework import (generics, viewsets, filters, authentication, permissions, mixins, views)
from rest_framework.response import Response
from bootcamp_table.api import (serializer, pagination)
from bootcamp_table.api.permissions import CustomPermission, IsOwner
from bootcamp_table import models
from auth_app.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.http import urlsafe_base64_encode

PUBLISHER_ID = 1
ADMIN_ID = 2
USER_ID = 3

class DestroyUpdateBootcampAV(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = serializer.BootcampSerializer
    queryset = models.Bootcamp.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, CustomPermission]

    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        bootcamp = models.Bootcamp.objects.filter(id=self.kwargs['pk'])
        if (bootcamp.exists() == False):
            return Response({"error": "Bootcamp not found!"}, status=404)
        bootcamp = self.get_object()
        
        request.data["user"] = request.user.id
        bc_serializer = serializer.BootcampSerializer(bootcamp, data=request.data)
        if(bc_serializer.is_valid() is False):
            return Response({"Error": bc_serializer.errors})

        bc_serializer.save()
        return Response({ "data": bc_serializer.data})
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        bootcamp = models.Bootcamp.objects.filter(id=self.kwargs['pk'])
        if (bootcamp.exists() == False):
            return Response({"error": "Bootcamp not found!"}, status=404)
        
        bootcamp = self.get_object()

        if (bootcamp.user.id != request.user.id):
            return Response({"error": "Only Admin or Owner can update bootcamp!"}, status=403)
        
        bootcamp.delete()

        return Response({ "Success": True, "Message": "Successfully deleted!"})

class CreateBootcampAV(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = serializer.BootcampSerializer
    queryset = models.Bootcamp.objects.all()
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # bootcamp = models.Bootcamp.objects.filter(user__email=request.user.email)  

        # request.data["email"] = request.user.email 
        if (request.user.role == ADMIN_ID): 
            request.data["user"] = request.user.id
            return self.create(request, *args, **kwargs)

        # if (bootcamp is not None and bootcamp.exists() and request.user.role != ADMIN_ID):
        #     return Response({"error": "Publisher can only publish one bootcamp!"}, status=403)

        # request.data.update({
        #     "name": urlsafe_base64_encode(str(request.data["name"]).encode("utf-8")),
        #     "description": urlsafe_base64_encode(str(request.data["description"]).encode("utf-8"))
        # })
        # request.data["user"] = request.user.id
        return self.create(request, *args, **kwargs)

class ListBootcampAV(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializer.BootcampSerializer
    queryset = models.Bootcamp.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class GetBootcampAV(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = serializer.BootcampSerializer
    queryset = models.Bootcamp.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class DestroyUpdateReviewAV(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = serializer.ReviewSerializer
    queryset = models.Review.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        review_filter = models.Review.objects.filter(bootcamp=self.kwargs['pk'], user=self.request.user.id)
        if (review_filter.exists() == False):
            return Response({"error": "Review not found!"}, status=404)
        review = models.Review.objects.get(bootcamp=self.kwargs['pk'], user=self.request.user.id)
        request.data["user"] = request.user.id
        request.data["bootcamp"] = self.kwargs['pk']
        bc_serializer = serializer.ReviewSerializer(review, data=request.data)
        if(bc_serializer.is_valid() is False):
            return Response({"Error": bc_serializer.errors})

        bootcamp = models.Bootcamp.objects.get(id=self.kwargs["pk"])
        average = bootcamp.get_average_rating()
        total = bootcamp.get_total_rating()

        bootcamp_data = {
            "name": bootcamp.name,
            "description": bootcamp.description,
            "website": bootcamp.website,
            "phone": bootcamp.phone,
            "email": request.user.email,
            "user": bootcamp.user.id,
            "average_rating": average,
            "total_rating": total
        }
        bc_serializer = serializer.BootcampSerializer(bootcamp, data=bootcamp_data)
        if (bc_serializer.is_valid() is False):
            return Response({"Success": True, "Error": bc_serializer.errors})
        bc_serializer.save()

        return Response({ "data": bc_serializer.data})
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        review = models.Review.objects.filter(bootcamp=self.kwargs['pk'], user=request.user.id)
        if (review.exists() == False):
            return Response({"error": "Review not found!"}, status=404)
        
        bootcamp = models.Bootcamp.objects.get(id=self.kwargs['pk'])

        average = bootcamp.get_average_rating()
        total = bootcamp.get_total_rating()

        bootcamp_data = {
            "name": bootcamp.name,
            "description": bootcamp.description,
            "website": bootcamp.website,
            "phone": bootcamp.phone,
            "email": request.user.email,
            "user": bootcamp.user.id,
            "average_rating": average,
            "total_rating": total
        }
        bc_serializer = serializer.BootcampSerializer(bootcamp, data=bootcamp_data)
        if (bc_serializer.is_valid() is False):
            return Response({"Success": True, "Error": bc_serializer.errors})
        bc_serializer.save()
        
        review.delete()

        return Response({ "Success": True, "Message": "Successfully deleted!"})

class CreateReviewAV(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = serializer.ReviewSerializer
    queryset = models.Review.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, CustomPermission]
    
    def post(self, request, *args, **kwargs):


        review = models.Review.objects.filter(bootcamp=self.kwargs["pk"], user__email=request.user.email)    
        # if (review is not None and review.exists()):
        #     return Response({"error": "User can only publish one Review!"}, status=403)

        request.data["user"] = request.user.id
        return self.create(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        bootcamp_id = self.kwargs["pk"]
        request.data["bootcamp"] = bootcamp_id
        

        review_serializer = serializer.ReviewSerializer(data=request.data)
        if (review_serializer.is_valid() is False):
            return Response({"Success":False, "Error": review_serializer.errors})

        # bootcamp_updated_data = {}
        bootcamp = models.Bootcamp.objects.get(id=bootcamp_id)
        
        average = bootcamp.get_average_rating()
        total = bootcamp.get_total_rating()

        bootcamp_updated_data = {
            "name": bootcamp.name,
            "description": bootcamp.description,
            "website": bootcamp.website,
            "phone": bootcamp.phone,
            "email": request.user.email,
            "user": bootcamp.user.id,
            "average_rating": average,
            "total_rating": total
        }

        bootcamp_serializer = serializer.BootcampSerializer(bootcamp, data=bootcamp_updated_data)
        if (bootcamp_serializer.is_valid() is False):
            return Response({"Success":False, "Error": bootcamp_serializer.errors})

        bootcamp_serializer.save()
        review_serializer.save()

        return Response({"Success": True, "Message": "Review created successfully!"})

class ListReviewAV(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = serializer.ReviewSerializer
    queryset = models.Review.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        reviews = models.Review.objects.filter(bootcamp=self.kwargs["pk"])
        if (reviews.exists() is False):
            return Response({"Success": False, "Error": "Bootcamp does not have any reviews"})
    
        reviews = reviews.values()
        return Response({"Success": True, "Reviews": reviews})

class GetReviewAV(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = serializer.ReviewSerializer
    queryset = models.Review.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)