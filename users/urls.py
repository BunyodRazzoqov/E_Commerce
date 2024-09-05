from django.urls import path
from users import views

urlpatterns = [
    path('logout/', views.logout_page, name='logout_page'),
    path('login/', views.LoginPageView.as_view(), name='login_page'),
    path('register/', views.RegisterFormView.as_view(), name='register_page'),
    path('sending-mail/', views.SendEmailView.as_view(), name='sending_email'),
    path('success/', views.success, name='success'),
    path('activation-link/<uidb64>/<token>/', views.activate, name='activate'),
]
