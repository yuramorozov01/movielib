from rest_framework import serializers

from .models import Movie, Review


class MovieListSerializer(serializers.ModelSerializer):
	'''Movie list'''

	class Meta:
		model = Movie
		fields = ('title', 'tagline', 'category')


class RecursiveReviewChildrenSerializer(serializers.Serializer):
	'''Recursive review children output'''

	def to_representation(self, value):
		serializer = self.parent.parent.__class__(value, context=self.context)
		return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
	'''Filter for reviews to output only parent reviews'''

	def to_representation(self, data):
		data = data.filter(parent=None)
		return super().to_representation(data)
		

class ReviewCreateSerializer(serializers.ModelSerializer):
	'''Create review'''

	class Meta:
		model = Review
		fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
	'''Output review'''

	children = RecursiveReviewChildrenSerializer(many=True)

	class Meta:
		list_serializer_class = FilterReviewListSerializer
		model = Review
		fields = ('name', 'text', 'children')


class MovieDetailsSerializer(serializers.ModelSerializer):
	'''Movie details'''

	category = serializers.SlugRelatedField(slug_field='name', read_only=True)
	directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	reviews = ReviewSerializer(many=True)
	
	class Meta:
		model = Movie
		exclude = ('draft',)