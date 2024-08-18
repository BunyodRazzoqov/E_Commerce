from django.urls import path

from product import views

urlpatterns = [
    path('product-list/', views.product_list, name='product_list'),
]
