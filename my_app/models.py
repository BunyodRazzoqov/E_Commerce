from django.db import models


# Create your models here.


# Book , Author

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} by {self.author}'
