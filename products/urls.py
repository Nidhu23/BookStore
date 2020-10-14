from django.urls import path
from . import views

urlpatterns = [
    path("allbooks/", views.get_books),
    path("bynameorauthor/", views.book_by_title_or_author),
    path("sortbyprice/", views.sort_by_price),
]
