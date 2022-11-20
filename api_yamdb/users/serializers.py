from rest_framework import serializers

from reviews.models import User


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError(
                "Имя 'me' недопустимо - сериализатор"
            )
        return data

    class Meta:
        model = User
        fields = ["username", "email"]
