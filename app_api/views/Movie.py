from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from app_api.models.Movie import Movie
from django.contrib.auth.models import User


class MovieView(ViewSet):

    def list(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        pass

    def update(self, request, pk):
        pass

    def destroy(self, request, pk):
        pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name')


class MovieSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Movie
        fields = ('title', "description", "run_time",
                  'user', 'date_released', 'genre')
        depth = 1
