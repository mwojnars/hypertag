from hypertag.core.errors import TypeErrorEx
from hypertag.core.tag import Markup
from hypertag.std.registry import Registry


register = Registry()


########################################################################################################################################################
#####
#####  UTILITIES
#####

def html_escape(text):
    """Escape HTML/XML special characters (& < >) in a string that's to be embedded in a text part of an HTML/XML document.
    For escaping attribute values use html_attr_escape() - attributes need a different set of special characters to be escaped.
    """
    return text.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')


########################################################################################################################################################
#####
#####  STANDARD HTML5 tags
#####
#####  In the future, we would like to provide a way to easily produce "polyglot" (X)HTML5 markup, which will be
#####  compatible with both HTML5 and XHTML5.
#####

_HTML_TAGS_VOID    = "area base br col command embed hr img input link meta param source track wbr".split()
_HTML_TAGS_NONVOID = "a abbr acronym address applet article aside audio b basefont bdi bdo big blockquote body " \
                     "button canvas caption center cite code colgroup data datalist dd del details dfn dialog dir " \
                     "div dl dt em fieldset figcaption figure font footer form frame frameset h1 h2 h3 h4 h5 h6 " \
                     "head header html i iframe ins kbd label legend li main map mark meter nav noframes noscript " \
                     "object ol optgroup option output p picture pre progress q rp rt ruby s samp script section " \
                     "select small span strike strong style sub summary sup svg table tbody td template textarea " \
                     "tfoot th thead time title tr tt u ul var video".split()

def _create(name, void):
    # register.tag(Markup(name.lower(), void, 'XHTML'))         # XHTML only permits lowercase tag names
    register.tag(Markup(name.lower(), void, 'HTML'))
    register.tag(Markup(name.upper(), void, 'HTML'))


### create tags

for tag in _HTML_TAGS_NONVOID:  _create(tag, False)
for tag in _HTML_TAGS_VOID:     _create(tag, True)
    

########################################################################################################################################################
#####
#####  HYPERTAG'S CUSTOM tags & functions (HTML-specific)
#####

@register.tag
class comment(Markup):
    
    name = "comment"
    
    def expand(self, body, attrs, kwattrs):
        
        if attrs or kwattrs: raise TypeErrorEx("'comment' tag does not accept attributes")
        body = body.render()
        
        # if the block contains a headline, the closing tag is placed on the same line as body;
        # a newline is added at the end, otherwise
        nl = '\n' if body[:1] == '\n' else ''
        return "<!--" + body + nl + "-->"
    

    