from rest_framework import serializers

from reviews.models import User


class SignUpSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data.get("username") == "me":
            raise serializers.ValidationError(
                "Имя 'me' недопустимо"
            )
        return data

    class Meta:
        model = User
        fields = ["username", "email"]


class GetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username"]