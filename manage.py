"""
Django management script for the OC Lettings project.

This module provides the command-line utility for administrative tasks
such as running the development server, creating migrations, and managing
the database.
"""

import os
import sys


def main():
    """
    Run administrative tasks.

    Sets the Django settings module and executes the command-line utility.
    Raises ImportError if Django is not installed or not available.
    """
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
