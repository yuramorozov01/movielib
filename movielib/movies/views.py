from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer


class MovieListView(APIView):
	'''Output movie list'''

	def get(self, request):
		movies = Movie.objects.filter(draft=False)
		serializer = MovieListSerializer(movies, many=True)
		return Response(serializer.data)


class MovieDetailsSerializer(serializers.ModelSerializer):
	'''Movie details'''

	class Meta:
		model = Movie
		exclude = ('draft',)