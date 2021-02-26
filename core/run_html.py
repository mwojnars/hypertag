from hypertag.core._html import html_escape
from hypertag.core.runtime import Runtime, _read_module
import hypertag.html


########################################################################################################################################################
#####
#####  HTML runtime
#####


class HyperHTML(Runtime):
    
    language = 'HTML'
    escape   = staticmethod(html_escape)
    
    DEFAULT = Runtime.DEFAULT.copy()
    DEFAULT.update(_read_module(hypertag.html))
    