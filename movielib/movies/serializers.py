from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class MovieListSerializer(serializers.ModelSerializer):
	'''Movie list'''

	rating_user = serializers.BooleanField()
	middle_star = serializers.IntegerField()
	
	class Meta:
		model = Movie
		fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'middle_star')


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


class ActorListSerializer(serializers.ModelSerializer):
	'''Output actor and director list'''

	class Meta:
		model = Actor
		fields = ('id', 'name', 'image')


class ActorDetailsSerializer(serializers.ModelSerializer):
	'''Output actor and director details'''

	class Meta:
		model = Actor
		fields = '__all__'

		
class MovieDetailsSerializer(serializers.ModelSerializer):
	'''Movie details'''

	category = serializers.SlugRelatedField(slug_field='name', read_only=True)
	directors = ActorListSerializer(read_only=True, many=True)
	actors = ActorListSerializer(read_only=True, many=True)
	genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	reviews = ReviewSerializer(many=True)
	
	class Meta:
		model = Movie
		exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
	'''Adding rating by user'''

	class Meta:
		model = Rating
		fields = ('star', 'movie')


	def create(self, validated_data):
		rating, _ = Rating.objects.update_or_create(ip=validated_data.get('ip', None), movie=validated_data.get('movie', None), defaults={'star': validated_data.get('star')})
		return rating


