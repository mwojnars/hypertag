"""
Django standard filters imported for use with Hypertag.
A complete list and documentation of filters:  https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#built-in-filter-reference
"""

import django
from django.conf import settings as __settings__
from django.template.defaultfilters import register as __register__

##
## for now, Django's default settings are always used in those filters that depend on them
##

__settings__.configure()
django.setup()

## all standard Django filters are loaded to this module's namespace, so that they can be imported into other files
## and used as functions or Hypertag filters (with a pipeline operator), for example:
##
##  >>> from hypertag.django.filters import slugify
##  >>> from hypertag.django.filters import dictsort
##
## OR, if imported in a Hypertag script:
##
##      from hypertag.django.filters import $slugify
##

globals().update(__register__.filters)
