"""
Hypertag's template processing backend for Django.
"""

from django.template import Origin, TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy

from hypertag import HyperHTML



class Hypertag(BaseEngine):
    """
    Hypertag's template processing backend for Django. Produces HTML5 documents.
    This class should be installed in TEMPLATES, in Django project's settings.py:

    TEMPLATES = [
        {
            'BACKEND': 'hypertag.django.backend.Hypertag',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {},
        },
        # ... other engines here ...
    ]
    """
    
    # Name of the subdirectory containing the templates for this engine
    # inside an installed application.
    app_dirname = 'hypertag'


    def __init__(self, params):
        # print('setting up Hypertag backend...')
        params  = params.copy()
        options = params.pop('OPTIONS').copy()
        super().__init__(params)
        
        # `options` are ignored currently
        self.engine = HyperHTML()  #**options

    def from_string(self, template_code):
        
        return Template(self.engine, template_code)

    def get_template(self, template_name):
        
        tried = []
        for template_file in self.iter_template_filenames(template_name):
            try:
                script = open(template_file, 'rt').read()
                return Template(self.engine, script, template_file)

            except FileNotFoundError:
                tried.append((
                    Origin(template_file, template_name, self),
                    'Source does not exist',
                ))

        raise TemplateDoesNotExist(template_name, tried = tried, backend = self)


class Template:

    def __init__(self, engine, view, filename = None):
        self.engine = engine
        self.view = view
        self.filename = filename

    def render(self, context=None, request=None):
        if context is None:
            context = {}
        if request is not None:
            context['request'] = request
            context['csrf_input'] = csrf_input_lazy(request)
            context['csrf_token'] = csrf_token_lazy(request)
        if self.filename and '__file__' not in context:
            context['__file__'] = self.filename
        
        return self.engine.render(self.view, **context)
    
    