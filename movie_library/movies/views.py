from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie, MovieList
from .serializers import MovieSerializer, MovieListSerializer
import requests

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def search_movies(request):
    query = request.GET.get('q')
    if query:
        response = requests.get(f'http://www.omdbapi.com/?s={query}&apikey=c57e847e')
        data = response.json()
        return Response(data)
    return Response({'error': 'No query parameter provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def movie_list(request):
    if request.method == 'GET':
        lists = MovieList.objects.filter(user=request.user)
        serializer = MovieListSerializer(lists, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        data['user'] = request.user.id
        serializer = MovieListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def movie_list_detail(request, pk):
    try:
        movie_list = MovieList.objects.get(pk=pk, user=request.user)
    except MovieList.DoesNotExist:
        return Response({'error': 'Movie list not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieListSerializer(movie_list)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        data['user'] = request.user.id
        serializer = MovieListSerializer(movie_list, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movie_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import SignUpForm

class CustomLoginView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class SignUpView(View):
    form_class = SignUpForm
    template_name = 'signup.html'
    next_page = reverse_lazy('login')


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})





# views.py
import requests
from django.shortcuts import render
from .forms import MovieSearchForm
from .models import Movie, MovieList, ListItem

def home(request):
    form = MovieSearchForm()
    movies = []

    if request.method == 'GET' and 'query' in request.GET:
        form = MovieSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            response = requests.get(f'http://www.omdbapi.com/?s={query}&apikey=c57e847e')
            movies = response.json().get('Search', [])

    return render(request, 'home.html', {'form': form, 'movies': movies})


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, MovieList, ListItem
from .forms import MovieSearchForm

@login_required
def create_list(request):
    if request.method == 'POST':
        name = request.POST['name']
        is_public = request.POST.get('is_public', False)
        movie_list = MovieList.objects.create(name=name, user=request.user, is_public=is_public)
        return redirect('list_detail', list_id=movie_list.id)
    return render(request, 'create_list.html')

@login_required
# views.py
def list_detail(request, list_id):
    movie_list = get_object_or_404(MovieList, id=list_id)
    if not movie_list.is_public and movie_list.user != request.user:
        return redirect('home')
    return render(request, 'list_detail.html', {'movie_list': movie_list})



