from rest_framework import serializers

from .models import Movie


class MovieListSerializer(serializers.ModelSerializer):
	'''Movie list'''

	class Meta:
		model = Movie
		fields = ('title', 'tagline', 'category')


class MovieDetailsSerializer(serializers.ModelSerializer):
	'''Movie details'''

	class Meta:
		model = Movie
		exclude = ('draft',)