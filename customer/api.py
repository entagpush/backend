from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.models import ArtistProfile
from accounts.serializers import ArtistProfileSerializer
from customer.models import Gig, Message
from customer.serializers import (
    ArtistReviewSerializer,
    CounterOfferMessageSerializer,
    GigSerializer,
    MessageSerializer,
    RejectGigSerializer,
)
from customer.utils import create_message


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArtistProfile.objects.filter(user__is_active=True)
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CustomerViewSet(viewsets.GenericViewSet):
    queryset = ArtistProfile.objects.filter(user__is_active=True, user__is_artist=True)
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        if getattr(self, "swagger_fake_view", False):
            return Message.objects.none()

        user = self.request.user
        if user.is_authenticated:
            return Message.objects.filter(sender=user) | Message.objects.filter(
                receiver=user
            )
        return Message.objects.none()

    def perform_create(self, serializer):
        receiver = serializer.validated_data["receiver"]
        if not (
            (self.request.user.is_artist and receiver.is_customer)
            or (self.request.user.is_customer and receiver.is_artist)
        ):
            raise ValidationError(
                {"error": "Messages can only be sent between artists and customers."}
            )
        serializer.save(sender=self.request.user)


class GigViewSet(viewsets.ModelViewSet):
    queryset = Gig.objects.all()
    serializer_class = GigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Gig.objects.none()

        user = self.request.user

        if user.is_authenticated:
            if user.is_customer:
                return Gig.objects.filter(customer=user)
            elif user.is_artist:
                return Gig.objects.filter(artist__user=user)

        return Gig.objects.none()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def accept_gig(self, request, pk=None):
        gig: Gig = self.get_object()
        if request.user != gig.artist.user:
            return Response(
                {"error": "You are not allowed to accept this gig."},
                status=status.HTTP_403_FORBIDDEN,
            )
        gig.status = "accepted"
        gig.save()
        return Response({"status": "Gig accepted."}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def reject_gig(self, request, pk=None):
        serializer = RejectGigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        gig: Gig = self.get_object()
        if request.user != gig.artist.user:
            return Response(
                {"error": "You are not allowed to reject this gig."},
                status=status.HTTP_403_FORBIDDEN,
            )

        gig.status = "rejected"
        gig.reason_for_rejection = serializer.validated_data["reason"]

        gig.save()
        return Response({"status": "Gig rejected."}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def start_counter_offer(self, request, pk=None):
        gig = self.get_object()

        counter_offer_message = CounterOfferMessageSerializer(data=request.data)
        counter_offer_message.is_valid(raise_exception=True)

        if request.user != gig.customer.user:
            return Response(
                {"error": "You are not allowed to start a counter offer."},
                status=status.HTTP_403_FORBIDDEN,
            )
        gig.status = "counter_offer"
        gig.save()

        create_message(
            sender=gig.artist.user,
            receiver=gig.customer.user,
            content=counter_offer_message.data["content"],
            is_counter_offer=True,
            gig=gig,
        )

        return Response({"status": "Counter offer started."}, status=status.HTTP_200_OK)
