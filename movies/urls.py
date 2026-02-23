from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name="movie_list"),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('api/movies/', views.movie_list_api, name="movie_list_api"),
    path('api/movie/<int:pk>/', views.movie_detail_api, name='movie_detail_api'),
    path('api/movie/<int:pk>/delete', views.delete_review, name='delete_review'),
    path('signup/', views.signup, name='signup'),
    path('movie/<int:pk>/favorite/', views.add_to_favorites, name='add_to_favorites'),
]
