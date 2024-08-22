from django import forms
from django.core.validators import validate_email


class MultiEmailField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        super().validate(value)
        for email in value:
            validate_email(email)
