from django.contrib.auth import get_user_model
from auth_app import models
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class UserSerializer(serializers.ModelSerializer):

    repeat_password = serializers.CharField(style= {"type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', "role", "repeat_password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def update(self, instance, validated_data):
        return instance.update(validated_data)

    def save(self, *args):
        User = get_user_model()
        # Create
        if not args:
            if (len(self.validated_data) == 0): raise serializers.ValidationError({"Error": "Error when creating user"})
            password = self.validated_data['password']
            repeat_password = self.validated_data['repeat_password']
            email = self.validated_data['email']
            role = self.validated_data["role"]

            if (password != repeat_password):
                raise serializers.ValidationError({'password': 'Passwords do not match'})
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({'email': 'Email already exists'})
            
            user = User(username=self.validated_data["username"], email=email, role=role)
            user.set_password(password) 
            user.save()

            return user
        # Update
        if (args[0]["mode"].upper() == "SAVE"):
            get_user = self.context["request"].user
            get_user.set_password(self.context["request"].data["password"])
            get_user.save()
            return get_user



class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = "__all__"

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')