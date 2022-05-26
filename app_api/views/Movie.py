from unicodedata import name
from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from app_api.models.Movie import Movie
from django.contrib.auth.models import User
from rest_framework.decorators import action


class MovieView(ViewSet):

    def list(self, request):
        movies = Movie.objects.all()
        genre_id = request.query_params.get("genre_id", None)

        if genre_id is not None:
            movies = movies.filter(genre__id=genre_id)

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CreateMovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.auth.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        serializer = CreateMovieSerializer(movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        movie.run_time = request.data["run_time"]
        movie.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=False)
    def my_movies(self, request):
        movies = Movie.objects.filter(user=request.auth.user)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def movies_under100(self, request):
        movies = Movie.objects.filter(run_time__lte=100)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def movies_starts_with_h(self, request):
        movies = Movie.objects.filter(genre__name__endswith="r")
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def movies_horror_or_romance(self, request):
        genrelist = ["Horror", "Romance"]
        movies = Movie.objects.filter(genre__name__in=genrelist)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name')


class CreateMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'run_time', 'date_released', 'genre')


class MovieSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Movie
        fields = ('id', 'title', "description", "run_time",
                  'user', 'date_released', 'genre')
        depth = 1
