import datetime as dt
import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

FORBIDDEN_NAME = "me"


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError(
            f"Проверьте год! Должен быть меньше {dt.date.today().year}"
        )
    return value


def validate_username(value):
    forbidden_symbols = re.findall(r"[^-\w]+", value)
    if forbidden_symbols:
        cleared_forbidden = "".join(
            set("".join(str(symbols) for symbols in forbidden_symbols))
        )
        raise serializers.ValidationError(
            f"Недопустимые символы в username: {cleared_forbidden} "
        )
    if value == FORBIDDEN_NAME:
        raise serializers.ValidationError(f"Имя '{value}' недопустимо")
    return value
