import re
from rest_framework import serializers
from reviews.models import User


def validate_username(value):
    if len(User.objects.filter(username=value)) != 0:
        raise serializers.ValidationError(
            "Пользователь с таким username уже зарегистрирован"
        )
    if value == "me":
        raise serializers.ValidationError("Имя 'me' недопустимо")
    if len(value) > 150:
        raise serializers.ValidationError(
            "Длина username не может превышать 150 символов"
        )
    if not re.match("^[A-Za-z0-9@._-]*$", value):
        raise serializers.ValidationError("Недопустимые символы в username")
    return value


def validate_email(value):
    if len(User.objects.filter(email=value)) != 0:
        raise serializers.ValidationError(
            "Пользователь с таким email уже зарегистрирован"
        )
    return value
