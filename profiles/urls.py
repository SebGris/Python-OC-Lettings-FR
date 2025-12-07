"""
URL configuration for the profiles application.

This module defines the URL patterns for the profiles app,
including the list view and detail view for individual profiles.
"""
from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
]
