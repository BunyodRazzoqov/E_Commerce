from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from product.models import Product, ProductAttribute


# Create your views here.


def product_list(request):
    products = Product.objects.all()
    product_attributes = ProductAttribute.objects.all()
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': page_obj,
               'attributes': product_attributes}
    return render(request, 'product/product-list.html', context)