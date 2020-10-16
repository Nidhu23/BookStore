from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import request
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from .serializers import ProductSerializer
import logging
from .productRepository import get_book
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
        books = get_book(request, id, sort)
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