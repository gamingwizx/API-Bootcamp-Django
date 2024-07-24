from rest_framework import serializers
from bootcamp_table import models

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Review
        fields = "__all__"