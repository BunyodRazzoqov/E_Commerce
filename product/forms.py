from django import forms
from product.models import Product, Category


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'