"""
@author:  Marcin Wojnarski
"""

from __future__ import unicode_literals


grammar = r"""

###  Before the grammar is applied, indentation in the input text must be converted into
###  "indent" and "dedent" special characters: INDENT_S/DEDENT_S for spaces, INDENT_T/DEDENT_T for tabs.
###  These characters must be unique and not occur anywhere else in input text,
###  except for places where they get inserted during conversion.

###  DOCUMENT

document         =  core_blocks? margin?

tail_blocks      =  (indent_s core_blocks dedent_s) / (indent_t core_blocks dedent_t)
core_blocks      =  tail_blocks / block+

block            =  margin_out (modifier ws)? (block_control / block_def / block_context / block_import / block_struct / block_comment / special_tag)
modifier         =  dedent / append
dedent           =  '<'                         # marks the block shall be dedented by one level (to parent's indentation)
append           =  '...'                       # marks the block is a continuation and should be appended to a previous block without a newline (no top margin, inline mode)

###  CONTROL BLOCKS

block_control    =  block_assign / block_if / block_try / block_for / block_while

block_try        =  try_long / try_short
try_long         =  'try' generic_control? (nl 'else' generic_control?)*
try_short        =  '?' ws (block_struct / body_control)?       # short version of "try" block:  ?tag ... or ?|...

block_assign     =  mark_eval ws targets ws op_inplace? '=' ws (embedding / expr_augment) inline_comment?
op_inplace       =  ~"//|\%%|<<|>>|[-+*/&|^]"

block_while      =  'while' clause_if
block_for        =  'for' space targets space 'in' space tail_for
block_if         =  'if' clause_if (nl 'elif' clause_if)* (nl 'else' generic_control?)?
clause_if        =  space tail_if

targets          =  target (comma target)* (ws ',')?            # result object must be unpacked whenever at least one ',' was parsed
target           =  ('(' ws targets ws ')') / var_def           # left side of assignment: a variable, or a tuple of variables/sub-tuples
var_def          =  name_id ''                                  # definition (assignment) of a variable

tail_for         =  (expr_factor generic_control) / (expr_augment body_control?)
tail_if          =  (expr_factor generic_control) / (expr         body_control?)         # expr may contain hanging operators (/|) hence it can't be followed by generic_control which may contain /| as a text block marker

###  DEFINITION BLOCKS

block_def        =  mark_def ws name_id attrs_def generic_struct
attrs_def        =  (space attr_body)? (space attr_def)*

attr_body        =  mark_embed ws name_id
attr_def         =  name_id (ws '=' ws value_of_attr)?

block_context    =  'context' space cntx_import (comma cntx_import)* inline_comment?
block_import     =  'from' space path_import space 'import' space item_import (comma item_import)* inline_comment?
path_import      =  ~"[^\s\x22\x27]+"                           # import path can be ANY string of 1+ characters unless it contains a whitespace, ' or "
item_import      =  wild_import / name_import
wild_import      =  '*'
cntx_import      =  symbol rename?
name_import      =  symbol rename?                              # imported name must always be prepended with percent or $ to denote whether we load it from (and save into) a tag namespace or a variable namespace
rename           =  space 'as' space name_id


###  STRUCTURED BLOCK

block_struct     =  (tags_expand generic_struct) / body_text    # text block is a special case of a structural block (!), in this case block_struct gets
                                                                # reduced after parsing to the underlying block_verbat/_normal/_markup
tags_expand      =  null / (tag_expand (ws mark_struct ws tag_expand)*)
tag_expand       =  name_id attrs_val?

special_tag      =  pass ''   #/ break_tag / continue_tag

null             =  '.'
pass             =  'pass'

#break_tag       =  'break'
#continue_tag    =  'continue'


###  HEAD, BODY

generic_control  =  (ws body_text) / body_control               # like body_control, but additionally allows full-text body
generic_struct   =  (ws body_text) / body_struct                # like body_struct, but additionally allows full-text body

body_control     =  (ws mark_struct inline_comment? tail_blocks?) / (inline_comment? tail_blocks)
body_struct      =  (ws mark_struct)? ((ws headline) / inline_comment)? tail_blocks?       # this rule matches empty string '' (!)

body_text        =  block_verbat / block_normal / block_markup / block_embed
headline         =  head_verbat / head_normal / head_markup

head_verbat      =  mark_verbat gap? line_verbat?
head_normal      =  mark_normal gap? line_normal?
head_markup      =  mark_markup gap? line_markup?

###  TEXT BLOCKS, TAIL, LINE

block_embed      =  mark_embed ws expr inline_comment?          # @... embedding of a DOM fragment; not strictly a text block, but is treated as such to allow inline placement after a tag:  TAG @body ... @ body.child[0]
block_comment    =  mark_comment line_verbat? tail_verbat?
inline_comment   =  ws mark_comment verbatim?                   # inline (end-line) comment; full-line comments are parsed as block_comment

block_verbat     =  mark_verbat line_verbat? tail_verbat?
block_normal     =  mark_normal line_normal? tail_normal?
block_markup     =  mark_markup line_markup? tail_markup?

tail_verbat      =  (indent_s core_verbat dedent_s) / (indent_t core_verbat dedent_t)
tail_normal      =  (indent_s core_normal dedent_s) / (indent_t core_normal dedent_t)
tail_markup      =  (indent_s core_markup dedent_s) / (indent_t core_markup dedent_t)

core_verbat      =  (tail_verbat / (margin line_verbat))+
core_normal      =  (tail_normal / (margin line_normal))+
core_markup      =  (tail_markup / (margin line_markup))+

line_verbat      =  verbatim ''
line_normal      =  line_markup ''                              # same as line_markup during parsing, but renders differently (performs HTML-escaping)
line_markup      =  (escape / embedding / text)+                # line of plain text with {...} or $... expressions; no HTML-escaping during rendering

mark_struct      =  ':'
mark_verbat      =  '!'
mark_normal      =  '|'
mark_markup      =  '/'

mark_def         =  '%%'                                        # double percent means single percent, only we need to escape for grammar string formatting
mark_eval        =  '$'
mark_embed       =  '@'
mark_comment     =  ~"--|#"

gap              =  ~"[ \t]"                                    # 1-space leading gap before a headline, ignored during rendering


###  EMBEDDINGS

embedding        =  embedding_braces / embedding_eval
embedding_braces =  '{' ws expr_augment ws '}' qualifier?
embedding_eval   =  mark_eval !mark_eval expr_var

#embedding_or_factor = embedding / expr_factor


###  ATTRIBUTES of tags

# actual attributes as passed to a tag
attrs_val        =  (space (attr_val / attr_short))+       #/ ws '(' attr_val (',' ws attr_val)* ')'
attr_val         =  attr_named / attr_unnamed

attr_short       =  ('.' / '#') (attr_short_lit / embedding)        # shorthands: .class for class="class", #id for id="id" ... or #{var} or #$var
attr_short_lit   =  ~"[a-z0-9_-]+"i                                 # shorthand literal value MAY contain "-", unlike python identifiers!
attr_named       =  name_xml ws '=' ws value_of_attr                # name="value" OR name=value OR name=$(...)
attr_unnamed     =  value_of_attr ''
value_of_attr    =  embedding / expr_strict

###  ARGUMENTS of functions

args             =  arg (comma arg)* (ws ',')?
arg              =  kwarg / expr
kwarg            =  name_id ws '=' ws expr

###  EXPRESSIONS

# the expression...
# built bottom-up, starting with inner-most components built of high-priority operators (arithmetic)
# and proceeding outwards, to operators of lower and lower priority (logical);
# after parsing, the expression nodes with only 1 child are reduced (compactified),
# to avoid long (~10 nodes) branches in the syntax tree that don't perform any operations
# other than blindly propagating method calls down to the leaf node.

expr         =  expr_root ''                # basic (standard) form of an expression
expr_var     =  factor_var ''               # reduced form of an expression: a variable, with optional trailer; used for inline $... embedding (embedding_eval) and attributes lists
expr_factor  =  factor ''                   # reduced form of an expression: any atom, with optional trailer; used for non-embedded attribute values
expr_strict  =  factor_strict ''            # reduced form of an expression: any atom with a trailer, but no spaces inside (before the trailer)
expr_augment =  expr_tuple / expr_root      # augmented form of an expression: includes unbounded tuples (no parentheses); used in augmented assignments
expr_tuple   =  expr ws ',' (ws expr ws ',')* (ws expr)?      # unbounded tuple, without parentheses ( ); used in `expr_augment` only
expr_bitwise =  or_expr ''                  # reduced form of an expression: only arithmetic and bitwise operators; other ops must be enclosed in (...)

subexpr      =  '(' ws expr ws ')'

var_use      =  mark_eval? name_id ''                         # occurrence (use) of a variable; $ is allowed inside {...} for convenience
tuple        =  '(' ws ((expr comma)+ (expr ws)?)? ')'
list         =  '[' ws (expr comma)* (expr ws)? ']'
set          =  '{' ws expr (comma expr)* ws (',' ws)? '}'    # obligatory min. 1 element in a set
dict         =  '{' ws (dict_pair comma)* (dict_pair ws)? '}'
dict_pair    =  expr_bitwise ws ':' ws expr                   # here, `expr_bitwise` is used instead of `expr` to avoid ambiguity with pipeline operator

atom         =  literal / var_use / subexpr / tuple / list / dict / set
factor_var   =  var_use trailer* qualifier?                   # reduced form of `factor`: a variable with optional trailer, no spaces allowed
factor_strict=  atom trailer* qualifier?                      # reduced form of `factor`: no spaces allowed before the trailer
factor_filt  =  atom trailer_filt*                            # reduced form of `factor`: no function call () allowed; for use as filter function in `pipeline`
factor       =  atom (ws trailer)* qualifier?                 # operators: () [] .

pow_expr     =  factor (ws op_power ws factor)*
term         =  pow_expr (ws op_multiplic ws pow_expr)*       # operators: * / // percent
arith_expr   =  neg? ws term (ws op_additive ws term)*        # operators: neg + -
shift_expr   =  arith_expr (ws op_shift ws arith_expr)*

and_expr     =  shift_expr (ws '&' ws shift_expr)*
xor_expr     =  and_expr (ws '^' ws and_expr)*
or_expr      =  xor_expr (ws '|' ws xor_expr)*

pipeline     =  or_expr (ws ':' ws filter)*                   # "pipeline" operator, x:fun(a,b) gets executed as fun(x,a,b)
concat_expr  =  pipeline (space pipeline)*                    # string concatenation: space-delimited list of items

comparison   =  concat_expr (ws op_comp ws concat_expr)*
not_test     =  (not space)* comparison                       # spaces are obligatory around: not, and, or, if, else,
and_test     =  not_test (space 'and' space not_test)*        # even if subexpressions are enclosed in (...) - unlike in Python
or_test      =  and_test (space 'or' space and_test)*
ifelse_test  =  or_test (space 'if' space or_test (space 'else' space ifelse_test)?)?       # "else" branch is optional, defaults to None

#empty_test  =  ifelse_test op_empty (ifelse_test)?           # test for emptiness (falseness) of 1st operand: if empty, it's replaced with either '' or None, depending on operator: ? or !

expr_root    =  ifelse_test ''


###  TAIL OPERATORS:  call, slice, member access, filter application, qualifier ...

slice_value  =  ws (expr_bitwise ws)?           # empty value '' serves as a placeholder, so that we know which part of *:*:* we're at; expr_bitwise is used to avoid collission with pipeline operator
slice        =  slice_value ':' slice_value (':' slice_value)?
subscript    =  slice / (ws expr_augment ws)

call         =  '(' ws (args ws)? ')'
index        =  '[' subscript ']'               # handles atomic indices [i] and all types of [*:*:*] slices
member       =  '.' ws name_id
trailer      =  call / index / member
trailer_filt =  index / member                  # reduced form of `trailer` for use in `factor_filt` and `pipeline`

partial_call =  '(' ws (args ws)? ')'
filter       =  factor_filt partial_call?       # no space is allowed between the function and its arguments

qualifier    =  ~"[\?!]"                        # ? means that None/empty(false)/exceptions shall be converted to '' ... ! means that empty (false) value triggers exception
# obligatory   =  '!'
# optional     =  '?'


###  SIMPLE OPERATORS

op_power     =  '**'
neg          =  '-'                             # multiple negation, e.g., "---x", not allowed -- unlike in Python
op_multiplic =  '*' / '//' / '/' / '%%'         # double percent means single percent, only we need to escape for grammar string formatting
op_additive  =  '+' / '-'
op_shift     =  '<<' / '>>'
op_empty     =  '?' / '!'

not          =  'not'
op_comp      =  ~"==|!=|>=|<=|<|>|not\s+in|is\s+not|in|is"

###  IDENTIFIERS

symbol           =  (mark_def / mark_eval) name_id
name_id          =  !name_reserved ~"[a-z_][a-z0-9_]*"i
name_reserved    =  ~"(from|import|if|else|elif|try|for|while|break|continue|pass|is|in|not|and|or)\\b"     # names with special meaning inside expressions, disallowed for hypertags & variables; \\b is a regex word boundary and is written with double backslash bcs single backslash-b is converted to a backspace by Python

# names allowed in XML, defined liberally, with nearly all characters allowed to match all valid HTML/XML identifiers (esp. attributes);
# EXCEPTION: colon ':' is NOT allowed as the 1st or the last character, to avoid collision with a trailing ":" used in blocks
name_xml         =  ~"[%(XML_StartChar)s]([%(XML_Char)s]*[%(XML_EndChar)s])?"i


###  ATOMS

literal          =  number / string / boolean / none

number_signed    =  ~"[+-]?" number
number           =  ~"((\.\d+)|(\d+(\.\d*)?))([eE][+-]?\d+)?"      # the leading +- is added during expression construction (<neg>)
#string           =  ~"'[^']*'" / ~'"[^"]*"'         # '...' or "..." string; no escaping of ' and " inside!
boolean          =  'True' / 'False'
none             =  'None'

string           =  string_format / string_raw
string_raw       =  ~"r'[^']*'" / ~'r"[^"]*"'         # '...' or "..." string; must not contain ' or " inside (no escaping available)

string_format    =  string_quot1 / string_quot2
string_quot1     =  "'" (escape / embedding / text_quot1)* "'"
string_quot2     =  '"' (escape / embedding / text_quot2)* '"'


###  BASIC TOKENS

escape      =  ~'\$\$|{{|}}'                 # escape sequences: $$ {{ }}

verbatim    =  ~"[^%(INDENT_S)s%(DEDENT_S)s%(INDENT_T)s%(DEDENT_T)s\n]+"su       # 1 line of plain text, may include special symbols (left unparsed)
text        =  ~"[^%(INDENT_S)s%(DEDENT_S)s%(INDENT_T)s%(DEDENT_T)s\n${}]+"su    # 1 line of plain text, excluded $ { }
text_quot1  =  ~"[^%(INDENT_S)s%(DEDENT_S)s%(INDENT_T)s%(DEDENT_T)s\n${}']+"su   # 1 line of plain text, excluded $ { } '
text_quot2  =  ~'[^%(INDENT_S)s%(DEDENT_S)s%(INDENT_T)s%(DEDENT_T)s\n${}"]+'su   # 1 line of plain text, excluded $ { } "

indent_s    = "%(INDENT_S)s"
dedent_s    = "%(DEDENT_S)s"
indent_t    = "%(INDENT_T)s"
dedent_t    = "%(DEDENT_T)s"

margin_out  =  nl ''                         # margin that preceeds an outlined block; its trailing \n will be moved out into the block before rendering
margin      =  nl ''                         # top margin of a block; same as `nl` in grammar, but treated differently during analysis (`nl` is ignored)
nl          =  ~"\n+"                        # vertical space = 1+ newlines

comma       =  ws ',' ws
space       =  ~"[ \t]+"                     # obligatory whitespace, no newlines
ws          =  ~"[ \t]*"                     # optional whitespace, no newlines

###  SYMBOLS that mark TYPES of blocks or text spans

"""

#####################################################################################################################################################
#####
#####  DEFINITIONS for use together with the grammar
#####

MARK_TAG = '%'
MARK_VAR = '$'

def TAG(name):
    """Convert a tag name to a symbol, for insertion to (and retrieval from) a Context."""
    return MARK_TAG + name

def VAR(name):
    """Convert a variable name to a symbol, for insertion to (and retrieval from) a Context."""
    return MARK_VAR + name

def TAGS(names):
    """Mapping of a dict of tag names (and their linked objects) to a dict of symbols."""
    return {MARK_TAG + name: link for name, link in names.items()}

def VARS(names):
    """Mapping of a dict of variable names (and their linked objects) to a dict of symbols."""
    return {MARK_VAR + name: link for name, link in names.items()}

def IS_TAG(symbol):
    return symbol.startswith(MARK_TAG)

def IS_VAR(symbol):
    return symbol.startswith(MARK_VAR)

