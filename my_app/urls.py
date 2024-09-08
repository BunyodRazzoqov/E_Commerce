from django.urls import path
from my_app import views

urlpatterns = [
    # path('books/', views.book_list, name='books'),
    # path('index/', views.index, name='index'),
    path('magic/', views.magic, name='magic'),
]
