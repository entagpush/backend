from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.models import ArtistProfile
from accounts.serializers import ArtistProfileSerializer
from customer.models import Gig, Message
from customer.serializers import (
    ArtistReviewSerializer,
    GigSerializer,
    MessageSerializer,
)


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArtistProfile.objects.filter(user__is_active=True)
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CustomerViewSet(viewsets.GenericViewSet):
    queryset = ArtistProfile.objects.filter(user__is_active=True, user__is_artist=True)
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    # @action(
    #     detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    # )
    # def create_gig(self, request, pk=None):
    #     artist = self.get_object()
    #     serializer = GigSerializer(data=request.data, context={"request": request})
    #     if serializer.is_valid():
    #         serializer.save(artist=artist)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def post_review(self, request, pk=None):
        artist = self.get_object()
        serializer = ArtistReviewSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            review = serializer.save(artist=artist)
            # Update artist ranking based on new review
            artist.update_ranking(review.rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(
            receiver=user
        )

    def perform_create(self, serializer):
        receiver = serializer.validated_data["receiver"]
        if not (
            (self.request.user.is_artist and receiver.is_customer)
            or (self.request.user.is_customer and receiver.is_artist)
        ):
            return Response(
                {"error": "Messages can only be sent between artists and customers."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(sender=self.request.user)


class GigViewSet(viewsets.ModelViewSet):
    queryset = Gig.objects.all()
    serializer_class = GigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_customer:
            return Gig.objects.filter(customer=user)
        elif user.is_artist:
            return Gig.objects.filter(artist__user=user)
        return Gig.objects.none()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
