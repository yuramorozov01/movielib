from django.db import models

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, viewsets

from .models import Movie, Actor, Review, Genre, RatingStar
from .serializers import MovieListSerializer, MovieDetailsSerializer, ReviewCreateSerializer, CreateRatingSerializer, ActorListSerializer, ActorDetailsSerializer, GenreSerializer, RatingStarSerializer
from .service import get_client_ip, MovieFilter, PaginationMovies


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
	'''Output movies'''

	filter_backends = (DjangoFilterBackend,)
	filterset_class = MovieFilter
	pagination_class = PaginationMovies
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		movies = Movie.objects.filter(draft=False).annotate(
			rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
		).annotate(
			middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
		)
		return movies.order_by('id')

	def get_serializer_class(self):
		if self.action == 'list':
			return MovieListSerializer
		elif self.action == 'retrieve':
			return MovieDetailsSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
	'''Create movie review'''

	pagination_class = None
	serializer_class = ReviewCreateSerializer
	permission_classes = [permissions.IsAuthenticated]


class AddStarRatingViewSet(viewsets.ModelViewSet):
	'''Add movie rating'''

	pagination_class = None
	serializer_class = CreateRatingSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(ip=get_client_ip(self.request))


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
	'''Output actors'''

	queryset = Actor.objects.all()
	pagination_class = None
	permission_classes = [permissions.IsAuthenticated]

	def get_serializer_class(self):
		if self.action == 'list':
			return ActorListSerializer
		elif self.action == 'retrieve':
			return ActorDetailsSerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
	'''Output all genres'''

	queryset = Genre.objects.all()
	pagination_class = None
	serializer_class = GenreSerializer
	permission_classes = [permissions.IsAuthenticated]


class RatingStarViewSet(viewsets.ReadOnlyModelViewSet):
	'''Output all available rating star values'''

	queryset = RatingStar.objects.all()
	pagination_class = None
	serializer_class = RatingStarSerializer
	permission_classes = [permissions.IsAuthenticated]

