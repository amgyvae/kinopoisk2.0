from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name of Director")
    age = models.PositiveSmallIntegerField(default=0, verbose_name="Age of Director")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directors"
        
class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name of Genre")
    description = models.TextField(verbose_name="Description", blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        
class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    description = models.TextField(verbose_name="Description", blank=True)
    year = models.PositiveSmallIntegerField(default=0, verbose_name="Year")
    country = models.CharField(max_length=100, verbose_name="Name of Country")
    rating = models.FloatField(verbose_name="Rating (outsiding)")
    poster = models.ImageField(upload_to='posters/', verbose_name="Poster", null=True, blank=True)
    video_url = models.URLField(verbose_name="YouTube Video URL", null=True, blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_movies', blank=True)
    
    director = models.ForeignKey(Director, on_delete=models.CASCADE, verbose_name="Directors")
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name="Movie"
        verbose_name_plural="Movies"
        
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100, verbose_name='Name of Author')
    text = models.TextField(verbose_name='Text of Review')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review from {self.author} for movie {self.movie.title}"
