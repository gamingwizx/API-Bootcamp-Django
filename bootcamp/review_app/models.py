# from django.db import models
# from django.db.models import Sum
# from auth_app.models import User
# from bootcamp_table.models import Bootcamp
# Create your models here.
# class Review(models.Model):
#     title = models.CharField(max_length=50)
#     text=models.CharField(max_length=255)
#     rating=models.IntegerField()
#     bootcamp=models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name="bootcamp_reviews")
#     user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")

#     def __str__(self):
#         return self.title  
    
    # def calculate_average_rating(self):
    #     count = Review.objects.count()
    #     total = Review.objects.aggregate(Sum("rating", default=1))["rating__sum"] 
    #     return round(total / count, 2) 
    
    # def calculate_total_rating(self):
    #     return Review.objects.count()