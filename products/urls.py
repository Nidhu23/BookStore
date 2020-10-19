from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("book/all/<int:id>", views.get_books),
    path("book/all/<sort>", views.get_books),
    path("book/all/", cache_page(900)(views.get_books)),
]
