"""
Django standard filters for use with Hypertag.
A complete list and documentation of filters:  https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#built-in-filter-reference

All standard Django filters are loaded to this module's namespace, so that they can be imported into other files
and used as functions or Hypertag filters (with a pipeline operator), for example:

    from hypertag.django.filters import slugify
    from hypertag.django.filters import dictsort

OR, if imported in a Hypertag script:

    from hypertag.django.filters import $slugify

"""

import django as __django__
from django.conf import settings as __settings__
from django.template.defaultfilters import register as __register_default__
from django.contrib.humanize.templatetags.humanize import register as __register_humanize__

##
## for now, Django's default settings are always used in those filters that depend on them
##

__settings__.configure()
__django__.setup()


globals().update(__register_humanize__.filters)
globals().update(__register_default__.filters)

del globals()['__django__']
del globals()['__settings__']
del globals()['__register_default__']
del globals()['__register_humanize__']
