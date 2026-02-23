from django.shortcuts import render
from .models import Movie, Review
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import ReviewForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

import redis

# Create your views here.
def movie_list(request):
    #movies = Movie.objects.all()
    #for movie in movies:
    #    movie.genres_list = ", ".join(genre.name for genre in movie.genres.all())
    search_query = request.GET.get('q', '')
    if search_query:
        movies = Movie.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(director__name__icontains=search_query)
        )
    else:
        movies = Movie.objects.all()
    
    movies = cache.get('all_movies')
    if not movies:
        movies = Movie.objects.all()
        cache.set('all_movies', movies, 60 * 15)
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'search_query': search_query
        })

r = redis.StrictRedis(host='localhost', port=6379, db=0)
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def movie_detail(request, pk):
    # Достаем фильм по ID (pk). Если не найден — покажем ошибку 404.
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        r.publish('notifications', f"New review for movie {pk}!")
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.author = request.user.username
            review.save()
            return redirect('movie_detail', pk=movie.pk)
        else:
            print(form.errors)
    else:
        form = ReviewForm()
        
    return render(request, 'movies/movie_detail.html', {
        'movie': movie, 
        'form': form 
        })
    
@api_view(['GET'])
def movie_list_api(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail_api(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=404)
    
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    movie_pk = review.movie.pk
    review.delete()
    return redirect('movie_detail', pk=movie_pk)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def add_to_favorites(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if movie.favorites.filter(id=request.user.id).exists():
        movie.favorites.remove(request.user)
    else:
        movie.favorites.add(request.user)
    return redirect('movie_detail', pk=pk)

