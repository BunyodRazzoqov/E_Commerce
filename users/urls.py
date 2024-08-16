from django.contrib import admin
from django.urls import path

from my_web.views import views
from my_web.views import auth

urlpatterns = [
    path('admin/', admin.site.urls),
]
