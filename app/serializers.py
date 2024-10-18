from rest_framework import serializers

from .models import FavoriteMovie, Person


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = ["id", "person", "movie_id"]

    def validate(self, data):
        person = data["person"]
        if person.favorite_movies.count() >= 10:
            raise serializers.ValidationError(
                "A person can only have a maximum of 10 favorite movies."
            )
        return data


class PersonDetailSerializer(serializers.ModelSerializer):
    favorite_movies = FavoriteMovieSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = "__all__"


class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "first_name", "last_name"]
