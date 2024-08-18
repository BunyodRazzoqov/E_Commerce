from django import forms
from my_web.models import Customer


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
