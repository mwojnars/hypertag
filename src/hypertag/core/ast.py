# -*- coding: utf-8 -*-
"""
@author:  Marcin Wojnarski
"""

from __future__ import unicode_literals

import sys, re, codecs, operator
from collections import OrderedDict
from six import reraise, text_type

from parsimonious.grammar import Grammar as Parsimonious
from parsimonious.exceptions import IncompleteParseError

from hypertag.nifty.util import ObjDict
from hypertag.nifty.parsing import ParsimoniousTree as BaseTree

from hypertag.core.errors import SyntaxErrorEx, ValueErrorEx, TypeErrorEx, MissingValueEx, NameErrorEx, \
    UnboundLocalEx, UndefinedTagEx, NotATagEx, NoneStringEx, VoidTagEx, ImportErrorEx
from hypertag.core.grammar import grammar, MARK_TAG, MARK_VAR, TAG, VAR, IS_TAG
from hypertag.core.xml_chars import XML_StartChar, XML_Char, XML_EndChar
from hypertag.core.structs import Context, State, Slot, ValueSlot
from hypertag.core.dom import del_indent, get_indent, DOM
from hypertag.core.tag import Tag, null

DEBUG = False


#####################################################################################################################################################
#####
#####  UTILITIES
#####

_re_decode_escapes = re.compile(r'''
    ( \\U........               # 8-digit hex escapes
    | \\u....                   # 4-digit hex escapes
    | \\x..                     # 2-digit hex escapes
    | \\[0-7]{1,3}              # Octal escapes
    | \\N\{[^}]+\}              # Unicode characters by name
    | \\[\\'"abfnrtv]           # Single-character escapes including "\\"
    )''', re.UNICODE | re.VERBOSE)

def decode_escapes(s):
    r"""
    Decoding of escape characters (\n \t \\ \x.. etc.) inside a string `s`. Handles Unicode correctly.
    Based on: https://stackoverflow.com/a/24519338/1202674
    """
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')
    
    return _re_decode_escapes.sub(decode_match, s)


def duplicate(seq):
    """Any duplicate in a sequence `seq`; or None if no duplicates are present."""
    seen = set()
    dups = set(x for x in seq if x in seen or seen.add(x))
    return dups.pop() if dups else None

def STR(value, node = None, msg = "expression to be embedded in markup text evaluates to None"):
    """Convert `value` to a string for embedding in text markup. Raise NoneStringEx if value=None."""
    if value is None: raise NoneStringEx(msg, node)
    return text_type(value)

def partial(func, *args, **kwargs):
    """
    Create a partial function during processing of a filter pipeline, like in x:fun(a,b)
    - the returned function represents application of (a,b) to a `fun`; whatever argument will be supplied later,
    it will be PREPENDED to the argument list, unlike in functools.partial() which APPENDS new arguments at the end.
    """
    def newfunc(*newargs):
        return func(*(newargs + args), **kwargs)
    return newfunc


#####################################################################################################################################################

class Native(Tag):
    """
    An already-expanded tag created by NODES.xblock_def for insertion into a DOM. Expansion of native tags is done
    before DOM creation, hence expand() - called after DOM creation - only performs body rendering and nothing else.
    """
    def __init__(self, name):
        self.name = name
        
    def expand(self, body, attrs, kwattrs):
        return body.render()


class Hypertag:
    """
    Base class for a hypertag definition block and for hypertags imported from other scripts.
    This class is UNRELATED to the Tag class: its expansion accepts more arguments and is performed
    BEFORE creation of a DOM, not after.
    """
    def expand(self, body, attrs, kwattrs, state, caller):
        raise NotImplementedError

class Imported(Hypertag):
    """
    Wrapper around an imported hypertag. Stores the global state of the imported module,
    so that it can replace the state of the importing module when expand() of the imported hypertag is called.
    """
    def __init__(self, hypertag, module_symbols):
        
        assert isinstance(hypertag, Hypertag)
        self.hypertag = hypertag
        self.module_symbols = module_symbols
        
    def expand(self, body, attrs, kwattrs, state, caller):
        
        module_state = State(self.module_symbols)
        return self.hypertag.expand(body, attrs, kwattrs, module_state, caller)


#####################################################################################################################################################
#####
#####  HYPERTAG GRAMMAR & SCRIPT PREPROCESSING
#####

class Grammar(Parsimonious):
    
    default = None      # class-level default instance of HyML_Parser, the one with standard indentation chars;
                        # can be used for parsing of a given text only if the text doesn't contain any of
                        # special characters that are used in the parser for indent / dedent
    
    SPECIAL_SYMBOLS = ['INDENT_S', 'DEDENT_S', 'INDENT_T', 'DEDENT_T']
    CHARS_DEFAULT   = [u'\u2768', u'\u2769', u'\u276A', u'\u276B']              # indent/dedent special chars to be used in `default` parser
    
    symbols = None      # dict of special symbols: {symbol_name: character}
    
    def __init__(self, special_chars):
        """
        :param special_chars: list of 4 unicode characters that will be used to encode INDENT_* and DEDENT_* symbols;
                              they should not occur in the script to be parsed
        """
        
        assert len(special_chars) == len(self.SPECIAL_SYMBOLS)
        self.symbols = dict(zip(self.SPECIAL_SYMBOLS, special_chars))
        
        placeholders = self.symbols.copy()
        placeholders.update({'XML_StartChar': XML_StartChar, 'XML_Char': XML_Char, 'XML_EndChar': XML_EndChar})
        
        gram = grammar % placeholders
        # print('Hypertag grammar:')
        # print(gram)
        
        super(Grammar, self).__init__(gram)
    
    @staticmethod
    def get_parser(text):
        """
        Return instance of Grammar class suitable for parsing of a given `text`.
        The grammar must be created with a proper choice of special characters,
        ones that don't collide with character set of `text`.
        """
        if not (set(Grammar.CHARS_DEFAULT) & set(text)):
            return Grammar.default
        
        chars = []
        
        # find 4 unicode characters that are not in `text`; start with CHARS_DEFAULT[0]
        code = ord(Grammar.CHARS_DEFAULT[0])
        for _ in range(4):
            while chr(code) in text:
                code += 1
            chars.append(chr(code))
            code += 1
            
        return Grammar(chars)
        
    
    def preprocess(self, text, verbose = False):
        """
        Preprocessing:
        - INDENT_* / DEDENT_* inserted in place of leading spaces/tabs
        - trailing whitespace removed in each line
        - whitespace-only lines replaced with empty lines (\n) and inserted *after* any neighboring DEDENT_*,
          so that DEDENT's always preceed empty lines and the latter can be interpreted as a top margin
          of the following block (rather than a bottom margin of the preceeding block, which would cause
          issues with proper indentation etc.)
        """
        INDENT_S = self.symbols['INDENT_S']
        DEDENT_S = self.symbols['DEDENT_S']
        INDENT_T = self.symbols['INDENT_T']
        DEDENT_T = self.symbols['DEDENT_T']

        lines = ['']            # output lines after preprocessing; empty line prepended for correct parsing of the 1st block's margin;
        linenum = 0             # current line number in input script
        current = ''            # current indentation, as a string
        margin  = 0             # current no. of empty lines that preceed the next block
        
        script = text.split('\n') + ['']            # empty line appended to ensure equal no. of DEDENT as INDENT
        total  = len(script) - 1
        
        for line in script:
            linenum += 1
            line = line.rstrip()                    # trailing whitespace removed
            tail = line.lstrip()
            indent = line[: len(line) - len(tail)]
            
            if not tail and linenum <= total:       # only whitespace in line? add to the `margin`
                margin += 1
                # lines.append('')
                
            # elif tail.startswith('--') or tail.startswith('#'):             # comment line, ignore
            #     pass
            
            else:                                   # code line, convert `indent` to INDENT_*/DEDENT_* characters and insert `tail`
                if indent == current:
                    pass

                elif indent.startswith(current):
                    increment = indent[len(current):]
                    current = indent
                    symbols = ''.join(INDENT_S if char == ' ' else INDENT_T for char in increment)
                    lines[-1] += symbols

                elif current.startswith(indent):
                    decrement = current[len(indent):]
                    current = indent
                    symbols = ''.join(DEDENT_S if char == ' ' else DEDENT_T for char in reversed(decrement))
                    lines[-1] += symbols
                    
                else:
                    raise IndentationError('indentation on line %s is incompatible with previous line' % linenum)
                    
                tail   = margin * '\n' + tail
                margin = 0
                
                lines.append(tail)
                
        assert current == '', "'%s'" % current

        # append remaining empty lines
        output = '\n'.join(lines) + margin * '\n'
        
        # drop terminal empty line that was added initially before the loop start
        assert output[-1] == '\n'
        output = output[:-1]
        
        if verbose:
            print("Grammar.preprocess() output:")
            print('-----')
            print(output)
            print('-----')

        return output
        
        
Grammar.default = Grammar(special_chars = Grammar.CHARS_DEFAULT)


########################################################################################################################################################
#####
#####  NODES
#####

class NODES(object):
    """A lexical container for definitions of all HyML tree node classes."""

    # # modes of rendering & evaluation of subtrees
    # MODE_STRICT = 1         # strict mode: requires that all variables in the subtree are defined (not MISSING), otherwise UndefinedValue exception is raised
    # MODE_NORMAL = 2         # normal mode: None variables are


    ###  BASE NODES  ###

    class node(BaseTree.node):
        indent = None               # indentation length of this node; for debugging
        
        isstatic     = False        # True in <static>, <literal> and their subclasses
        isexpression = False        # True in <expression> and subclasses - nodes that implement evaluate() method
        #iselement    = False        # True in <xelement>, <xhypertag> and other xelement subclasses
        #ishypertag   = None         # HypertagSpec object in all hypertags: <xhypertag> nodes and external hypertag objects/functions
        #isspecial    = False        # True in <special> and subclasses - nodes that mix element/hypertag functionality
        
        ispure       = None         # True if this node's render() is a pure constant function: will always return the exact same value
                                    # regardless of the context of execution and without side effects.
                                    # Is set in analyse() or compactify(), not __init__()!
        
        def check_pure(self):
            """Calculate, set and return self.ispure on the basis of check_pure() of children nodes;
            or return self.ispure if it's already set.
            """
            if self.ispure is not None: return self.ispure
            npure = sum(n.check_pure() for n in self.children)      # sum up the no. of True values among children
            self.ispure = (npure == len(self.children))             # is pure only when all children have pure=True
            return self.ispure
        
        def compactify(self, state):
            """Replace pure nodes in the subtree rooted at 'self' with static string/value nodes containg pre-computed render() result
            of a given node, so that this pre-computed string/value is returned on all future render() calls on the new node.
            Compactification is a kind of pre-rendering: whatever can be rendered in the tree before runtime variable values are known,
            is rendered and stored in the tree as static values.
            'state' is needed for render() calls because the subtree may need to push some local variables internally.
            """
            # push compactification down the tree
            for c in self.children: c.compactify(state)
            
        def compactify_self(self, state):
            "If 'self' is pure and not static, compactify it, otherwise try to compactify children. Return the new node or self."
            if self.isstatic: return self
            if self.check_pure(): return NODES.merged(self, state)
            self.compactify(state)
            return self
            
        def analyse(self, ctx):
            """
            `ctx` is an instance of Context. For read access, it can be used like a dict
            of current name->node mappings. NOTE: `ctx` contains symbols, not just raw names,
            every symbol being a concatenation of a name and a namespace qualifier (a tag or a variable),
            see TAG() and VAR() functions.
            """
            for c in self.children: c.analyse(ctx)

        # @staticmethod
        # def _translate_all(nodes, state):
        #     return DOM(n.translate(state) for n in nodes)

        @staticmethod
        def _render_all(nodes, state):
            return u''.join(n.render(state) for n in nodes)
            
        def __str__(self): return "<%s>" % self.__class__.__name__  #object.__str__(self)

    class static(node):
        """
        A node that represents static text outside expressions; its self.value is already known
        during analysis, before translate() is called. See also: class literal (for static values in expressions).
        """
        isstatic = True
        ispure   = True
        value    = None
        
        def setup(self):            self.value = self.text()
        def analyse(self, ctx):     pass
        def translate(self, state): return DOM.text(self.value) if self.value else DOM()
        def render(self, state):    return self.value
        def __str__(self):          return self.value
        
    class artificial(node):
        """Base class for artificial nodes added to the AST after parsing: during analysis or compactification."""
        type = '_artificial_'
        
        def __init__(self, origin):
            self.pos = origin.pos
            self.tree = origin.tree
            self.fulltext = origin.fulltext


    class xdocument(node):
        
        slots_in  = None    # dict of slots created for each default value to be imported into `ctx` upon startup
        slots_out = None    # dict of top-level symbols defined by this document, and their Slots: {symbol: slot}
        globals   = None    # dict of global symbols to be automatically imported into `ctx` when analysis begins
        
        # def setup(self):
        #     self.predefined = {}
        
        def predefine(self, globals):
            """
            Append `symbols` to a dict of predefined symbols that will be available to child blocks
            right from the beginning of document parsing.
            """
            if globals: self.globals = globals
        
        def analyse(self, ctx):
            self.slots_in = {symbol: ValueSlot(symbol, value, ctx) for symbol, value in self.globals.items()}
            ctx.pushall(self.slots_in)
            position = ctx.position()
            for c in self.children: c.analyse(ctx)
            self.slots_out = ctx.asdict(position)           # pull newly defined top-level symbols from the tree

        def translate(self, state):
            """
            Because <xdocument> is the root of every AST, its translate() is unusual, in that it returns a triple:
            - DOM.Root node of the final DOM generated as a result of translation of the entire AST
            - dict of top-level symbols indexed by their names: {symbol_name: value}
            - dict of top-level symbols indexed by slots: {slot: value}, for use as an initial state
              in case some hypertags get imported by other Hypertag documents and need to be expanded
              in the original (final) state of the model they were defined in
            """
            for slot in self.slots_in.values(): slot.set_value(state)
            nodes = [c.translate(state) for c in self.children]
            hroot = DOM.Root(body = nodes, indent = '\n')
            hroot.indent = ''       # fix indent to '' instead of '\n' after all child indents have been relativized
            
            # pull actual values of top-level output symbols
            symbols   = {}
            state_out = {}
            for symbol, slot in self.slots_out.items():
                try:
                    symbols[symbol] = value = slot.get(state)
                    state_out[slot] = value
                    
                except KeyError:            # some top-level slots may remain uninitialized if defined inside a control block (if/for/...)
                    continue
                    
            return hroot, symbols, state_out

        # def compactify(self, state):
        #     # if DEBUG: print("compact", "DOC", state)
        #     self.children = NODES._compactify_siblings_(self.children, state)


    ###  BLOCKS  ###

    class xblock(node):
        """Wrapper around all specific types of blocks: adds top margin and marks "outline" mode for the first returned DOM node."""
        modifier = None         # optional modifier of layout  ("<", "...") that preceeds the block
        block    = None         # the actual inner block of a specific type
        
        def setup(self):
            assert 2 <= len(self.children) <= 3 and self.children[0].type == 'margin_out'
            if len(self.children) == 3:
                self.modifier = self.children[1].value
                del self.children[1]                    # for translate() there must remain 2 children: [margin, block]
            self.block = self.children[-1]
            
        def analyse(self, ctx):
            
            # check if we're possibly moving out of the document prolog
            if ctx.in_prolog and self.block.type not in ('block_comment', 'block_context'):
                ctx.in_prolog = False

            super(NODES.xblock, self).analyse(ctx)

        def translate(self, state):
            margin, block = (c.translate(state) for c in self.children)
            if not block: return margin
            
            append = (self.modifier == '...')
            dedent = (self.modifier == '<')
            
            if not append:
                block[0].set_outline()            # mark the 1st node of the block as being "outline" not "inline"
            if dedent:
                block.set_indent('')
            return DOM(margin, block)
            
    class block_text(node):

        def translate(self, state):
            return DOM.text(self.render(state), indent = state.indentation)
            
        def render(self, state):

            # temporarily reset indentation to zero for rendering of children; this will be reverted later on
            indent = state.indentation
            state.indentation = ''
            
            lead = self.column          # horizontal position where the block's first line begins in the script
            try:
                body = self._render_all(self.children, state)
                # if body.startswith('\n'):
                #     output = body[1:]                   # no headline? drop the leading newline
                # else:
                output = ' ' * lead + body          # in the headline, spaces are prepended to replace leading tag(s) and a marker character /|!
            finally:
                state.indentation = indent

            sub_indent = get_indent(output)
            sub_indent = sub_indent[:lead+1]        # max 1 initial space/tab after the lead is dropped; remaining sub-indentation is preserved in `output`
            output = del_indent(output, sub_indent)
            # print('sub_indent: "{sub_indent}"')

            # if tail lines have shorter indent than the headline, drop all the lead + 1 space (gap)
            if len(sub_indent) < lead:
                drop = lead - len(sub_indent)
                if output[drop:drop+1] == ' ': drop += 1
                output = output[drop:]
                
            # # drop the 1st line (headline) if empty
            # if output.split('\n', 1)[0].strip() == '':
            #     output =
            
            return output

    class xblock_markup(block_text): pass
    class xblock_normal(block_text): pass
    class xblock_verbat(block_text): pass
    class xblock_comment(block_text):
        def translate(self, state): return DOM()
        def render(self, state):    return ""
    
    class xblock_embed(node):
        """Embedding of DOM nodes through @... type of expression."""
        expr = None
        
        def setup(self):
            self.expr = self.children[0]
            
        def translate(self, state):
            body = self.expr.evaluate(state)
            body = self._as_sequence(body)
            body.set_indent(state.indentation)                  # set indentation of the fragment to be inserted
            return body
        
        def _as_sequence(self, body):
            if isinstance(body, DOM): return body
            if isinstance(body, DOM.Node): return DOM(body)
            try:
                body = list(body)
            except Exception as ex:
                raise TypeErrorEx("embedded @-expression evaluates to %s instead of a DOM or DOM.Node or an iterable of DOM.Node's" % type(body), self)
            return DOM(*body)

    class xblock_struct(node):
        tags = None         # <tags_expand> node
        body = None         # <body_struct> node
        
        def setup(self):
            self.tags = self.children[0]
            self.body = self.children[1]
            assert self.tags.type == 'tags_expand'
            
        def analyse(self, ctx):
            ctx.regular_depth += 1
            position = ctx.position()
            for c in self.children: c.analyse(ctx)
            ctx.reset(position)             # tagged node defines a local namespace, hence need to drop symbols defined inside
            ctx.regular_depth -= 1
            
        def translate(self, state):
            body = self.body.translate(state)
            body = self.tags.apply_tags(state, body)
            body.set_indent(state.indentation)
            return body

    class xblock_def(node, Hypertag):
        """Definition of a native hypertag."""
        name       = None
        attrs      = None           # all attributes as a list of children nodes, including @body
        attr_body  = None           # the @body node if present, otherwise None
        attr_names = None           # names of all attributes, including @body, as a dict {name: node}
        attr_regul = None           # all regular (non-body) attributes, as a list of children
        body       = None
        slot       = None
        native     = None           # a Native tag instance that will be inserted into all DOMs
        
        def setup(self):
            self.name  = self.children[0].value
            self.attrs = self.children[1:-1]
            self.body  = self.children[-1]
            assert all(attr.type.startswith('attr_') for attr in self.attrs)
            
            self.attr_names = {attr.name: attr for attr in self.attrs}

            # TODO: check that attr names are Python identifiers (name_id), otherwise they can't be used in expressions
            
            # check that attr names are unique
            if len(self.attr_names) < len(self.attrs):
                raise SyntaxErrorEx("duplicate attribute '%s' in hypertag definition '%s'" % (duplicate(self.attrs), self.name), self)
            
            # pick body attribute (attr_body) and the remaining list of regular attributes (attr_regul)
            if self.attrs and self.attrs[0].body:
                self.attr_body  = self.attrs[0]
                self.attr_regul = self.attrs[1:]
            else:
                self.attr_regul = self.attrs
            
            # create a Native tag that will be inserted into DOMs
            self.native = Native(self.name)
            
        def analyse(self, ctx):
            if ctx.control_depth >= 1: raise SyntaxErrorEx('hypertag definition inside a control block is not allowed', self)
            
            ctx.regular_depth  += 1
            ctx.hypertag_depth += 1
            position = ctx.position()
            
            for attr in self.attrs:                 # analyse default-value expressions of attributes
                attr.analyse(ctx)

            for attr in self.attrs:                 # declare attributes as local variables for subsequent analysis of self.body
                attr.declare_var(ctx)

            self.body.analyse(ctx)                  # analyse the formal body

            ctx.reset(position)
            ctx.hypertag_depth -= 1
            ctx.regular_depth  -= 1

            symbol = TAG(self.name)
            self.slot = ValueSlot(symbol, self, ctx)
            ctx.push(symbol, self.slot)
            
        def translate(self, state):
            self.slot.set_value(state)
            return None                 # hypertag produces NO output in the place of its definition (only in places of occurrence)

        def expand(self, body, attrs, kwattrs, state, caller):
            """
            Translate the formal self.body in a given `state`, insert the actual `body` wherever necessary,
            and return as a DOM (not a string!) for possible further manipulation in other hypertags.
            """
            dom_attrs = self._append_attrs(body, attrs, kwattrs, state, caller)         # extend `state` with actual values of tag attributes
            output = self.body.translate(state)
            output.set_indent(state.indentation)
            # return output
            
            if output: output[0].set_outline(False)         # node's `outline` will be set for the root node up in xblock.translate()
            return DOM.node(output, state.indentation, tag = self.native, kwattrs = dom_attrs)

        def _append_attrs(self, body, attrs, kwattrs, state, caller):
            """Extend `state` with actual values of tag attributes."""

            # verify no. of positional attributes & names of keyword attributes
            if len(attrs) > len(self.attr_regul):
                raise TypeErrorEx("hypertag '%s' takes %s positional attributes but %s were given" % (self.name, len(self.attr_regul), len(attrs)), caller)
            if self.attr_body and self.attr_body.name in kwattrs:
                raise TypeErrorEx("direct assignment to body attribute '%s' of hypertag '%s' is not allowed" % (self.attr_body.name, self.name), caller)
            
            # translate attribute names in `kwattrs` to nodes as keys
            try:
                kwattrs = {self.attr_names[name]: value for name, value in kwattrs.items()}
            except KeyError as ex:
                name = ex.args[0]
                raise TypeErrorEx("hypertag '%s' got an unexpected keyword attribute '%s'" % (self.name, name), caller)

            dom_attrs = {}
            dom_kwattrs = {attr.name: value for attr, value in kwattrs.items()}
            
            # move positional attributes to `kwattrs`
            for pos, value in enumerate(attrs):
                attr = self.attr_regul[pos]
                if attr in kwattrs: raise TypeErrorEx("hypertag '%s' got multiple values for attribute '%s'" % (self.name, attr.name), caller)
                kwattrs[attr] = value
                dom_attrs[attr.name] = value

            dom_attrs.update(dom_kwattrs)
            # dom_attrs = {attr.name: value for attr, value in kwattrs.items()}
            
            # impute missing values with defaults
            for attr in self.attr_regul:
                if attr not in kwattrs:
                    if attr.expr is None: raise TypeErrorEx("hypertag '%s' missing a required positional attribute '%s'" % (self.name, attr.name), caller)
                    kwattrs[attr] = attr.expr.evaluate(state)
                    
            # transfer attribute values from `kwattrs` to `state`
            for attr, value in kwattrs.items():
                attr.assign(state, value)
            # state.update(kwattrs)
            
            # append `body` to `state`
            if self.attr_body:
                self.attr_body.assign(state, body)
                # state[self.attr_body] = body
            elif body:
                raise VoidTagEx("non-empty body passed to a void hypertag '%s'" % self.name, caller)
            
            return dom_attrs
            
    class xblock_import(node):
        """"""
        path  = None            # import path string; optional
        items = None            # list of 1+ nodes of type <xwild_import> or <xname_import>
        
        def setup(self):
            if self.children[0].type == 'path_import':
                self.path  = self.children[0].value
                self.items = self.children[1:]
            else:
                self.items = self.children
            for item in self.items:
                item.path = self.path
                
        def analyse(self, ctx):
            if ctx.control_depth >= 1: raise SyntaxErrorEx('import inside a control block is not allowed', self)
            super(NODES.xblock_import, self).analyse(ctx)

        def translate(self, state):
            for item in self.items: item.translate(state)
            return DOM()
        
    class _import(node):
        def _import(self, path):
            runtime = self.tree.runtime
            module  = self.tree.module
            return runtime.import_module(path, module, self)
        
    class xwild_import(_import):
        path    = None          # path string as specified in the "from" clause
        slots   = None          # dict of symbols and their slots created during analysis
        
        def analyse(self, ctx):
            module = self._import(self.path)

            # exclude private symbols AND wrap up all native tag definitions within Imported
            # to preserve original runtime state of their module, for expand()
            symbols = {name: Imported(value, module.state) if (IS_TAG(name) and isinstance(value, Hypertag)) else value
                       for name, value in module.symbols.items() if name[1] != '_'}
            
            self.slots = {symbol: ValueSlot(symbol, value, ctx) for symbol, value in symbols.items()}
            ctx.pushall(self.slots)

        def translate(self, state):
            for slot in self.slots.values(): slot.set_value(state)
            
    class xname_import(_import):
        path  = None        # path string as specified in the "from" clause
        slot  = None        # <slot> that will keep value of this imported symbol
        
        def analyse(self, ctx):
            assert self.path
            symbol  = self.children[0].value                        # original symbol name with leading % or $
            rename  = (symbol[0] + self.children[1].value) if len(self.children) == 2 else symbol
            module  = self._import(self.path)

            if symbol not in module.symbols: raise ImportErrorEx("cannot import '%s' from a given path (%s)" % (symbol, self.path), self)
            value = module.symbols[symbol]
            
            if IS_TAG(symbol) and isinstance(value, Hypertag):
                value = Imported(value, module.state)
            
            self.slot = ValueSlot(rename, value, ctx)
            ctx.push(rename, self.slot)

        def translate(self, state):
            self.slot.set_value(state)

    class xblock_context(xblock_import):
        """
        Wrapper-block around `context` imports (xcntx_import). Checks whether the block is placed
        at the beginning of a document (in document's prolog).
        """
        def analyse(self, ctx):
            if not ctx.in_prolog: raise SyntaxErrorEx('context block(s) must be the first block(s) in a document (after comments)', self)
            super(NODES.xblock_import, self).analyse(ctx)

    class xcntx_import(node):
        """Like <xname_import> but imports the name from a dynamic context rather than from a module."""
        slot  = None        # <slot> that will keep value of the symbol
        
        def analyse(self, ctx):
            context = self.tree.context
            symbol  = self.children[0].value                            # original symbol name with leading % or $
            rename  = (symbol[0] + self.children[1].value) if len(self.children) == 2 else symbol
            
            if symbol not in context: raise ImportErrorEx("symbol '%s' not found in context" % symbol, self)
            value = context[symbol]
            self.slot = ValueSlot(rename, value, ctx)
            ctx.push(rename, self.slot)

        def translate(self, state):
            self.slot.set_value(state)

        
    class control_block(node):
        """
        Base class for if/try/for/while blocks. Inside these blocks, the execution may proceed through 2 or more different
        paths (one of them being the "null" branch) and for this reason they require special handling during analysis.
        """
        # slot_maps = None        # list of slot mappings for every branch including the null branch (-1); each mapping
        #                         # is a dict of {input_or_local_slot: output_slot} pairs; values are copied
        #                         # from input/local to output slots after translation of the block
        
        def analyse(self, ctx):
            ctx.control_depth += 1
            self._analyse_branches(ctx)
            ctx.control_depth -= 1

        def _analyse_branches(self, ctx):
            """
            Unlike a regular tagged block, if/try block does NOT introduce a new namespace,
            so all symbols defined in branches must be made visible to sibling nodes that go after the block.
            Moreover, if a variable is (re)declared multiple times in separate branches, all these declaraions
            (i.e., their corresponding slots) must be mapped onto a single shared outgoing slot.
            Also, if any of the locally-defined variables overrides an existing variable defined before the block,
            the incoming variable must be mapped onto an outgoing slot, as well, for proper handling of a "null branch" execution
            (i.e., the situation when no code of this block gets executed, like in an empty loop or a failed "try" block).
            """
            # # list of dicts of symbols and local slots defined in each subsequent branch, including the "null" branch at [-1]
            # local_slots = []
            # new_symbols = []
            
            for i, branch in enumerate(self.children):
                position = ctx.position()
                branch.analyse(ctx)
                symbols = ctx.asdict(position)          # top-level symbols declared in this branch...
                ctx.reset(position)
                ctx.pushnew(symbols)                    # ...only new symbols (not declared in a previous branch) are added
                
                # local_slots.append(symbols)
                # new_symbols += symbols.keys()
                
            # if not new_symbols: return
            # new_symbols = set(new_symbols)
            #
            # # [-1] contains symbols of the "null" branch, they will be copied from incoming slots when no clause is executed
            # null_slots = {symbol: ctx[symbol] for symbol in new_symbols if symbol in ctx}
            # local_slots.append(null_slots)
            #
            # # create outgoing slots for all newly defined variables
            # output_slots = {symbol: Slot(symbol, ctx) for symbol in new_symbols}
            #
            # mapping_default = {input_slot: output_slots[symbol] for symbol, input_slot in null_slots.items()}
            #
            # def match(slots):
            #     mapping_branch = {local_slot: output_slots[symbol] for symbol, local_slot in slots.items()}
            #     mapping = mapping_default.copy()
            #     mapping.update(mapping_branch)
            #     return mapping
            #
            # # set up mappings from local/incoming slots to outgoing slots for each branch separately including the "null" branch
            # self.slot_maps = list(map(match, local_slots))
            #
            # ctx.pushall(output_slots)
            
        # def _fill_slots(self, branch, state):
        #     """Fill out outgoing slots according to what execution branch (0..N-1) has been selected; -1 is the "null" branch.
        #     """
        #     # for slot in self.output_slots:
        #     #     slot.set_value(branch, state)
        #     mapping = self.slot_maps[branch]
        #     for in_slot, out_slot in mapping.items():
        #         value = in_slot.get(state)
        #         out_slot.set(state, value)
        
        def _select_branch(self, state):
            raise NotImplementedError
        
        def translate(self, state):
            body, branch = self._select_branch(state)
            # self._fill_slots(branch, state)
            body.set_indent(state.indentation)
            return body
        

    class xblock_try(control_block):
        """
        A "try" block. Two syntax forms available:
        - short form:   ?tag... ?|...
        - long form:    try ... else ... else ...
        Every "try" block catches ALL exceptions that inherit from Exception class, including all Hypertag exceptions.
        There is no way to explicitly restrict the scope of exceptions caught (no "except" clause), unlike in Python.
        The block does NOT catch special exceptions that inherit directly from BaseException:
        SystemExit, KeyboardInterrupt, GeneratorExit.
        Note that the meaning of the "else" clause is OPPOSITE to what it is in Python: here, "else" branch
        is executed if all preceeding try/else branches failed with exceptions.
        If all branches fail, including the last one, empty output is rendered (exception from the last branch is NOT re-raised).
        """
        def _select_branch(self, state):
            for i, branch in enumerate(self.children):
                try:
                    return branch.translate(state), i
                except Exception as ex:
                    pass
            return DOM(), -1
    
    class xblock_if(control_block):
        clauses  = None         # list of 1+ <clause_if> nodes
        elsebody = None         # optional <body_*> node for the "else" branch
        
        def setup(self):
            if self.children[-1].type == 'clause_if':
                self.clauses = self.children
            else:
                self.clauses = self.children[:-1]
                self.elsebody = self.children[-1]

        def _select_branch(self, state):
            for i, clause in enumerate(self.clauses):
                if clause.test.evaluate(state):
                    return clause.translate(state), i
            if self.elsebody:
                return self.elsebody.translate(state), -2
            return DOM(), -1
        
    class xclause_if(node):
        test = None             # <expression> node containing a test to be performed
        body = None             # <body> to be rendered if the clause is positive
        def setup(self):
            assert 1 <= len(self.children) <= 2
            self.test = self.children[0]
            self.body = self.children[1] if len(self.children) == 2 else None
        def translate(self, state):
            return self.body.translate(state) if self.body else DOM()
        # def render(self, state):
        #     return self.body.render(state)
        
    class xblock_while(control_block):
        def _analyse_branches(self, ctx):
            self.children[0].analyse(ctx)
        def translate(self, state):
            out = []
            clause = self.children[0]
            while clause.test.evaluate(state):
                body = clause.translate(state)
                out += body.nodes
            # return DOM(*out), 0
            out = DOM(*out)
            out.set_indent(state.indentation)
            return out
        
    class xblock_for(control_block):
        targets = None              # 1+ loop variables to assign to
        expr    = None              # loop expression that returns a sequence (iterable) to be looped over
        body    = None
        
        def setup(self):
            self.targets, self.expr = self.children[:2]
            self.body = self.children[2] if len(self.children) == 3 else None
            assert isinstance(self.expr, NODES.expression)
            assert self.targets.type == 'targets'
            # assert self.targets.type == 'var', 'Support for multiple targets in <for> not yet implemented'
            
        def _analyse_branches(self, ctx):
            self.expr.analyse(ctx)
            self.targets.analyse(ctx)
            if self.body: self.body.analyse(ctx)

        def translate(self, state):
            out = []
            sequence = self.expr.evaluate(state)
            for value in sequence:                  # translate self.body multiple times, once for each value in `sequence`
                self.targets.assign(state, value)
                if self.body:
                    body = self.body.translate(state)
                    out += body.nodes
                
            out = DOM(*out)
            out.set_indent(state.indentation)
            return out

    class xblock_assign(node):
        targets = None
        inplace = None          # symbol of in-place arithmetic operator to apply (+-*/), optional
        expr    = None
        oper    = None          # 2-arg function that implements `inplace` operator
        
        opers   = {'+':  operator.add,
                   '-':  operator.sub,
                   '*':  operator.mul,
                   '%':  operator.mod,
                   '/':  getattr(operator, 'div', None) or operator.truediv,
                   '//': operator.floordiv,
                   '<<': operator.lshift,
                   '>>': operator.rshift,
                   '&':  operator.and_,
                   '|':  operator.or_,
                   '^':  operator.xor,
        }
        
        def setup(self):
            assert 2 <= len(self.children) <= 3
            self.targets  = self.children[0]
            self.expr     = self.children[-1]

            # in-place operator-assignment ?
            if len(self.children) == 3:
                inplace   = self.children[1].value
                self.oper = self.opers[inplace]
                if self.targets.is_augmented():
                    raise SyntaxErrorEx("illegal expression %s= for augmented assignment" % inplace, self)
                self.targets.set_inplace()
            
        def analyse(self, ctx):
            self.expr.analyse(ctx)
            self.targets.analyse(ctx)

        def translate(self, state):
            value = self.expr.evaluate(state)
            if self.oper:
                current = self.targets.evaluate(state)
                value   = self.oper(current, value)
            self.targets.assign(state, value)
            return None
    
    class xtargets(node):
        def is_augmented(self):
            """True if self represents multiple targets (not a plain variable) to assign to."""
            return len(self.children) >= 2 or self.children[0].type != 'var_def'
        
        def set_inplace(self):
            self.children[0].set_inplace()
            
        def analyse(self, ctx):
            """Recursively insert all variables that comprise this target into context."""
            for c in self.children: c.analyse(ctx)

        def assign(self, state, value):
            """Unpack `value` and assign to child targets."""
            N = len(self.children)
            if N == 1:
                self.children[0].assign(state, value)
                return
            
            # unpack and assign to multiple child targets
            i = 0
            for i, v in enumerate(value):               # raises TypeError if `value` is not iterable
                if i >= N: raise ValueErrorEx("too many values to unpack (expected %s)" % N, self)
                self.children[i].assign(state, v)
            if i+1 < N:
                raise ValueErrorEx("not enough values to unpack (expected %s, got %s)" % (N, i+1), self)
            
        def evaluate(self, state):
            assert len(self.children) == 1
            return self.children[0].evaluate(state)
            
            
    ###  BODY & LINES  ###

    class body(node):
        def translate(self, state):
            return DOM(n.translate(state) for n in self.children)
            # return self._translate_all(self.children, state)
    
    class xbody_control(body): pass
    class xbody_struct (body): pass

    class line(node):
        def translate(self, state):
            return DOM.text(self.render_inline(state))
        def render(self, state):
            return state.indentation + self.render_inline(state)
        def render_inline(self, state):
            """Render contents of the line, i.e., everything except boundary (indentation, margin). Implemented by subclasses."""
            raise NotImplementedError

    class xline_verbat(line):
        def render_inline(self, _):
            return self.text()

    class xline_normal(line):
        def render_inline(self, state):
            assert len(self.children) == 1
            child = self.children[0]
            assert child.type == 'line_markup'
            text = child.render_inline(state)                   # this calls xline_markup.render_inline()
            # escape = self.tree.config['escape_function']
            escape = self.tree.runtime.escape
            return escape(text) if escape else text

    class xline_markup(line):
        def render_inline(self, state):
            markup = self._render_all(self.children, state)     # renders embedded expressions, in addition to static text
            return markup

    
    ###  TAGS & HYPERTAGS  ###

    class xtags_expand(node):
        """List of tag_expand nodes."""
        def apply_tags(self, state, body):
            """Wrap up the translated `body` (a DOM, not AST) with subsequent tags processed (expanded) in reverse order."""
            for tag in reversed(self.children):
                body = tag.translate_tag(state, body)
            return body
        
    class xtag_expand(node):
        """
        Occurrence of a tag.
        NOTE #1: unnamed attrs can be *mixed* with named ones (unlike in python) -
                 during tag expansion all unnamed attrs are passed first to a tag, followed by all named (keyword-) ones
        NOTE #2: same attr can appear more than once, in such case its values (must be strings!) get space-concatenated;
                 this is particularly useful for "class" attibute and its short form:  div .top.left.darkbg
        """
        DEFAULT = "div"     # default `name` when no tag name was provided (a shortcut was used: .xyz or #xyz); UNUSED!
        name  = None        # tag name: a, A, h1, div ...
        tag   = None        # resolved definition of this tag, as a Tag or Hypertag (xblock_def) instance; or a Slot
        attrs = None        # 0+ list of <attr_short> and <attr_val> nodes
        unnamed = None      # list of <expression> nodes of unnamed attributes from `attrs`
        named   = None      # list of (name, expression) pairs of named attributes from `attrs`; duplicate names allowed
        
        def setup(self):
            
            # retrieve `name` of this tag
            head = self.children[0]
            if head.type == 'name_id':
                self.name = head.value
                self.attrs = self.children[1:]
            else:
                self.name = self.DEFAULT
                self.attrs = self.children
                
            self.unnamed = []
            self.named = []
            
            # collect attributes: their names (optional) and expressions (obligatory);
            for attr in self.attrs:
                name = attr.name
                expr = attr.expr
                if name is None:
                    if self.named: raise SyntaxErrorEx("positional argument follows keyword argument")
                    self.unnamed.append(expr)
                else:
                    # if name in self.named: raise SyntaxErrorEx("attribute '{name}' appears twice on attributes list of tag '{self.name}'", attr)
                    self.named.append((name, expr))
                
        def analyse(self, ctx):
            
            for c in self.attrs: c.analyse(ctx)
            self.tag = ctx.get(TAG(self.name))
            if self.tag is None: raise UndefinedTagEx("undefined tag '%s'" % self.name, self)
            
        def translate_tag(self, state, body):
            """
            translate_tag() differs from a regular translate() in that it accepts `body` additionaly.
            The actual `body` is already translated and has a form of a DOM.
            """
            attrs, kwattrs = self._eval_attrs(state)            # calculate actual values of attributes
            
            assert isinstance(self.tag, Slot)
            tag = self.tag.get(state)

            if isinstance(tag, Hypertag):
                return tag.expand(body, attrs, kwattrs, state, self)
            
            elif isinstance(tag, Tag):
                return DOM.node(body, tag = tag, attrs = attrs, kwattrs = kwattrs)
            
            else:
                raise NotATagEx("Not a tag: '%s' (%s)" % (self.name, tag.__class__), self)
            
        def _eval_attrs(self, state):
            unnamed = [attr.evaluate(state) for attr in self.unnamed]
            
            named = {}
            for name, expr in self.named:
                value = expr.evaluate(state)
                if name in named:
                    named[name] += ' ' + value       # = '{named[name]} {value}'
                else:
                    named[name] = value
                    
            return unnamed, named
            
    class xnull(node):
        def translate_tag(self, state, body):
            return DOM.node(body, tag = null)
        
    class xpass(node):
        def translate(self, state):
            return DOM()
        

    ###  ATTRIBUTES & ARGUMENTS  ###
    
    class attribute(node):
        """Attribute inside a hypertag occurrence OR tag definition:
            unnamed / named / short (only in tag occurence) / obligatory / body (only in tag definition).
        """
        name = None         # [str] name of this attribute; None if unnamed
        expr = None         # <expression> node of this attribute; None if no expression present (attr definition with no default)
        body = False        # True in xattr_body
        slot = None         # Slot that identifies this variable inside `state`
        
        def declare_var(self, ctx):
            symbol = VAR(self.name)
            self.slot = Slot(symbol, ctx)
            ctx.push(symbol, self.slot)
        
        def assign(self, state, value):
            self.slot.set(state, value)
        
    # in-definition attributes:  xattr_body, xattr_def
    
    class xattr_body(attribute):
        body = True
        def setup(self):
            assert len(self.children) == 1
            self.name = self.children[0].value          # <name_id>
            
    class xattr_def(attribute):
        def setup(self):
            assert 1 <= len(self.children) <= 2
            self.name = self.children[0].value          # <name_xml>
            if len(self.children) == 2:
                self.expr = self.children[1]
            
    # in-occurrence attributes:  xattr_named, xattr_unnamed, xattr_short
    
    class xattr_named(attribute):
        def setup(self):
            assert len(self.children) == 2
            self.name = self.children[0].value          # <name_xml>
            self.expr = self.children[1]
            
    class xattr_unnamed(attribute):
        def setup(self):
            assert len(self.children) == 1
            self.expr = self.children[0]
            
    class xattr_short(attribute):
        def setup(self):
            symbol = self.fulltext[self.pos[0]]
            assert symbol in '.#'
            self.name = 'class' if symbol == '.' else 'id'
            assert len(self.children) == 1
            self.expr = self.children[-1]
        
    class xkwarg(node):
        name = None
        expr = None
        
        def setup(self):
            assert len(self.children) == 2
            assert self.children[0].type == 'name_id'
            self.name = self.children[0].value
            self.expr = self.children[1]
            
        def evaluate(self, state):
            return self.expr.evaluate(state)
        

    ###  EXPRESSIONS - ROOT NODES  ###
    
    class expression(node):
        """Base class for all nodes that represent an expression, or its part (a subexpression)."""
        
        qualifier = None            # optional qualifier: ? or ! ... used only in a few node types
        
        def evaluate(self, state):
            raise NotImplementedError

        def evaluate_with_qualifier(self, state):
            """Special variant of evaluate() to be used in these expression nodes that may have a not-None qualifier.
               They should call this method in evaluate() and implement _eval_inner_qualified().
            """
            try:
                val = self._eval_inner_qualified(state)
            except Exception as ex:
                if self.qualifier == '?': return ''
                else: raise
            
            if val: return val
            
            # `val` is false ... check qualifiers to undertake appropriate action
            if self.qualifier == '?': return ''
            if self.qualifier == '!': raise MissingValueEx("Obligatory expression evaluates to a false value (%s)" % repr(val), self)
            return val

        def _eval_inner_qualified(self, state):
            raise NotImplementedError


    class expression_root(expression):
        """Base class for root nodes of all non-literal embedded expressions, either in markup or attribute/argument lists.
        """
        qualifier = None        # optional qualifier: ? or !
        context   = None        # copy of Context that has been passed to this node during analyse(); kept for re-use by render(),
                                # in case if the expression evaluates to yet another (dynamic) piece of Hypertag code
        def setup(self):
            # see if there is a qualifier added as a sibling of this node
            if self.sibling_next and self.sibling_next.type == 'qualifier':
                self.qualifier = self.sibling_next.text()
        
        def render(self, state):
            """Rendering is invoked only for a root node of an expression embedded in xline_* node of text."""
            return STR(self.evaluate(state), self)
        
        def evaluate(self, state):
            return self.evaluate_with_qualifier(state)
        
        def _eval_inner_qualified(self, state):
            assert len(self.children) == 1
            return self.children[0].evaluate(state)

    class xexpr(expression_root): pass
    class xexpr_var(expression_root): pass
    class xexpr_factor(expression_root): pass
    class xexpr_strict(expression_root): pass
    class xexpr_augment(expression_root): pass
    class xexpr_bitwise(expression_root): pass
    
    class variable(expression):
        """Common code for both a variable's definition (xvar_def) and a variable's occurrence (xvar_use)."""
        name  = None
        read  = False       # True in <xvar_use> and this <xvar_def> which performs in-place operation
        write = False       # True in <xvar_def> and <attribute>
        
        slot_read  = None       # Slot that identifies this variable inside `state` for read access
        slot_write = None       # Slot that identifies this variable inside `state` for write access
        
        # slot_read & slot_write may reference different Slots, e.g., in a reassignment block that overrides a name defined upper in the doc:
        #   $x = 1
        #   div:
        #      $x += 1        -- this <variable> reads "x" from the upper level and assigns a new "x" in a narrower name scope, hence a new Slot is needed
        
        def setup(self):
            self.name = self.text()
            if self.name[0] == '$':                     # preceeding $ is allowed inside {...} and should be truncated here
                self.name = self.name[1:]
        
        def analyse(self, ctx):
            symbol = VAR(self.name)
            slot   = ctx.get(symbol)
            assert slot is None or isinstance(slot, Slot), "not a slot: %s in %s" % (type(slot), self.name)

            if self.read:
                if slot is None: raise NameErrorEx("variable '%s' is not defined" % self.name, self)
                self.slot_read = slot
            
            if self.write:
                if slot and slot.depth == ctx.regular_depth:
                    self.slot_write = slot
                else:
                    self.slot_write = Slot(symbol, ctx)
                    ctx.push(symbol, self.slot_write)
            
        def evaluate(self, state):
            
            assert self.read
            try:
                return self.slot_read.get(state)
            
            except KeyError:
                raise UnboundLocalEx("variable '%s' referenced before assignment" % self.name, self)

        def assign(self, state, value):
            assert self.write
            self.slot_write.set(state, value)

    class xvar_use(variable):
        """Occurence (use) of a variable."""
        read = True

    class xvar_def(variable):
        """Definition of a variable, or assignment to a previously defined variable."""
        write = True
        
        def set_inplace(self):
            """Mark this definition as occuring in an in-place assignment (+= -= etc.) so the variable will be
               used in read access, not only for writing.
            """
            self.read = True
        

    ###  EXPRESSIONS - TAIL OPERATORS  ###
    
    class tail(node):
        """Tail operators implement apply() instead of evaluate()."""
        def apply(self, obj, state):
            raise NotImplementedError

    class xcall(tail):
        title = 'function call (...)'                   # for error messaging
        def apply(self, fun, state):
            args, kwargs = self._evaluate_args(state)
            return fun(*args, **kwargs)
        
        def _evaluate_args(self, state):
            items  = [(c.name if c.type == 'kwarg' else None, c.evaluate(state)) for c in self.children]
            args   = [value       for name, value in items if name is None]
            kwargs = {name: value for name, value in items if name is not None}
            return args, kwargs
            
    class xpartial_call(xcall):
        """Partial function call inside pipeline operator, like in x:fun(a,b)."""
        def apply(self, fun, state):
            if not self.children: return fun
            args, kwargs = self._evaluate_args(state)
            return partial(fun, *args, **kwargs)
            
    class xslice_value(expression):
        def evaluate(self, state):
            assert len(self.children) <= 1
            if self.children: return self.children[0].evaluate(state)
            return None                                 # None indicates an empty index, like in 1:, in the slice(...) object
            
    class xindex(tail):
        """Element access: [...], with any type of subscript: [i], [i:j], [i:j:k], [::] etc.
        Children after reduction are either a single <xexpr> node (no slicing),
        or a list of 2-3 <xslice_value> nodes in case of a slice.
        """
        title = 'sequence index [...]'

        def compactify(self, state):
            assert 1 <= len(self.children) <= 3
            self.children = [n.compactify(state) for n in self.children]
            return self

        def apply(self, obj, state):
            # simple index: [i]
            if len(self.children) == 1:
                index = self.children[0].evaluate(state)
                return obj[index]
            
            # 2- or 3-element slice index:  i:j[:k]
            values = [n.evaluate(state) for n in self.children]
            return obj[slice(*values)]
        
    class xmember(tail):
        title = 'member access "."'
        def compactify(self, state):
            return self                                 # no compactification, it's only 1 child: a static identifier
        def apply(self, obj, state):
            assert self.children[0].type == "name_id"
            member = self.children[0].value
            return getattr(obj, member)
    
    class xqualifier(static):
        def setup(self): self.value = ''

    class xfactor(expression):
        """A chain of tail operators: () [] . with optional trailing qualifier ? or ! """
        atom      = None
        tail      = None        # list of tail operators: call / index / member
        qualifier = None        # optional qualifier: ? or !
        
        def setup(self):
            self.atom = self.children[0]
            self.tail = self.children[1:]
            if self.tail and self.tail[-1].type == 'qualifier':
                qualifier_node = self.tail.pop()
                self.qualifier = qualifier_node.text()
            
        def evaluate(self, state):
            return self.evaluate_with_qualifier(state)
        
        def _eval_inner_qualified(self, state):
            val = self.atom.evaluate(state)
            for op in self.tail:
                assert isinstance(op, NODES.tail)
                val = op.apply(val, state)
            return val
    
    class xfactor_var(xfactor): pass
    class xfactor_filt(xfactor): pass
    class xfactor_strict(xfactor): pass
    class xfilter(xfactor): pass
    
    
    ###  EXPRESSIONS - OPERATORS (BINARY / TERNARY)  ###

    class static_operator(static):
        name  = None        # textual representation of the operator, for possible rendering back into the document
        apply = None        # corresponding function from 'operator' module
        
        ops = ['+ add', '- sub', '** pow', '* mul', '// floordiv', '% mod', '<< lshift', '>> rshift', '& and_', '| or_', '^ xor',
               '< lt', '> gt', '== eq', '>= ge', '<= le', '!= ne', 'is is_', 'is not is_not']
        ops = [m.rsplit(' ', 1) for m in ops]
        ops = {op: getattr(operator, fun) for op, fun in ops}
        
        # '/' must be added separately, because it has different names (and behavior) in Python 2 vs. 3
        ops['/'] = getattr(operator, 'div', None) or operator.truediv
        
        # extra operators, implemented by ourselves
        ops['in'] = lambda x, d: x in d                         # operator.contains() is not suitable bcs it takes operands in reversed order
        ops['not in'] = lambda x, d: x not in d
        ops[''] = ops['+']                                      # missing operator mapped to '+' (implicit +)
        
        def setup(self):
            self.name = self.text()
            self.name = ' '.join(self.name.split())             # to replace multiple whitespaces in "not in", "is not"
            self.apply = self.ops[self.name]
            
    class xop_multiplic(static_operator): pass
    class xop_additive(static_operator): pass
    class xop_power(static_operator): pass
    class xop_shift(static_operator): pass
    class xop_comp(static_operator): pass
    class xop_inplace(static): pass
    class xneg(static): pass                            # negation is implemented inside <xarith_expr>
    class xnot(static): pass                            # static keyword "not" must have a node, for counting of repeated "not not not ..." expression
    
    class chain_expression(expression):
        """A chain of different binary operators, all having the same priority: x1 OP1 x2 OP2 x3 ..."""

        def evaluate(self, state):
            head, tail = self._prepare(state)
            ops = tail[0::2]                            # items 0,2,4,... are operators
            exprs = tail[1::2]                          # items 1,3,5,... are subsequent expressions, after the initial one
            assert len(exprs) == len(ops)
            
            res = head
            for op, expr in zip(ops, exprs):                # adding terms one by one to 'res'
                val = expr.evaluate(state)
                res = op.apply(res, val)                    # calulate: <res> = <res> op <val>
            
            return res
        
        def _prepare(self, state):
            """Pre-processesing of the 1st item of the chain for evaluate(). Returns the chain as (head, tail) for actual evaluation.
            Override in subclasses if the 1st item is treated differently then the others."""
            head = self.children[0].evaluate(state)
            tail = self.children[1:]
            return head, tail
    
    class xpow_expr(chain_expression):
        """chain of power operators: ** """
    class xterm(chain_expression):
        """chain of multiplicative operators: * / // %"""
    class xshift_expr(chain_expression):
        """chain of shift operators: << >>"""
    class xarith_expr(chain_expression):
        """chain of additive operators: neg + -"""
        def _prepare(self, state):
            if self.children[0].type == 'neg':
                head = self.children[1].evaluate(state)
                if head is not None:
                    head = -head
                tail = self.children[2:]
            else:
                head = self.children[0].evaluate(state)
                tail = self.children[1:]
            return head, tail
    
    class xconcat_expr(expression):
        """
        Chain of expressions separated by a space (concatenation operator): x1 x2 x3 ...
        Values of subexpressions are converted to strings and concatenated WITHOUT space.
        This is an extension of Python syntax for concatenation of literal strings, like in:
               'Python' " is "  'cool'
        and is primarily intended for easy concatenation of variables to strings in HTML attr values construction:
               p style={"font-size:" size}
        """
        def evaluate(self, state, error = "expression to be string-concatenated evaluates to None"):
            return ''.join(STR(expr.evaluate(state), expr, error) for expr in self.children)
            # items = (STR(expr.evaluate(state)) for expr in self.children)
            # return ' '.join(item for item in items if item != '')     # empty strings '' silently removed from concatenation
        
    class simple_chain_expression(expression):
        """A chain built from the same binary operator: x OP y OP z OP ..."""
        oper = None                 # the operator function to be applied
        def evaluate(self, state):
            res = self.children[0].evaluate(state)
            for expr in self.children[1:]:
                val = expr.evaluate(state)
                res = self.oper(res, val)
            return res
    
    class xand_expr(simple_chain_expression):
        "chain of bitwise-and operators: &"
        oper = operator.and_
        name = '&'
    class xxor_expr(simple_chain_expression):
        "chain of bitwise-xor operators: ^"
        oper = operator.xor
        name = '^'
    class xor_expr(simple_chain_expression):
        "chain of bitwise-or (filtering) operators: |"
        name = '|'
        @staticmethod
        def oper(x, y):
            "x | y. If 'y' is a function or method, returns y(x) (filter application), else calculates x | y in a standard way."
            #if isfunction(y): return y(x)
            return x | y                            # here, 'y' can be a Filter instance
    class xpipeline(simple_chain_expression):
        """
        Chain of "pipeline" operators, x:fun(a,b) gets executed as fun(x,a,b).
        For oper() execution, fun(a,b) is represented as a partial function returned by our custom partial() implementation.
        """
        name = ':'
        @staticmethod
        def oper(x, partial_fun):
            return partial_fun(x)
            
            
    class xcomparison(chain_expression):
        "chain of comparison operators: < > == >= <= != in is, not in, is not"
        raise_null = False
        
    class xnot_test(expression):
        """not not not ..."""
        def evaluate(self, state):
            assert len(self.children) >= 2 and all(c.type == 'not' for c in self.children[:-1])
            neg = not (len(self.children) % 2)              # check parity of 'children' to see if negation appears even or odd no. of times
            val = self.children[-1].evaluate(state)
            return not val if neg else val
    
    class xand_test(simple_chain_expression):
        "chain of logical 'and' operators. Lazy evaluation: if false item is encountered, it's returned without evaluation of subsequent items"
        name = 'and'
        def evaluate(self, state):
            res = self.children[0].evaluate(state)
            for expr in self.children[1:]:
                if not res: return res
                res = res and expr.evaluate(state)
            return res
    class xor_test(simple_chain_expression):
        "chain of logical 'or' operators. Lazy evaluation: if true item is encountered, it's returned without evaluation of subsequent items"
        name = 'or'
        def evaluate(self, state):
            res = self.children[0].evaluate(state)
            for expr in self.children[1:]:
                if res: return res
                res = res or expr.evaluate(state)
            return res
    
    class xifelse_test(expression):
        """
        ... if ... else ... Lazy evaluation of arguments: only the true branch of the condition undergoes evaluation.
        "else" branch is optional, "else None" is assumed if "else" is missing.
        """
        def evaluate(self, state):
            assert len(self.children) in (2, 3)             # the expression is compactified, that's why a single child is not possible here
            if self.children[1].evaluate(state):
                return self.children[0].evaluate(state)
            if len(self.children) == 3:
                return self.children[2].evaluate(state)
            return None                                     # default None when "else..." branch is missing
    
    # class xempty_test(expression):
    #     """
    #     Test for emptiness: X OP [TEST]
    #     If the 1st operand (X) evaluates to false, a predefined default value is returned:
    #     - '' if operator OP is ?
    #     - None if operator OP is !
    #     Otherwise, X is returned unmodified. If an optional 2nd operand (TEST) is present and evaluates to false,
    #     the default ('' or None) is returned regardless of the value of X.
    #     Additionally, if OP = ?, any exceptions raised during evaluation of X are caught and
    #     treated the same as if X was false.
    #     """
    

    ###  EXPRESSIONS - COLLECTIONS  ###

    class xlist(expression):
        def evaluate(self, state):
            return [child.evaluate(state) for child in self.children]

    class xtuple(expression):
        def evaluate(self, state):
            return tuple(child.evaluate(state) for child in self.children)

    class xexpr_tuple(xtuple):
        pass
        
    class xset(expression):
        def evaluate(self, state):
            return set(child.evaluate(state) for child in self.children)

    class xdict(expression):
        def evaluate(self, state):
            items = []
            assert len(self.children) % 2 == 0          # there's always an even no. of children after reduction of dict_pair
            for i in range(0, len(self.children), 2):
                key_child, val_child = self.children[i:i+2]
                items.append((key_child.evaluate(state), val_child.evaluate(state)))
            return dict(items)

    class xstring_format(expression):
        def evaluate(self, state):
            return self._render_all(self.children, state)       # renders embedded expressions, in addition to static text
            

    ###  EXPRESSIONS - LITERALS  ###

    class literal(expression):
        isstatic = True
        ispure   = True
        value    = None
        def setup(self):            self.value = self.text()
        def analyse(self, ctx):     pass
        def evaluate(self, state):  return self.value
    
    class xstring_raw(literal):
        def setup(self):
            self.value = self.text()[2:-1]          # remove surrounding quotes: '' or "", and the leading "r" indicating a raw string

    class xnumber(literal):
        def setup(self):
            s = self.text()
            try:
                self.value = int(s)
                return
            except: pass
            self.value = float(s)
    
    class xboolean(literal):
        def setup(self):
            self.value = (self.text() == 'True')

    class xnone(literal):
        def setup(self):
            self.value = None

    class xattr_short_lit(literal): pass


    ###  STATIC nodes  ###
    
    class xpath_import(static): pass
    class xsymbol(static):      pass
    class xname_id(static):     pass
    class xname_xml(static):    pass

    class xtext_quot(static):
        r"""In `text_quot1` and `text_quot2` productions, Python's escape characters (\n \t \x.. etc.) must be decoded."""
        def setup(self):
            self.value = decode_escapes(self.text())
        
    class xtext_quot1(xtext_quot): pass
    class xtext_quot2(xtext_quot): pass

    class xnl(static):          pass
    class xtext(static):        pass
    class xdedent(static):      pass
    class xappend(static):      pass
    class xmargin(static):      pass
    
    class xmargin_out(static):
        """
        Vertical margin composed of 1+ newlines that preceeds an outlined block.
        A trailing newline (\n) is truncated from its `value` and moved out to a subsequent sibling node
        as a leading \n to mark that that node should be rendered in "outline" rather than "inline" mode.
        Every <margin_out> IS followed by a node (block) by grammar rules. The transition of the singleton
        newline is performed in xblock.translate().
        """
        def setup(self):
            self.value = self.text()[:-1]

    class xescape(static):
        def setup(self):
            escape = self.text()
            assert len(escape) == 2 and escape[0] == escape[1]
            self.value = escape[0]                          # the duplicated char is dropped
    
    class xup_indent(static):
        """Marks occurrence of an extra 1-space indentation in a title line. Renders to empty string."""
        def render(self, state):
            return ''
    
    class indent(node):
        whitechar = None
        def translate(self, state):
            """Called when INDENT/DEDENT surround a block."""
            state.indent(self.whitechar)
            return None
        def render(self, state):
            """Called when INDENT/DEDENT surround a line within a text block."""
            state.indent(self.whitechar)
            return ''

    class dedent(node):
        whitechar = None
        def translate(self, state):
            state.dedent(self.whitechar)
            return None
        def render(self, state):
            state.dedent(self.whitechar)
            return ''

    class xindent_s(indent):
        whitechar = ' '
    class xindent_t(indent):
        whitechar = '\t'
    class xdedent_s(dedent):
        whitechar = ' '
    class xdedent_t(dedent):
        whitechar = '\t'


    # ###  SYNTHETIC nodes  ###
    #
    # class merged(static):
    #     """
    #     An artificial node created during compactification by merging several sibling nodes that are all pure (or static, in particular).
    #     Values of the original nodes (strings to be concatenated) are retrieved from their render().
    #     """
    #     value = None        # pre-rendered output of the compactified nodes
    #     ex = None           # if MissingValueEx exception was caught during rendering, it's stored here as an (exception, traceback) pair
    #
    #     def __init__(self, node, state):
    #         self.tree = node.tree
    #         self.fulltext = node.fulltext
    #         self.pos = node.pos
    #         try:
    #             self.value = node.render(state)
    #         except MissingValueEx as ex:
    #             self.ex = (ex, sys.exc_info()[2])
    #
    #     def merge(self, node, state, sep):
    #         self.pos = (self.pos[0], node.pos[1])
    #         if self.ex: return                          # we already know that an exception will be raised upon self.render(), no need to append new nodes
    #         try:
    #             nodeValue = node.render(state)
    #             self.value += sep + nodeValue
    #         except MissingValueEx as ex:
    #             self.ex = (ex, sys.exc_info()[2])
    #
    #     def render(self, state):
    #         if self.ex: reraise(None, self.ex[0], self.ex[1])
    #         return self.value
    #
    #     def info(self):
    #         from nifty.util import escape as slash_escape
    #         return "%s at position %s rendering: %s" % (self.infoName(), self.pos, slash_escape(str(self.value)))
    #
    # ###  UTILITY METHODS  ###
    #
    # @staticmethod
    # def _compactify_siblings_(nodes, state, sep = u''):
    #     "Compactify a list of sibling nodes, by compactifying each one separately when possible and then merging neighboring static nodes."
    #     out = []
    #     last = None         # the current last <merged> node; can be expanded if the subsequent node is also pure
    #
    #     for node in nodes:
    #         #print(' ', node, node.check_pure())
    #         if node.check_pure():                               # a pure node that can be reduced into a <merged> node?
    #             if last: last.merge(node, state, sep)
    #             else:
    #                 last = NODES.merged(node, state)
    #                 out.append(last)
    #         else:                                               # non-pure node? let's compactify recursively its subtree and append
    #             node.compactify(state)
    #             out.append(node)
    #             last = None
    #
    #     return out
    

#####################################################################################################################################################
#####
#####  HypertagAST
#####

class HypertagAST(BaseTree):

    NODES  = NODES              # must tell the BaseTree's rewriting routine where node classes can be found
    parser = None               # instance of Grammar to be used by super class __init__() and parse() to convert input text to AST
    _use_init = False

    ###  Configuration of rewriting process  ###
    
    # nodes that will be ignored during rewriting (pruned from the tree)
    _ignore_  = "nl ws space gap comma verbatim inline_comment " \
                "mark_struct mark_verbat mark_normal mark_markup mark_embed mark_eval mark_def mark_comment"
    
    # nodes that will be replaced with a list of their children
    _reduce_  = "modifier block_control target core_blocks tail_blocks headline body_text generic_control generic_struct " \
                "item_import rename try_long try_short special_tag head_verbat head_normal head_markup " \
                "tail_for tail_if tail_verbat tail_normal tail_markup core_verbat core_normal core_markup " \
                "attrs_def attrs_val attr_val value_of_attr args arg " \
                "embedding embedding_braces embedding_eval target " \
                "expr_root subexpr slice subscript trailer trailer_filt atom literal dict_pair " \
                "string string_quot1 string_quot2"
    
    # nodes that will be replaced with their child if there is exactly 1 child AFTER rewriting of all children;
    # they must have a corresponding x... node class, because pruning is done after rewriting, not before
    _compact_ = "factor_filt factor_strict factor_var factor pow_expr term arith_expr shift_expr and_expr xor_expr or_expr concat_expr " \
                "pipeline comparison not_test and_test or_test ifelse_test expr_tuple " \
                "block_struct"

    _reduce_anonym_ = True      # reduce all anonymous nodes, i.e., nodes generated by unnamed expressions, typically groupings (...)
    _reduce_string_ = True      # if a node to be reduced has no children but matched a non-empty part of text, it shall be replaced with a 'string' node
    

    ###  Environment  ###
    
    module   = None             # the module this script was imported from, as runtime.Module instance; can be None (script from a string)
    filename = None             # name of the file this script comes from; for error messages
    runtime  = None             # instance of Runtime that loaded this document and controls how external modules and symbols are imported
    context  = None             # dict of symbols passed to self.translate() as `context`
    
    ###  Output of parsing and analysis  ###

    text    = None              # full text of the input string fed to the parser
    ast     = None              # raw AST as generated by Pasimonious; for read access
    root    = None              # root node of the final tree after rewriting

    # symbols   = None            # dict of all top-level symbols as name->node pairs
    # hypertags = None            # dict of top-level hypertags indexed by name, for use by the client as hypertag functions
    #                             # includes imported hypertags (!), but not external ones, only the native ones

    
    def __init__(self, script, module, verbose = False):

        self.module   = module
        self.runtime  = module.runtime
        self.filename = module.filename
        self.parser   = Grammar.get_parser(script)
        
        # replace indentation with special characters INDENT/DEDENT
        flat_script = self.parser.preprocess(script, verbose = verbose)
        
        # parse input text to the 1st version of AST (self.ast) as returned by Parsimonious,
        # then rewrite it to custom NODES.* classes rooted at self.root
        try:
            super(HypertagAST, self).__init__(flat_script)
            
        except IncompleteParseError as ex:
            L = 15
            line, line_num = self._locate_error(script)
            dots = "..." if len(line) > L else ""
            raise SyntaxErrorEx('invalid syntax near line %s: %s%s' % (line_num, line[:L], dots))
        
        if self.root is None:           # workaround for Parsimonious bug in the special case of empty document (Parsimonious returns None instead of a tree root)
            self.root = NODES.xdocument(self, ObjDict(start = 0, end = 0, children = [], expr_name = 'document'))

        assert isinstance(self.root, NODES.xdocument)


    def _locate_error(self, script):
        """
        Find the first line of `script` that causes Parsimonious' IncompleteParseError. Uses binary search and script truncation.
        
        This method relies on the fact that truncating an arbitrary number of trailing lines of a script
        never introduces syntax errors unless they already have been present in the preceeding lines.
        For this to be true, all control blocks are allowed by Hypertag grammar to have empty body.
        """
        lines = script.split('\n')
        
        line_good = 0               # the last known line before the error
        line_bad  = len(lines)      # the first known line after or containing the error
        
        while line_good + 1 < line_bad:
            split   = (line_good + line_bad) // 2
            partial = '\n'.join(lines[:split])
            flat    = self.parser.preprocess(partial)
            try:
                super(HypertagAST, self).__init__(flat)
                line_good = split
                
            except IncompleteParseError:
                line_bad = split

        if not line_bad: line_bad = 1
        return lines[line_bad-1].strip(), line_bad
        
    @staticmethod
    def make_context(tags, variables):
        """
        Combine two dicts of symbols into one. If a symbol lacks a leading mark ($,%), the mark is imputed
        as $ (for `variables`), or % (for `tags`).
        """
        symbols = {}

        if tags:
            # TODO: check if names of tags are non-empty and syntactically correct
            symbols.update({name if name[0] in (MARK_TAG, MARK_VAR) else TAG(name) : value for name, value in tags.items()})
        if variables:
            symbols.update({name if name[0] in (MARK_TAG, MARK_VAR) else VAR(name) : value for name, value in variables.items()})
        
        return symbols

        
    def analyse(self, builtins = None):
        "Link occurences of variables and hypertags with their definition nodes, collect all symbols defined in the document."
        
        ctx = Context()
        self.root.predefine(builtins)
        self.root.analyse(ctx)
        
    def translate(self, __builtins__ = None, __tags__ = None, **variables):
        
        if __builtins__ is None:
            __builtins__ = self.runtime.import_builtins()
        self.context = self.make_context(__tags__, variables)
        
        self.analyse(__builtins__)
        
        dom, symbols, state = self.root.translate(State())        # calls NODES.xdocument.translate(), see there for description of returned objects
        assert isinstance(dom, DOM.Root)
        # print('top-level symbols: {symbols}')
        
        return dom, symbols, state

    def render(self):
        dom, symbols, state = self.translate()
        return dom.render()
        # output = dom.render()
        # if not output: return output
        # assert output[0] == '\n'        # extra empty line was prepended by Grammar.preprocess() and must be removed now
        # return output[1:]

    # def __getitem__(self, tag_name):
    #     """Returns a top-level hypertag node wrapped up in Hypertag, for isolated rendering. Analysis must have been performed first."""
    #     # TODO
    #     return self.hypertags[tag_name]
        

