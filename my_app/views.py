from django.shortcuts import render
from django.db.models import Min, Max, Avg, Count, Sum

from my_app.models import Author, Book


# Create your views here.


# def index(request):
#     # authors = {'authors_count':3}
#     authors = Author.objects.all().aggregate(authors_count=Count('id'))
#     count = authors.get('authors_count')
#     print(count)
#     return render(request, 'my_app/index.html', {'count': count})


# def book_list(request):
#     books = Book.objects.all().annotate(min_price=Max('price')).filter(min_price__gt=5000).order_by(
#         '-min_price').aggregate(avg_book_price=Avg('min_price'))
#
#     return render(request, 'my_app/index.html', {'books': books})


def magic(request):
    # authors = Author.objects.all().aggregate(authors_count=Count('id'))
    books1 = Book.objects.values('author__name').annotate(book_count=Count('id'))  # =>   author's => book count
    books2 = Book.objects.values('author__name').annotate(max_price=Max('price'))  # =>   author's => max price book
    books3 = Book.objects.values('author__name').annotate(min_price=Min('price'))  # =>   author's => min price book
    books4 = Book.objects.values('author__name').annotate(avg=Avg('price'))        # =>   author's => avg price book
    # authors = Author.objects.all().aggregate(max_price=Max('books__price'))
    return render(request, 'my_app/index.html',
                  {'books1': books1, 'books2': books2, 'books3': books3, 'books4': books4})
