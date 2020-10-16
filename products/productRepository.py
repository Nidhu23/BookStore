from .models import Product
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import request
from django.db.models import Q


def get_book(request, id, sort):
    if id == 0:
        if request.body != b"":
            books = Product.objects.filter(
                Q(title__iexact=request.data.get("title"))
                | Q(author__iexact=request.data.get("author"))
            )
            return books
        if sort == "":
            books = Product.objects.all()
        else:
            books = Product.objects.order_by(sort)
        try:
            paginator = Paginator(books, 10)
            page = request.GET.get("page")
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
    else:
        books = Product.objects.filter(id=id)
    return books