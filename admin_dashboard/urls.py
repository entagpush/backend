from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ArtistApplicationViewSet

router = DefaultRouter()
router.register(r"artist-applications", ArtistApplicationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
