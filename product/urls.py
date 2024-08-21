from django.urls import path

from product import views

urlpatterns = [
    path('product-list/', views.ProductListView.as_view(), name='product_list'),
    path('add-product/', views.ProductCreateView.as_view(), name='add_product'),
    path('edit-product/<slug:product_slug>/', views.ProductUpdateView.as_view(), name='edit_product'),
    path('delete-product/<slug:product_slug>/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('product-detail/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),

]
