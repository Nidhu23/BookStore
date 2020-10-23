from rest_framework.test import APITestCase
from products import models, serializers


class TestSetUp(APITestCase):
    def setUp(self):
        self.data = {
            "author": "Chetan Bhagat",
            "title": "The Girl in Room 105",
            "image": "http://books.google.com/books/content?id=GHt_uwEACAAJ&printsec=frontcover&img=1&zoom=5'",
            "quantity": 12,
            "price": 193,
            "description": "Hi I'm Keshavand my life is screwed.",
        }
        serializer = serializers.ProductSerializer(data=self.data)
        if serializer.is_valid():
            serializer.save()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()