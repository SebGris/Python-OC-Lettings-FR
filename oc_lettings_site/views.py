"""
Views for the Orange County Lettings main application.

This module contains the view functions for the main site pages.
"""
import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    """
    Display the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered home page template.
    """
    logger.info("Home page accessed")
    return render(request, 'index.html')
