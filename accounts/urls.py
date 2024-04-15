from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api import AdminInvitationViewSet, UserRegistrationViewSet

router = DefaultRouter()
router.register(r"auth-user", UserRegistrationViewSet, basename="user-signup")
router.register(r"admin-invitations", AdminInvitationViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "token/", TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
