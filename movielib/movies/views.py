from django.db import models

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions

from .models import Movie, Actor
from .serializers import MovieListSerializer, MovieDetailsSerializer, ReviewCreateSerializer, CreateRatingSerializer, ActorListSerializer, ActorDetailsSerializer
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
	'''Output movie list'''

	serializer_class = MovieListSerializer
	filter_backends = (DjangoFilterBackend,)
	filterset_class = MovieFilter
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		movies = Movie.objects.filter(draft=False).annotate(
			rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
		).annotate(
			middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
		)
		return movies


class MovieDetailsView(generics.RetrieveAPIView):
	'''Output movie details'''

	queryset = Movie.objects.filter(draft=False)
	serializer_class = MovieDetailsSerializer


class ReviewCreateView(generics.CreateAPIView):
	'''Create movie review'''

	serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
	'''Add movie rating'''

	serializer_class = CreateRatingSerializer

	def perform_create(self, serializer):
		serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):
	'''Output list of actors'''

	queryset = Actor.objects.all()
	serializer_class = ActorListSerializer


class ActorDetailsView(generics.RetrieveAPIView):
	'''Output actor details'''

	queryset = Actor.objects.all()
	serializer_class = ActorDetailsSerializer

