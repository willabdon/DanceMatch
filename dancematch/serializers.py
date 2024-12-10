from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Dancer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class DancerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
        
    class Meta:
        model = Dancer
        fields = ("id", "user", "location", "level")

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        dancer = Dancer.objects.create(user=user, **validated_data)
        return dancer
