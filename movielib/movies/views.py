from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailsSerializer, ReviewCreateSerializer


class MovieListView(APIView):
	'''Output movie list'''

	def get(self, request):
		movies = Movie.objects.filter(draft=False)
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