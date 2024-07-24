from rest_framework import serializers
from course_app import models
class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Course
        fields = "__all__"