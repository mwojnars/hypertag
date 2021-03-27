from hypertag.core.runtime import Runtime
from hypertag.std.html import html_escape
import hypertag.html


########################################################################################################################################################
#####
#####  HTML runtime
#####


class HyperHTML(Runtime):
    
    language = 'HTML'
    escape   = staticmethod(html_escape)
    BUILTINS = Runtime.BUILTINS + ['hypertag.html']
    