from django.urls import path, include
from rest_framework.routers import DefaultRouter
from website.api import BlogViewSet, WaitlistViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"blogs", BlogViewSet)
router.register(r"waitlist", WaitlistViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
