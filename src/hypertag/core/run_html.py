from hypertag.core.runtime import Runtime, _read_module
from hypertag.std.html import html_escape
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
    