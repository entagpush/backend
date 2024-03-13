from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api import AdminInvitationViewSet, UserRegistrationViewSet

router = DefaultRouter()
router.register(r"signup", UserRegistrationViewSet, basename="user-signup")
router.register(r"admin-invitations", AdminInvitationViewSet)


urlpatterns = [
    path("admin/", include(router.urls)),
    path(
        "admin/token/",
        csrf_exempt(TokenObtainPairView.as_view()),
        name="token_obtain_pair",
    ),
    path("admin/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
