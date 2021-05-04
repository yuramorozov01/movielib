from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailsSerializer, ReviewCreateSerializer, CreateRatingSerializer


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


class AddStarRatingView(APIView):
	'''Add movie rating'''

	def get_client_ip(self, request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip 

	def post(self, request):
		serializer = CreateRatingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(ip=self.get_client_ip(request))
			return Response(status=201)
		else:
			return Response(status=400)

			