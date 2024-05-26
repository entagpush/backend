from django.core.mail import send_mail
from django.conf import settings

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ArtistApplication
from .serializers import ArtistApplicationSerializer

User = settings.AUTH_USER_MODEL


class ArtistApplicationViewSet(viewsets.ModelViewSet):
    queryset = ArtistApplication.objects.all()
    serializer_class = ArtistApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        application = self.get_object()
        application.status = "approved"
        application.save()

        # Activate the user and send an email notification
        user = User.objects.get(email=application.email)
        user.is_active = True
        user.save()
        send_mail(
            "Artist Application Approved",
            f"Congratulations {application.name}, your application has been approved!",
            "from@example.com",
            [application.email],
            fail_silently=False,
        )
        return Response({"status": "application approved"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        application = self.get_object()
        application.status = "rejected"
        application.save()

        # Send an email notification
        send_mail(
            "Artist Application Rejected",
            f"Sorry {application.name}, your application has been rejected.",
            "from@example.com",
            [application.email],
            fail_silently=False,
        )
        return Response({"status": "application rejected"})
