from django.core.mail import send_mail
from django.db import transaction
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from accounts.models import Genre
from customer.models import ArtistApplication
from .serializers import ArtistApplicationSerializer, GenreSerializer

User = settings.AUTH_USER_MODEL


class ArtistApplicationViewSet(viewsets.GenericViewSet):
    queryset = ArtistApplication.objects.all()
    serializer_class = ArtistApplicationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ArtistApplicationSerializer,
        responses={200: ArtistApplicationSerializer},
    )
    def perform_create(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        request_body=GenreSerializer,
        responses={200: GenreSerializer},
    )
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def create_genre(self, request, *args, **kwargs):
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: GenreSerializer},
    )
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def list_genres(self, request, *args, **kwargs):
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        application = self.get_object()
        application.status = "approved"
        application.save()

        # Activate the user and send an email notification
        user = User.objects.get(email=application.email)
        user.is_active = True
        user.save()
        # send_mail(
        #     "Artist Application Approved",
        #     f"Congratulations {application.name}, your application has been approved!",
        #     "from@example.com",
        #     [application.email],
        #     fail_silently=False,
        # )
        return Response({"status": "application approved"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        application = self.get_object()
        application.status = "rejected"
        application.save()

        # Send an email notification
        # send_mail(
        #     "Artist Application Rejected",
        #     f"Sorry {application.name}, your application has been rejected.",
        #     "from@example.com",
        #     [application.email],
        #     fail_silently=False,
        # )
        return Response({"status": "application rejected"})

    @action(methods=["post"], detail=False, permission_classes=[IsAuthenticated])
    @transaction.atomic
    def submit_artist_application(self, request, *args, **kwargs):
        serializer = ArtistApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Artist application submitted successfully."},
            status=status.HTTP_201_CREATED,
        )
