from django.db import models
from bootcamp_table.models import Bootcamp
from auth_app.models import User

class Course(models.Model):
    title=models.CharField(max_length=255, unique=True)
    description=models.CharField(max_length=255)
    weeks=models.CharField(max_length=255) 
    tuition=models.FloatField() 
    minimumSkill=models.CharField(max_length=255) 
    scholarhipsAvailable=models.BooleanField(default=False) 
    bootcamp=models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name="bootcamp_course")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_creator") 

    def __str__(self):
        return self.title