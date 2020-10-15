from django.urls import path
from . import views

urlpatterns = [
    path("book/all/<int:id>", views.get_books),
    path("book/all/<sort>", views.get_books),
    path("book/all/", views.get_books),
    path("book/name-or-author/", views.book_by_title_or_author),
]
