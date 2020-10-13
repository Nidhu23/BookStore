from django.urls import path
from . import views

urlpatterns = [
    path("allbooks/", views.get_books),
    path("bookbyname/", views.get_book_by_name),
]
