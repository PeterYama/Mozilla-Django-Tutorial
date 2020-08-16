from django.contrib.auth.models import User
from catalog.models import Book
from django.urls import path, include
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

