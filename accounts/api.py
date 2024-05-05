from datetime import timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import get_object_or_404


from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from accounts.models import AdminInvitation, UserProfile

from .serializers import (
    AdminInvitationSerializer,
    UserDetailsSerializer,
    UserDetailsTokenSerializer,
    UserLoginSerializer,
    UserProfileCreateSerializer,
    UserProfileSerializer,
    UserSerializer,
)

User = get_user_model()


class UserTokenResponseMixin:
    def get_user_token_response_data(self, user):
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token.set_exp(lifetime=timedelta(minutes=settings.WEB_TOKEN_EXPIRY))
        user_profile = user.profile
        # data = UserDetailsTokenSerializer(user_profile, context={"request": self.request}).data

        data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "user": user_profile,
        }

        return UserDetailsTokenSerializer(data, context={"request": self.request}).data


class UserRegistrationViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, UserTokenResponseMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)  # Create a new token for the user

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )

    @action(methods=["post"], detail=False)
    @swagger_auto_schema(
        request_body=UserLoginSerializer, responses={200: UserDetailsTokenSerializer}
    )
    @csrf_exempt
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = self.get_user_token_response_data(user)
        return Response(data)

    @action(methods=["patch"], detail=False, permission_classes=[IsAuthenticated])
    @swagger_auto_schema(
        request_body=UserProfileCreateSerializer, responses={200: UserProfileSerializer}
    )
    @transaction.atomic
    def update_user_profile(self, request, *args, **kwargs):
        user_profile = self.get_user_profile(request.user)

        # Update the existing user profile with the new data
        serializer = UserProfileCreateSerializer(
            instance=user_profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=UserProfileSerializer(instance=user_profile).data,
            status=status.HTTP_200_OK,
        )

    def get_user_profile(self, user):
        return get_object_or_404(UserProfile, user=user)


class AdminInvitationViewSet(viewsets.ModelViewSet):
    queryset = AdminInvitation.objects.all()
    serializer_class = AdminInvitationSerializer
    permission_classes = [IsAdminUser]
