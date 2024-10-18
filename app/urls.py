from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PersonFavoriteMovieViewSet, PersonViewSet

router = DefaultRouter()

router.register(r"people", PersonViewSet, basename="people")
router.register(r'people/(?P<person_id>\d+)/favorite-movies', PersonFavoriteMovieViewSet, basename='favorite-movies')

urlpatterns = [
    path("", include(router.urls)),
]
