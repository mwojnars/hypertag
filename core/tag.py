from xml.sax.saxutils import quoteattr
from hypertag.core.errors import VoidTagEx, TypeErrorEx


########################################################################################################################################################
#####
#####  BASE CLASSES
#####

class Tag:
    """
    Common base class for two major types of tags:
    - ExternalTag - a tag implemented as a python function
    - NativeTag - a tag implemented inside Hypertag code
    """

########################################################################################################################################################

class ExternalTag(Tag):
    """
    A custom tag defined as a Python function.
    Instances of ExternalTag can be imported to a Hypertag script and used as tags.
    """
    name = None         # tag name that can be used in selectors when manipulating a DOM
    
    void = False        # if True, passing non-empty body to expand() is forbidden and the parser should rather raise an exception
    flat = True         # if True, body is passed as plain text (rendered DOM) to expand(), which allows better compactification of constant subtrees of the AST (TODO)
    pure = True         # if True, the tag is assumed to always return the same result for the same arguments (no side effects),
                        # which potentially enables full compactification of a node tagged with this tag
    
    # term = False        # if True, the tag is treated as terminal (static), which means its expansion is delayed until DOM rendering
    #
    # xml_names = False   # if True, all valid XML names are accepted for attributes, and named attributes are passed
    #                     # to expand() as a dict, rather than keywords; in such case, expand() must implement
    #                     # the following signature:
    #                     #
    #                     #   def expand(self, body, kwattrs, *attrs)
    #                     #
    #                     # It is recommended that xml_names are set to False whenever possible.
    
    def expand(self, body, attrs, kwattrs):
        """
        Subclasses should NOT append trailing \n nor add extra indentation during tag expansion
        - both things are added by the parser later on, if desired so by programmer.
        
        :param body: DOM of a translated body of tag occurrence, if self.flat is false, or a rendered string otherwise;
                     if a tag is void (doesn't accept body), it should check if the body is empty and raise VoidTagEx if not
        :param attrs: list/tuple of positional attributes
        :param kwattrs: dict of keyword attributes; attributes are guaranteed to have valid XML names, but NOT necessarily valid Python names
        :return: string
        """
        raise NotImplementedError


class NullTag(ExternalTag):
    """Null tag '.' is represented in the DOM tree. Its expand() passes the body unchanged."""
    
    name = '.'
    
    def expand(self, body, attrs, kwattrs):
        return body
    
null_tag = NullTag()


########################################################################################################################################################

class NativeTag(Tag):
    """Base class for native tags, i.e., tags implemented inside Hypertag code."""

    def dom_expand(self, state, body, attrs, kwattrs, caller):
        """
        Native tags are expanded in a different way than external tags: they produce DOM during expansion, not a flat string,
        hence a different method to be called by the parser.
        """
        raise NotImplementedError


########################################################################################################################################################
#####
#####  STANDARD MARKUP TAG
#####

class MarkupTag(ExternalTag):
    """
    A hypertag whose expand() outputs the body unchanged, surrounded by <name>...</name> strings, with proper handling
    of void tags <name /> and HTML/XHTML format differences for boolean attributes.
    This class is used for all built-in (X)HTML tags. It can also be used to define custom markup tags in an application.
    """
    
    name = None         # tag <name> to be printed into markup; may differ from the Hypertag name used inside a script (!)
    void = False        # if True, body is expected to be empty in expand() and the returned element is self-closing
    flat = True         # markup tags don't do any DOM manipulation internally, so `body` can be passed in as a string
    mode = 'HTML'       # (X)HMTL compatibility mode: either 'HTML' or 'XHTML'
    
    def __init__(self, name, void = False, mode = 'HTML'):
        self.name = name
        self.void = void
        self.mode = mode
    
    def expand(self, body, attrs, kwattrs):
        
        if attrs: raise TypeErrorEx(f"markup tag '{self.name}' does not accept positional attributes")
        
        name = self.name
        
        # render attributes
        kwattrs = filter(None, map(self._render_attr, kwattrs.items()))
        tag = ' '.join([name] + list(kwattrs))
        
        # render output
        if self.void:
            if body: raise VoidTagEx(f"non-empty body passed to a void markup tag '{name}'")
            return f"<{tag} />"
        else:
            # if the block contains a headline, the closing tag is placed on the same line as body;
            # a newline is added at the end, otherwise
            nl = '\n' if body[:1] == '\n' else ''
            return f"<{tag}>" + body + nl + f"</{name}>"

    def _render_attr(self, name_value):
        
        name, value = name_value
        if value is True:               # name=True   -- converted to:  name (HTML)  or  name="name" (XHTML)
            if self.mode == 'HTML':
                return name
            else:
                return f'{name}="{name}"'
        if value is False:              # name=False  -- removed from attr list
            return None
        
        value = str(value)
        if '"' not in value:
            value = f'"{value}"'
        elif "'" not in value:
            value = f"'{value}'"
        else:
            value = quoteattr(value)    # escaping of <,>,&," chars is performed ONLY when the value contains a quote "
        
        return f'{name}={value}'
        

