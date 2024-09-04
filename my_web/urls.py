from django.urls import path
from my_web.views import views

urlpatterns = [
    path('project-management/', views.project_management, name='project_management'),
    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('customer-details/<slug:customer_slug>/', views.CustomerDetailsView.as_view(), name='customer_details'),
    path('user-profile/', views.profile, name='profile'),
    path('user-settings/', views.profile_settings, name='profile_settings'),
    path('add-customer/', views.CustomerCreateView.as_view(), name='add_customer'),
    path('edit-customer/<slug:customer_slug>/', views.CustomerUpdateView.as_view(), name='edit_customer'),
    path('delete-customer/<slug:customer_slug>/', views.CustomerDeleteView.as_view(), name='delete_customer'),
    path('export-data/', views.ExportDataView.as_view(), name='export_data'),
]
