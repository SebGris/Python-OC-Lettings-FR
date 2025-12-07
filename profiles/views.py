"""
Views for the profiles application.

This module contains the view functions for displaying user profiles.
"""
from django.shortcuts import render

from .models import Profile


def index(request):
    """
    Display list of all profiles.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered profiles list template.
    """
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """
    Display details of a specific profile.

    Args:
        request: The HTTP request object.
        username: The username of the profile to display.

    Returns:
        HttpResponse: The rendered profile detail template.
    """
    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
