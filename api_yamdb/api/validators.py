import re
from rest_framework import serializers
from reviews.models import User


def is_user_exist(value):
    if User.objects.filter(username=value):
        raise serializers.ValidationError(
            "Пользователь с таким username уже зарегистрирован"
        )


def is_email_exist(value):
    if User.objects.filter(email=value):
        raise serializers.ValidationError(
            "Пользователь с таким email уже зарегистрирован"
        )
    return value
    

def validate_username(value):
    if not re.match("^[A-Za-z0-9@._-]*$", value):
        raise serializers.ValidationError("Недопустимые символы в username")
    if len(value) > 150:
        raise serializers.ValidationError(
            "Длина username не может превышать 150 символов"
        )
    if value == "me":
        raise serializers.ValidationError("Имя 'me' недопустимо")
    return value
