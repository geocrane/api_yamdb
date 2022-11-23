import datetime as dt
import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

FORBIDDEN_NAME = "me"


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError("Проверьте год!")
    return value


def validate_username(value):
    forbidden_symbols = re.findall("[^a-zA-Z0-9.@-_]+", value)
    if forbidden_symbols:
        raise serializers.ValidationError(
            f'В username присутствуют недопустимые символы: '
            f'{"".join(str(symbols) for symbols in forbidden_symbols)}'
        )
    if value == FORBIDDEN_NAME:
        raise serializers.ValidationError(f"Имя '{value}' недопустимо")
    return value
