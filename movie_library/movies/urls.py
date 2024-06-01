from django.urls import path
from .views import *
from .views import CustomLoginView, CustomLogoutView, SignUpView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('search/', search_movies, name='search-movies'),
    path('alllists/', movie_list, name='movie-lists'),
    path('lists/<int:pk>/', movie_list_detail, name='movie-list-detail'),
    #routes for templates
    path('home/', home, name='home'),
    path('addlist/', create_list, name='create_list'),
    path('list/', list_detail, name='list_detail'),

    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),

]
