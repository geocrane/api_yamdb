from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# class RegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)

#     class Meta:
#         model = User
#         fields = ["email", "username", "password", "token"]

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)
