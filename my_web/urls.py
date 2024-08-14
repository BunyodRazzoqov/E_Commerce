from django.contrib import admin
from django.urls import path

from my_web.views import views
from my_web.views import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('project-management/', views.project_management, name='project_management'),
    path('customers/', views.customers, name='customers'),
    path('customer-details/<slug:customer_slug>/', views.customer_details, name='customer_details'),
    path('user-profile/', views.profile, name='profile'),
    path('user-settings/', views.profile_settings, name='profile_settings'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('edit-customer/<slug:customer_slug>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<slug:customer_slug>/', views.delete_customer, name='delete_customer'),

    #     Authentication
    path('logout/', auth.logout_page, name='logout_page'),
    path('login/', auth.login_page, name='login_page'),
    path('register/', auth.register_page, name='register_page'),
]
