from django.shortcuts import get_object_or_404

import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import FavoriteMovie, Person
from .serializers import FavoriteMovieSerializer, PersonDetailSerializer, PersonListSerializer


class PersonFavoriteMovieViewSet(viewsets.ViewSet):

    def create(self, request, person_id=None):
        person = get_object_or_404(Person, id=person_id)

        if person.favorite_movies.count() >= 10:
            return Response(
                {"detail": "A person can only have a maximum of 10 favorite movies."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["person"] = person.id
        serializer = FavoriteMovieSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, person_id=None, pk=None):
        person = get_object_or_404(Person, id=person_id)
        favorite_movie = get_object_or_404(FavoriteMovie, person=person, id=pk)
        favorite_movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by("last_name", "first_name")
    serializer_class = PersonDetailSerializer, PersonListSerializer
    
    def get_serializer_class(self):
        if self.action in ['list']:
            return PersonListSerializer
        return PersonDetailSerializer

    @action(
        detail=False, methods=["get"], name="Get person by name", url_path="get-by-name"
    )
    def get_person_by_name(self, request):
        name = request.query_params.get("name", None)
        if not name:
            return Response(
                {"detail": "Name parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            person = Person.objects.get(first_name__icontains=name)
            serializer = PersonDetailSerializer, PersonListSerializer(person)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response(
                {"detail": "Person not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Person.MultipleObjectsReturned:
            return Response(
                {"detail": "Multiple persons found with that name"},
                status=status.HTTP_400_BAD_REQUEST,
            )
