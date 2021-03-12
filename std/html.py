from hypertag.core.tag import MarkupTag


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

BUILTIN_HTML  = {}

_HTML_TAGS_VOID    = "area base br col command embed hr img input link meta param source track wbr".split()
_HTML_TAGS_NONVOID = "a abbr acronym address applet article aside audio b basefont bdi bdo big blockquote body " \
                     "button canvas caption center cite code colgroup data datalist dd del details dfn dialog dir " \
                     "div dl dt em fieldset figcaption figure font footer form frame frameset h1 h2 h3 h4 h5 h6 " \
                     "head header html i iframe ins kbd label legend li main map mark meter nav noframes noscript " \
                     "object ol optgroup option output p picture pre progress q rp rt ruby s samp script section " \
                     "select small span strike strong style sub summary sup svg table tbody td template textarea " \
                     "tfoot th thead time title tr tt u ul var video".split()

def _create_tag_triple(name_, void_):
    lname, uname = name_.lower(), name_.upper()
    #BUILTIN_XHTML[lname] = MarkupTag(lname, void_, 'XHTML')         # XHTML only permits lowercase tag names
    BUILTIN_HTML[lname]  = MarkupTag(lname, void_, 'HTML')
    BUILTIN_HTML[uname]  = MarkupTag(uname, void_, 'HTML')

def _create_all_tags():
    # HTML tags
    for tag in _HTML_TAGS_NONVOID:
        _create_tag_triple(tag, False)
    for tag in _HTML_TAGS_VOID:
        _create_tag_triple(tag, True)
    
    
###  append all (X)HTML tags to BUILTIN_HTML

_create_all_tags()


########################################################################################################################################################
#####
#####  HYPERTAG'S CUSTOM tags & functions (HTML-specific)
#####
