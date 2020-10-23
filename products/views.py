from rest_framework.decorators import api_view
from rest_framework import request, status
from rest_framework.response import Response
from django.core.exceptions import FieldError
from .models import Product
from .serializers import ProductSerializer
import logging
from Bookstore import responses
from .productRepository import get_book


logger = logging.getLogger("django")

# Create your views here.
@api_view(["GET"])
def get_books(request, sort="", id=0):
    """
    API to get all the books available or
    book corresponding to an id, author or title of book

    Parameter:
    argument(1): value for sort(name of field to be sorted by)
    argument(2): id to search book details corresponding to it
    argument(3): request body with either title or author of book

    Returns:
    Details of all books available sorted by field name given,
    by default returns books details by insertion order or
    details of book corresponding to the id or title or author
    name passed.
    """
    try:
        books = get_book(request, id, sort)
        serializer = ProductSerializer(books, many=True)
        if serializer.is_valid:
            if serializer.data == []:
                return Response(
                    responses.get_response("EmptyBookList"),
                    status=responses.get_response("EmptyBookList").get("status"),
                )
            else:
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(serializer.errors)
            return Response(
                {
                    "error_message": serializer.errors,
                    "Status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Product.DoesNotExist:
        return Response(
            responses.get_response("EmptyBookList"),
            status=responses.get_response("EmptyBookList").get("status"),
        )
    except FieldError:
        return Response(
            responses.get_response("FieldError"),
            status=responses.get_response("FieldError").get("status"),
        )
    except Exception as e:
        logger.error(e)
        return Response(
            responses.get_response("GetBookError"),
            status=responses.get_response("GetBookError").get("status"),
        )