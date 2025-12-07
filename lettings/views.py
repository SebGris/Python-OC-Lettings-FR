"""
Views for the lettings application.

This module contains the view functions for displaying lettings information.
"""
from django.shortcuts import render

from .models import Letting


def index(request):
    """
    Display list of all lettings.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered lettings list template.
    """
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """
    Display details of a specific letting.

    Args:
        request: The HTTP request object.
        letting_id: The ID of the letting to display.

    Returns:
        HttpResponse: The rendered letting detail template.
    """
    letting = Letting.objects.get(id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
