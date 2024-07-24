from django.db import models
from django.conf import settings
from django.db.models import Sum 
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import decorators
from rest_framework.authtoken.models import Token
from auth_app.models import User
from django_bleach.models import BleachField
    
class Bootcamp(models.Model):
    name = BleachField(max_length=50, unique=True)
    description = BleachField(max_length=250)
    website=  BleachField(max_length=500)
    phone = BleachField(max_length=50)
    email = BleachField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bootcamp_creator")
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    average_rating = models.FloatField(default=0)
    total_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        review = Review.objects.filter(bootcamp=self.id)
        if review.exists() == False:
            return 0
        else:
            sum = review.aggregate(Sum("rating"))["rating__sum"]
            total = Review.objects.filter(bootcamp=self).count()
            return round(sum/total, 2)
    
    def get_total_rating(self):
        return Review.objects.filter(bootcamp=self).count()

class Review(models.Model):
    title = models.CharField(max_length=50)
    text=models.CharField(max_length=255)
    rating=models.IntegerField()
    bootcamp=models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name="bootcamp_reviews")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")

    def __str__(self):
        return self.title      
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)    