"""
Classes that represent Hypertag's native DOM (Document Object Model) that is produced as an output
of translation of the AST. The DOM can subsequently undergo "rendering" to a document in a target language.

DOM manipulation methods:
- find(path): generate a sequence of all (sub)nodes that match a given path.
- remove(path): remove from the DOM and return all (sub)nodes that match a given path;

@author:  Marcin Wojnarski
"""

import re, itertools
from types import GeneratorType
from nifty.util import Object

from hypertag.core.errors import VoidTagEx, TypeErrorEx


########################################################################################################################################################
#####
#####  UTILITIES
#####


def add_indent(text, indent, re_start = re.compile(r'\n(?=.)')):        # re.compile(r'(?m)^(?=.)')
    """
    Append `indent` string at the beginning of each line of `text` excluding the 1st line (!).
    Empty lines (containing zero characters, not even a space) are left untouched!
    """
    if not indent: return text
    return re_start.sub('\n' + indent, text)
    # if not text: return text
    # return indent + text.replace('\n', '\n' + indent)
    
def del_indent(text, indent = None):
    """
    Remove `indent` string from the beginning of each line of `text`, wherever it is present as a line prefix.
    If indent=None, maximum common indentation (get_indent()) is truncated.
    """
    if indent is None: indent = get_indent(text)
    if text.startswith(indent): text = text[len(indent):]
    return text.replace('\n' + indent, '\n')

def get_indent(text):
    """
    Retrieve the longest indentation string fully composed of whitespace
    that is shared by ALL non-empty lines in `text`, including the 1st line (if it contains a non-whitespace).
    """
    lines = text.split('\n')
    lines = list(filter(None, [l if l.strip() else '' for l in lines]))          # filter out empty lines
    if not lines: return ''

    for i, column in enumerate(zip(*lines)):        # zip() only eats up as many characters as the shortest line
        if not column[0].isspace() or min(column) != max(column):
            return lines[0][:i]
    else:
        size = min(map(len, lines))
        return lines[0][:size]                      # when all lines are prefixes of each other take the shortest one
    

########################################################################################################################################################
#####
#####  DOCUMENT OBJECT MODEL (DOM)
#####

class DOM:
    """
    List of DOM.Nodes that comprise (a part of) a body of a parent Node, or was produced as an intermediate
    collection of nodes during DOM manipulation.
    Provides methods for traversing a DOM tree and selecting nodes,
    as well as flattening and cleaning up the list during node construction.
    
    All DOM node classes: Node, Root, Text - are defined as inner classes of this one.
    """
    nodes = None
    
    def __init__(self, *nodes, _strict = True):
        self.nodes = self._flatten(nodes) if _strict else list(nodes)
        
    def __bool__(self):             return bool(self.nodes)
    def __len__(self):              return len(self.nodes)
    def __iter__(self):             return iter(self.nodes)
    def __getitem__(self, pos):
        
        if isinstance(pos, str):
            return self.select(pos)
        if isinstance(pos, slice):
            return DOM(self.nodes[pos], _strict = False)
        return self.nodes[pos]
    
    @staticmethod
    def node(*args, **kwargs):
        """
        Create a DOM consisting of a single DOM.Node instance initialized with given arguments.
        A shortcut for DOM(DOM.Node(...)).
        """
        return DOM(DOM.Node(*args, **kwargs))
    
    @staticmethod
    def text(*args, **kwargs):
        """
        Create a DOM consisting of a single DOM.Text instance initialized with given arguments.
        A shortcut for DOM(DOM.Text(...)).
        """
        return DOM(DOM.Text(*args, **kwargs))
    
    @staticmethod
    def _flatten(nodes):
        """Flatten nested lists of nodes by concatenating them into the top-level list; drop None's."""
        result = []
        for n in nodes:
            if n is None: continue
            if isinstance(n, (list, DOM, GeneratorType)):
                result += DOM._flatten(n)
            elif isinstance(n, DOM.Node):
                result.append(n)
            else:
                raise TypeErrorEx(f"found {type(n)} in a DOM, expected DOM.Node")
        return result
        
    def set_indent(self, indent):
        for n in self.nodes:
            n.set_indent(indent)
            
    def render(self):
        return ''.join(node.render() for node in self.nodes)

    def tree(self, indent = '', step = '  '):
        r"""Return a multiline \n-terminated string that presents this DOM's structure as a list of trees."""
        return ''.join(node.tree(indent, step) for node in self.nodes)
        

    ### SELECTORS API
    
    def walk(self, order = 'preorder'):
        """
        Generator of all nodes inside this DOM: parent nodes and descendants.
        Parents are yielded before descendants if order='preorder' (default), or after descendants if order='postorder'.
        The set of nodes is NOT wrapper up in a DOM - use select() instead if you need a DOM.
        """
        # if order not in ('preorder', 'postorder'): raise TypeErrorEx(f"incorrect value of order ({order})")
        return itertools.chain(*(node.walk(order) for node in self.nodes))

    ATTR_DEFINED = Object(name = 'ATTR_DEFINED')

    def select(self, tag = None, attr = None, value = ATTR_DEFINED, order = 'preorder', **attrs):
        """
        Select all nodes (including descendants) that match given search criteria and return as a new DOM instance.
        :param tag: desired tag name (<str>) or Tag instance that should be present in a matching node
        """
        name = None
        if tag:
            if isinstance(tag, str):
                name = tag
                tag  = None
        
        if attr is not None:
            attrs[attr] = value
            
        nodes = []
        
        for node in self.walk(order):
            if tag  is not None and node.tag is not tag: continue
            if name is not None and (node.tag is None or node.tag.name != name): continue
            
            stop = False
            for a, v in attrs.items():
                if a not in node.kwattrs: stop = True; break
                if v is not DOM.ATTR_DEFINED and node.kwattrs[a] != v: stop = True; break
            if stop: continue
            
            nodes.append(node)
        
        return DOM(*nodes, _strict = False)
        
        
    def skip(self, tag = None, id = None, class_ = None, **attrs):
        """Return a copy of `self`, but with the nodes matching the provided criteria removed."""
        
    # Selectors TODO:
    # - https://github.com/scrapy/cssselect (Scrapy converts all CSS selectors to XPath)
    

    ####################################################################################################################
    #####
    #####  DOM nodes
    #####
    
    class Node:
        """"""
        
        tag     = None      # Tag instance whose expand() will be called to post-process the body, in a non-terminal node
        attrs   = None      # list of positional (unnamed) attributes to be passed to tag.expand() during rendering
        kwattrs = None      # dict of keyword (named) attributes to be passed to tag.expand()
        
        body    = None      # DOM (possibly empty) containing child nodes of a non-terminal node; None in DOM.Text
        
        outline = False     # True/False denotes an "outline" block or an "inline" node; adds a leading newline during rendering if True
        indent  = None      # indentation string of this block: absolute (when starts with \n) or relative
                            # to its parent (otherwise); None means this is an inline (headline) block, no indentation
    
        def __init__(self, body = None, indent = None, **params):
            
            # assign secondary parameters
            for name, value in params.items():
                setattr(self, name, value)
                
            # assign a list of body nodes, with flattening of nested lists and filtering of None's
            self.body = DOM(body)
            
            # assign indentation, with proper handling of absolute (in parent) vs. relative (in children) indentations
            self.set_indent(indent)
            
            # assert not self.tag or isinstance(self.tag, Tag)
            
        def __getitem__(self, attr):
            """Return value of a keyword attribute `attr` if present. Raise an exception otherwise. Shortcut for self.kwattrs[attr]."""
            return self.kwattrs[attr]
            
        def get(self, attr, default = None):
            """Return value of a keyword attribute `attr` if present, or `default` otherwise. Shortcut for self.kwattrs.get(attr, default)."""
            return self.kwattrs.get(attr, default) if self.kwattrs else default
            
        def set_outline(self, outline = True):
            self.outline = outline
    
        def set_indent(self, indent):
            """
            Sets absolute indentation on self. This calls relative_indent() on all children
            to make their indentations relative to the parent's.
            """
            self.indent = indent
            if self.indent is not None:
                for child in self.body:
                    child.relative_indent(self.indent)
    
        def relative_indent(self, parent_indent):
            """
            Convert self.indent from absolute to relative by subtracting `parent_indent`.
            If this node is inline (indent=None), the method is called recursively on child nodes.
            """
            if self.indent is None:
                for child in self.body: child.relative_indent(parent_indent)
            elif self.indent[:1] == '\n':
                assert self.indent.startswith(parent_indent)
                self.indent = self.indent[len(parent_indent):]
            else:
                pass        # self.indent is relative already
                
        def render(self):
            
            text = self.outline * '\n' + self._render_body()
            
            # if self.outline and self.indent:
            if self.indent is not None:
                assert self.indent[:1] != '\n'                      # self.indent must have been converted already to relative
                text = add_indent(text, self.indent)                # indentation is only added where \n is present, the 1st line is left untouched!
                # text = text.replace('\n', '\n' + self.indent)
                
            return text
        
        def _render_body(self):
            if not self.tag:
                return self.body.render()
            
            if self.tag.void:
                if self.body: raise VoidTagEx(f"body must be empty for a void tag {self.tag}")
                body = None
            elif self.tag.flat:
                body = self.body.render()
            else:
                body = self.body
                
            return self.tag.expand(body, self.attrs or (), self.kwattrs or {})
            
        def tree(self, indent = '', step = '  '):
            r"""Return a multiline \n-terminated string that presents this node's structure as a tree."""
            
            name = self.tag.name if self.tag else f"<{self.__class__.__name__}>"
            heading = f"{name}"
            
            for attr in self.attrs or []:
                heading += f" {attr}"
            for key, attr in (self.kwattrs or {}).items():
                heading += f" {key}={attr}"
                
            return indent + heading + '\n' + self.body.tree(indent + step, step)

        def walk(self, order = 'preorder'):
            """
            Generator of all nodes inside the tree rooted at self: parent nodes and descendants.
            Parents are yielded before descendants if order='preorder' (default), or after descendants if order='postorder'.
            """
            if order == 'preorder': yield self
            if self.body:
                for node in self.body.walk(order): yield node
            if order == 'postorder': yield self

    class Root(Node):
        """Root node of a Hypertag DOM tree."""
    
        def render(self, drop_line = True):
            """
            If this Root node represents an entire translated document that was originally fed to a Hypertag parser,
            an extra empty line have been prepended by the parser in Grammar.preprocess() and should be removed now
            - set drop_line=True (default) to perform this correction or drop_line=False to skip it.
            """
            output = super(DOM.Root, self).render()
            return output[1:] if drop_line and output.startswith('\n') else output
            # if not output or not drop_line: return output
            # assert output[0] == '\n'
            # return output[1:]
            
    
    class Text(Node):
        """A leaf node containing plain text."""
        
        text = None         # text of this node, either plain text or markup after preprocessing; consists of two parts:
                            #  1) headline (head) - 1st line of `text`, without trailing newline
                            #  2) tailtext (tail) - all lines after the 1st one including the leading newline (!);
                            #     tailtext may contain trailing newline(s), but this is not obligatory
        
        def __init__(self, text = '', **kwargs):
            super(DOM.Text, self).__init__(text = text, **kwargs)
        
        def __str__(self):
            return self.text
            
        def set_indent(self, indent):
            self.indent = indent
    
        def _render_body(self):
            return self.text
    
        # def indent(self, spaces = 1, gap = 0, re_lines = re.compile(r'^(\s*\n)+|\s+$')):
        #     """
        #     Like self.text, but with leading/trailing empty lines removed and indentation fixed at a given number of `spaces`.
        #     Optionally, a fixed number (`gap`) of empty lines are added at the beginning.
        #     """
        #     text = self.text
        #     text = re_lines.sub('', text)           # strip leading and trailing empty lines
        #
        #     # replace current indentation with a `spaces` number of spaces; existing tabs treated like a single space
        #     lines  = text.splitlines()
        #     indent = ' ' * spaces
        #     offset = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
        #     text   = '\n'.join(indent + line[offset:] for line in lines)
        #     return gap * '\n' + text
        
        
