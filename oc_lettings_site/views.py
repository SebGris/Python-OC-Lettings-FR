"""
Views for the Orange County Lettings main application.

This module contains the view functions for the main site pages.
"""
from django.shortcuts import render


def index(request):
    """
    Display the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered home page template.
    """
    return render(request, 'index.html')
