from django.contrib import admin

from my_app.models import Author, Book

# Register your models here.


admin.site.register(Author)
admin.site.register(Book)
