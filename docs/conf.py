# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add project root to path for autodoc
sys.path.insert(0, os.path.abspath('..'))

# Set required Django settings for autodoc
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
os.environ.setdefault('SECRET_KEY', 'docs-build-secret-key-for-sphinx-readthedocs')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', 'localhost,readthedocs.org')

# Setup Django for autodoc
import django
try:
    django.setup()
except Exception as e:
    # Silently continue if Django setup fails
    pass

# -- Project information -----------------------------------------------------
project = 'OC Lettings'
copyright = '2025, Sébastien Grison'
author = 'Sébastien Grison'
release = '1.4.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinxcontrib.mermaid',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'fr'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
    'sticky_navigation': True,
}

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
