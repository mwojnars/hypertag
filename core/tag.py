from xml.sax.saxutils import quoteattr
from hypertag.core.errors import VoidTagEx
from hypertag.core.DOM import Sequence, HNode


########################################################################################################################################################
#####
#####  SDK
#####

class Tag:
    """
    Base class for all tags:
    - ExternalTag - a tag implemented as a python function
    - NativeTag - a tag implemented inside Hypertag code
    """
    name = None         # tag name that can be searched for (selected) when post-processing a DOM through Sequence class
    
    void = False        # if True, __body__ is expected to be empty, otherwise an exception shall be raised by the caller
    text = False        # if True, __body__ will be provided as plain text (rendered DOM), not a DOM; allows better compactification
    pure = True         # if True, the tag is assumed to always return the same result for the same arguments (no side effects),
                        # which potentially enables full compactification of a node tagged with this tag
    
    xml_names = False   # if True, all valid XML names are accepted for attributes, and named attributes are passed
                        # to expand() as a dict, rather than keywords; in such case, expand() must implement
                        # the following signature:
                        #
                        #   def expand(self, body, kwattrs, *attrs)
                        #
                        # It is recommended that xml_names are set to False whenever possible.
    
    # text_body = False       # if True, the `body` argument to expand() will be a string (rendered DOM), not DOM;
    #                         # setting this to True whenever possible allows speed optimization through better
    #                         # compactification of constant subtrees of the AST before their passing to a hypertag

    # void / non-void ... strict / non-strict
    # def expand(self, __body__, *attrs, **kwattrs): pass
    # def expand(self, __body__, kwattrs, *attrs): pass
    
    def translate_tag(self, state, body, attrs, kwattrs, caller):
        raise NotImplementedError


class ExternalTag(Tag):
    """
    External tag, i.e., a (hyper)tag defined as a python function.
    Every tag behaves like a function, with a few extensions:
    - it accepts body as the 1st unnamed argument, passed in as a Sequence of HNodes, or plain text;
      some tags may expect body to be empty
    - it may accept any number of custom arguments, regular or keyword
    - it should return either a Sequence of nodes, or plain text, or None
    """

    def translate_tag(self, state, body, attrs, kwattrs, caller):
        """External tag doesn't depend on a state of script execution, hence `state` is ignored."""
        return Sequence(HNode(body, tag = self, attrs = attrs, kwattrs = kwattrs))

    def expand(self, __body__):     # more attributes can be defined in subclasses
        """
        Subclasses should NOT append trailing \n nor add extra indentation during tag expansion
        - both things will be added by the caller later on, if desired so by programmer.
        
        :param __body__: rendered main body of tag occurrence, as a string; if a tag is void (doesn't accept body),
                         it may check whether __body__ is empty and raise VoidTag exception if not
        :param attrs, kwattrs: tag-specific attributes, listed directly in subclasses and/or using *attrs/**kwattrs notation
        :return: string containing tag output; optionally, it can be accompanied with a dict of (modified) section bodies,
                 as a 2nd element of a pair (output_body, output_sections); if output_sections are NOT explicitly returned,
                 they are assumed to be equal __sections__; also, the __sections__ dict CAN be modified *in place*
                 and returned without copying
        """
        raise NotImplementedError

class NativeTag(Tag):
    """Base class for a native tag: a tag implemented inside Hypertag code."""
    
class SpecialTag(Tag): pass

class NullTag(SpecialTag):
    """Null tag '.' is represented in the DOM tree. Its expand() passes the body unchanged."""
    
    name = '.'
    
    def translate_tag(self, state, body, attrs, kwattrs, caller):
        assert not attrs and not kwattrs
        return Sequence(HNode(body, tag = self))

    def expand(self, __body__):
        return __body__.render()
    
null_tag = NullTag()



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
    void = False        # if True, __body__ is expected to be empty and the returned element is self-closing
    mode = 'HTML'       # (X)HMTL compatibility mode: either 'HTML' or 'XHTML'
    
    def __init__(self, name, void = False, mode = 'HTML'):
        self.name = name
        self.void = void
        self.mode = mode
    
    def expand(self, __body__, **attrs):
        
        name = self.name
        
        # render attributes
        attrs = filter(None, map(self._render_attr, attrs.items()))
        tag = ' '.join([name] + list(attrs))
        
        # render output
        if self.void:
            if __body__: raise VoidTagEx(f"non-empty body passed to a void markup tag <{name}>")
            return f"<{tag} />"
        else:
            assert isinstance(__body__, Sequence)
            body = __body__.render()

            # if the block contains a headline, the closing tag is placed on the same line as __body__
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
        

