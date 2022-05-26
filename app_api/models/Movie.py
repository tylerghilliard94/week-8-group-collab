from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    run_time = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="movies")
    date_released = models.DateField(default=date.today())
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, related_name="movies")

    @property
    def watched(self):
        return self.__watched

    @watched.setter
    def watched(self, value):
        if value == 2 and self.genre.name == "Horror":
            self.__watched = True
        else:
            self.__watched = False
