from rest_framework import serializers
from bootcamp_table import models
from bootcamp_table.models import Review
from auth_app.models import User
class BootcampSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Bootcamp
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance