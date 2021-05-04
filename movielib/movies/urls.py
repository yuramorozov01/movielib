from django.urls import path

from . import views


urlpatterns = [
	path('movie/', views.MovieListView.as_view()),
	path('movie/<int:movie_id>/', views.MovieDetailsView.as_view()),
	path('review/', views.ReviewCreateView.as_view()),
]
