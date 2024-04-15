from datetime import timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema

from accounts.models import AdminInvitation

from .serializers import (
    AdminInvitationSerializer,
    UserDetailsTokenSerializer,
    UserLoginSerializer,
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
        
        return Response({
            "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


    @csrf_exempt
    @action(methods=["post"], detail=False)
    @swagger_auto_schema(
        request_body=UserLoginSerializer, responses={200: UserDetailsTokenSerializer}
    )
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = self.get_user_token_response_data(user)
        return Response(data)


class AdminInvitationViewSet(viewsets.ModelViewSet):
    queryset = AdminInvitation.objects.all()
    serializer_class = AdminInvitationSerializer
    permission_classes = [IsAdminUser]
