from .models import Product
from rest_framework import request
from django.db.models import Q
from .decorators import paginate

@paginate
def get_book(request, id, sort):
    if id == 0:
        if request.body != b"":
            books = Product.objects.filter(
                Q(title__iexact=request.data.get("title"))
                | Q(author__icontains=request.data.get("author"))
            )
            return books
        if sort == "":
            books = Product.objects.all()
        else:
            books = Product.objects.order_by(sort)
    else:
        books = Product.objects.filter(id=id)
    return books