from django.db import models

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailsSerializer, ReviewCreateSerializer, CreateRatingSerializer
from .service import get_client_ip


class MovieListView(APIView):
	'''Output movie list'''

	def get(self, request):
		movies = Movie.objects.filter(draft=False).annotate(
			rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
		).annotate(
			middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
		)
		serializer = MovieListSerializer(movies, many=True)
		return Response(serializer.data)


class MovieDetailsView(APIView):
	'''Output movie details'''

	def get(self, request, movie_id):
		movie = Movie.objects.get(id=movie_id, draft=False)
		serializer = MovieDetailsSerializer(movie)
		return Response(serializer.data)


class ReviewCreateView(APIView):
	'''Create movie review'''

	def post(self, request):
		review = ReviewCreateSerializer(data=request.data)
		if review.is_valid():
			review.save()
			
		return Response(status=201)


class AddStarRatingView(APIView):
	'''Add movie rating'''

	def post(self, request):
		serializer = CreateRatingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(ip=get_client_ip(request))
			return Response(status=201)
		else:
			return Response(status=400)

