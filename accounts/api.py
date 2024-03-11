from django.contrib.auth import get_user_model

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser

from accounts.models import AdminInvitation

from .serializers import AdminInvitationSerializer, UserSerializer

User = get_user_model()


class UserRegistrationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class AdminInvitationViewSet(viewsets.ModelViewSet):
    queryset = AdminInvitation.objects.all()
    serializer_class = AdminInvitationSerializer
    permission_classes = [IsAdminUser]
