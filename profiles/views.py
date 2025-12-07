"""
Views for the profiles application.

This module contains the view functions for displaying user profiles.
"""
import logging

from django.http import Http404
from django.shortcuts import render

from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    """
    Display list of all profiles.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered profiles list template.
    """
    logger.info("Profiles index page accessed")
    profiles_list = Profile.objects.all()
    logger.debug("Retrieved %d profiles", profiles_list.count())
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

    Raises:
        Http404: If no profile with the given username exists.
    """
    logger.info("Profile detail page accessed for username: %s", username)
    try:
        profile = Profile.objects.get(user__username=username)
        logger.debug("Found profile for user: %s", username)
    except Profile.DoesNotExist:
        logger.error("Profile for username '%s' not found", username)
        raise Http404(f"Profile for username '{username}' does not exist")
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
