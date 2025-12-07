"""
Views for the lettings application.

This module contains the view functions for displaying lettings information.
"""

import logging

from django.http import Http404
from django.shortcuts import render

from .models import Letting

logger = logging.getLogger(__name__)


def index(request):
    """
    Display list of all lettings.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered lettings list template.
    """
    logger.info("Lettings index page accessed")
    lettings_list = Letting.objects.all()
    logger.debug("Retrieved %d lettings", lettings_list.count())
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)


def letting(request, letting_id):
    """
    Display details of a specific letting.

    Args:
        request: The HTTP request object.
        letting_id: The ID of the letting to display.

    Returns:
        HttpResponse: The rendered letting detail template.

    Raises:
        Http404: If no letting with the given ID exists.
    """
    logger.info("Letting detail page accessed for ID: %s", letting_id)
    try:
        letting = Letting.objects.get(id=letting_id)
        logger.debug("Found letting: %s", letting.title)
    except Letting.DoesNotExist:
        logger.error("Letting with ID %s not found", letting_id)
        raise Http404(f"Letting with ID {letting_id} does not exist")
    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "lettings/letting.html", context)
