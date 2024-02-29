from django.shortcuts import render

from datetime import datetime, date
from django.db.models import Q, Count, F
from django.shortcuts import get_object_or_404

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets, filters, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Blog, Waitlist
from .serializers import WaitListSerializer, BlogSerializer

# Create your views here.


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BlogSerializer
    filter_backends = [filters.SearchFilter]


class WaitlistViewSet(viewsets.ModelViewSet):
    queryset = Waitlist.objects.all()
    permission_classes = [AllowAny]
    serializer_class = WaitListSerializer
    filter_backends = [filters.SearchFilter]
