from xml.sax.saxutils import quoteattr
from hypertag.core.errors import VoidTagEx, TypeErrorEx


########################################################################################################################################################
#####
#####  TAG
#####

class Tag:
    """
    Base class for custom tags defined as a Python functions (external tags).
    Instances can be imported to a Hypertag script and used as tags.
    """
    name = None         # [str] name that indentifies this tag in a DOM and can be used in DOM selectors
    
    pure = True         # if True, the tag is assumed to always return the same result for the same arguments (no side effects),
                        # which enables caching of expand() calls and compactification of DOM nodes tagged with this tag
    
    def expand(self, body, attrs, kwattrs):
        """
        Subclasses should NOT append trailing \n nor add extra indentation during tag expansion
        - both things are added by the parser later on, if desired so by programmer.
        
        :param body: DOM of a translated body of tag occurrence, possibly empty; if a tag is void and does not expect a body,
                     but a non-empty body was passed, the tag should raise VoidTagEx
        :param attrs: list/tuple of positional attributes
        :param kwattrs: dict of keyword attributes; attributes are guaranteed to have valid XML names, but NOT necessarily valid Python names
        :return: string
        """
        raise NotImplementedError


########################################################################################################################################################

class TagFunction(Tag):
    """A wrapper that creates a Tag instance from a function. The `body` attribute is passed as a string to the function."""
    
    def __init__(self, fun, dom = False):
        self.fun  = fun
        self.name = fun.__name__
        self.dom  = dom
    
    def expand(self, body, attrs, kwattrs):
        if not self.dom: body = body.render()
        return self.fun(body, *attrs, **kwattrs)
        

class Null(Tag):
    """Null tag '.' is represented in the DOM tree. Its expand() passes the body unchanged."""
    
    name = 'null'
    
    def expand(self, body, attrs, kwattrs):
        return body.render()
    
null = Null()


########################################################################################################################################################
#####
#####  STANDARD MARKUP TAG
#####

class Markup(Tag):
    """
    A hypertag whose expand() outputs the body unchanged, surrounded by <name>...</name> strings, with proper handling
    of void tags <name /> and HTML/XHTML format differences for boolean attributes.
    This class is used for all built-in (X)HTML tags. It can also be used to define custom markup tags in an application.
    """
    
    name = None         # tag <name> to be printed into markup; may differ from the Hypertag name used inside a script (!)
    void = False        # True if this tag is void: the `body` in expand() should be empty and the element is rendered as self-closing: <NAME />
    mode = 'HTML'       # (X)HMTL compatibility mode: either 'HTML' or 'XHTML'
    
    def __init__(self, name = None, void = False, mode = 'HTML'):
        if name: self.name = name
        self.void = void
        self.mode = mode
    
    def expand(self, body, attrs, kwattrs):
        
        if attrs: raise TypeErrorEx("markup tag '%s' does not accept positional attributes" % self.name)
        
        name = self.name
        
        # render attributes
        kwattrs = filter(None, map(self._render_attr, kwattrs.items()))
        tag = ' '.join([name] + list(kwattrs))

        body = body.render()
        
        # render output
        if self.void:
            if body: raise VoidTagEx("non-empty body passed to a void markup tag '%s'" % name)
            return "<%s />" % tag
        else:
            # if the block contains a headline, the closing tag is placed on the same line as body;
            # a newline is added at the end, otherwise
            nl = '\n' if body[:1] == '\n' else ''
            return "<%s>" % tag + body + nl + "</%s>" % name

    def _render_attr(self, name_value):
        
        name, value = name_value
        if value is True:               # name=True   -- converted to:  name (HTML)  or  name="name" (XHTML)
            if self.mode == 'HTML':
                return name
            else:
                return '%s="%s"' % (name, name)
        if value is False:              # name=False  -- removed from attr list
            return None
        
        value = str(value)
        if '"' not in value:
            value = '"%s"' % value
        elif "'" not in value:
            value = "'%s'" % value
        else:
            value = quoteattr(value)    # escaping of <,>,&," chars is performed ONLY when the value contains a quote "
        
        return '%s=%s' % (name, value)
        

