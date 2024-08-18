from django.urls import path
from users import views

urlpatterns = [
    path('logout/', views.logout_page, name='logout_page'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
]
