from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ArtistViewSet, CustomerViewSet, GigViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"artists", ArtistViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"gigs", GigViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
