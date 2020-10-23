from .test_setup import TestSetUp
from rest_framework.test import APITestCase
from rest_framework import status
from products import serializers, models


class ProductsAPITest(TestSetUp):
    def test_get_books(self):
        response = self.client.get("/book/all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_books_author(self):
        self.data = {"author": "Chetan Bhagat'"}
        response = self.client.get("/book/all/", self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_books_title(self):
        self.data = {"title": "The Girl in Room 105'"}
        response = self.client.get("/book/all/", self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
