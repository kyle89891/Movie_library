from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=255, unique=True)
    details = models.TextField()

    def __str__(self):
        return self.title

class MovieList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    movies = models.ManyToManyField(Movie, related_name='movie_lists')

    def __str__(self):
        return self.name
    
class ListItem(models.Model):
    movie_list = models.ForeignKey(MovieList, related_name='items', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} in {self.movie_list.name}"
