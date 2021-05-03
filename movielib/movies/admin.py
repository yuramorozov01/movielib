from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Review


class MovieAdminForm(forms.ModelForm):
    '''Form with widget ckeditor'''
    description = forms.CharField(label='Description', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'

