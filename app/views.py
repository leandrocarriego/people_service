from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by("last_name", "first_name")
    serializer_class = PersonSerializer

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
            serializer = PersonSerializer(person)
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
