from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import request
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from .serializers import ProductSerializer
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

logger = logging.getLogger("django")

# Create your views here.
@api_view(["GET"])
def get_books(request, sort="", id=0):
    """
    API to get all the books available

    Parameter:
    argument(1): value for sort(name of field to be sorted by)
    argument(2): id to search book details corresponding to it

    Returns:
    Details of all books available sorted by field name given,
    by default returns books details by insertion order or
    details of book corresponding to the id passed.
    """
    try:
        if id == 0:
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
        serializer = ProductSerializer(books, many=True)
        if serializer.is_valid:
            if serializer.data == []:
                return Response("No books found", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(serializer.errors)
            return Response(
                {
                    "Error_message": serializer.errors,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )
    except Product.DoesNotExist:
        return Response(
            {
                "Error_message": "The Book does not exist",
                "status_code": status.HTTP_404_NOT_FOUND,
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error(e)
        return Response(
            {
                "Error_message": "There was an error while fetching the books",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def book_by_title_or_author(request):
    """
    API to search book by it's title or author name

    Parameters:
    argument(1):request paramter: having title of book or author name

    Returns:
    Details of book that matches the title or author name
    """
    try:
        books = Product.objects.filter(
            Q(title=request.data.get("title")) | Q(author=request.data.get("author"))
        )
        serializer = ProductSerializer(books, many=True)
        if serializer.is_valid:
            if serializer.data == []:
                return Response(
                    {
                        "message": "Book with this title or author name does not exist",
                        "status_code": status.HTTP_404_NOT_FOUND,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(serializer.errors)
            return Response(
                {
                    "error_message": serializer.errors,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Exception as e:
        logger.error(e)
        return Response(
            {
                "error_message": "Something went wrong",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
