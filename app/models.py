from django.core.exceptions import ValidationError
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    has_insurance = models.BooleanField(default=False)

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.get_full_name


class FavoriteMovie(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="favorite_movies"
    )
    movie_id = models.IntegerField()

    class Meta:
        unique_together = ("person", "movie_id")

    def clean(self):
        if self.person.favorite_movies.count() >= 10:
            raise ValidationError(
                "A person can only have a maximum of 10 favorite movies."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person.name} - Movie ID: {self.movie_id}"
