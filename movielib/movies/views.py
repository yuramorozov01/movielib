from django.db import models

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, viewsets

from .models import Movie, Actor, Review, Genre
from .serializers import MovieListSerializer, MovieDetailsSerializer, ReviewCreateSerializer, CreateRatingSerializer, ActorListSerializer, ActorDetailsSerializer, GenreSerializer
from .service import get_client_ip, MovieFilter, PaginationMovies


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
	'''Output movies'''
	filter_backends = (DjangoFilterBackend,)
	filterset_class = MovieFilter
	pagination_class = PaginationMovies

	def get_queryset(self):
		movies = Movie.objects.filter(draft=False).annotate(
			rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
		).annotate(
			middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
		)
		return movies

	def get_serializer_class(self):
		if self.action == 'list':
			return MovieListSerializer
		elif self.action == 'retrieve':
			return MovieDetailsSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
	'''Create movie review'''

	serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
	'''Add movie rating'''

	serializer_class = CreateRatingSerializer

	def perform_create(self, serializer):
		serializer.save(ip=get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
	'''Output actors'''

	queryset = Actor.objects.all()

	def get_serializer_class(self):
		if self.action == 'list':
			return ActorListSerializer
		elif self.action == 'retrieve':
			return ActorDetailsSerializer


class GenreViewSet(viewsets.ModelViewSet):
	'''Output all genres'''

	queryset = Genre.objects.all()
	serializer_class = GenreSerializer

