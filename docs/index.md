<style type="text/css" rel="stylesheet">
    header h1 { text-transform: uppercase; }

    /*.tag-h1 { text-decoration: underline }*/
    /*.tag-h2 { font-weight: bold; }*/
    
    li.tag-h3 { display: none; }
    
    h1#introduction { margin: 10px 0 20px; }
    h1 { margin: 40px 0 20px; }
    h2 { margin: 35px 0 20px; }
    h3 {
     font-size:18px;
     line-height:35px;
     color: #333;
     font-weight: bold;
    }

    body {
     font:16px/23px 'Quattrocento Sans', "Helvetica Neue", Helvetica, Arial, sans-serif;
     color:#333;
    }
    pre 
    {
      font: 13px/20px 'Quattrocento Sans', "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
   
    section {
      /* width: 590px; */
      width: 850px;
      /* padding: 30px 30px 50px 30px; */
      padding: 40px 50px 50px 50px; 
      /* background: #fbfbfb; */
      background: #fcfcfc;
    }

    .wrapper {
      /* width: 650px; */
      width: 950px;
    }

    nav {
      /* margin-left: -580px; */
      margin-left: -730px;
    }

    #banner {
      /* margin-right: -382px; */
      margin-right: -532px;
    }

    #banner .fork {
      /* margin-left: -325px; */
      margin-left: -475px;
    }

    footer {
      /* margin-left: -530px; */
      margin-left: -680px;
    }

    #dummybodyid > header {
      padding-left: 0px;
      padding-right: 0px;
    }

    pre.highlight {
        max-height: 170px;
        overflow-y: auto;
    }

    pre {
      /* background: #333333; */
      /* background: #444; */
      background: #f0f3f6;                  /* #f9f7f4; */
      /* border: 1px solid #c7c7c7; */
      border: 1px solid #ddd;
    }
    code {
      font-family: monospace, serif; 
      /* background: #333; */
      /* background: #444; */
      background: #f0f3f6;
      /* color: #efefef; */
      color: #444;
      text-shadow: none;  /*0px 1px 0px #000;*/
      /* font-size: 13px; */
      line-height: 20px;
    }

    .highlight .nt {
      /* color: #f4bf75; */
      color: #f29717;
    }
    .highlight .na {
      /* color: #6a9fb5; */
      color: #3e8aaa;
    }
    .highlight .s, .highlight .sb, .highlight .sc, .highlight .sd, .highlight .s2, .highlight .sh, .highlight .sx, .highlight .s1 {
      /* color: #90a959; */
      color: #75a609;
    }
    .highlight .m, .highlight .mf, .highlight .mh, .highlight .mi, .highlight .il, .highlight .mo, .highlight .mb, .highlight .mx {
      /* color: #90a959; */
      color: #85aa34;
    }
    .highlight .k, .highlight .kn, .highlight .kp, .highlight .kr, .highlight .kv {
      /* color: #aa759f; */
      color: #9f508f;
    }
    .highlight .p, .highlight .pi {
      /* color: #d0d0d0; */
      color: #999;
    }
    .highlight .o, .highlight .ow {
      /* color: #d0d0d0; */
      color: #999;
    }
    .highlight .nn {
      /* color: #f4bf75; */
      color: #f79a19;
    }
    
    a {
      /* color: #3399cc; */
      color: #0594db;
    }
</style>

<script>
$(function() {
  $("section li, p").on("click", "a", function(event) {
    var position = $($(this).attr("href")).offset().top - 190;
    $("html, body").animate({scrollTop: position}, 400);
    event.preventDefault();
  });
});
</script>


# Introduction

Hypertag is a modern language for front-end development that allows
writing markup documents in a way similar to writing Python scripts,
where [indentation](#layout) determines relationships between nested elements 
and removes the need for explicit closing tags. Hypertag provides:

- Advanced control of rendering process with native [control blocks](#control-blocks) 
  (_if_, _for_, _while_, _try_).
- High level of modularity thanks to Python-like [imports](#imports) and explicit [context](#context) specification.
- Unprecedented support for code reuse with native [custom tags](#custom-tags).
- Native [DOM](#dom) representation and [DOM manipulation](#dom-manipulation) during rendering.
- Embedded [compound expressions](#expressions).
- All Python [operators](#operators) to manipulate arbitrary Python objects.
- Custom [pipeline](#filters) operator (`:`) for chaining multiple functions as [filters](#filters).
- Expression [qualifiers](#qualifiers) (`!?`) to create alternative paths of calculation and handle edge cases easily.
- Built-in tags for [HTML5](#html-specific-symbols) generation and for [general](#hypertag-built-ins) purposes.
- Integrated [Python built-ins](#python-built-ins).
- Integrated [Django filters](#django-filters).
- [Django connector](#django-connector).
  
See the 
[Quick Start](https://github.com/mwojnars/hypertag#quick-start) for a brief introduction.
The source code is available on [GitHub](https://github.com/mwojnars/hypertag) and [PyPI](https://pypi.org/project/hypertag-lang/).

The documentation below describes the latest *development* version of Hypertag.
Some details may differ between an official release,
see the [change log](https://github.com/mwojnars/hypertag/blob/main/CHANGELOG.md)
for differences.

Authored by [Marcin Wojnarski](http://www.linkedin.com/in/marcinwojnarski)
from [Paperity](https://paperity.org/).


## Setup

Install in Python 3:
```
pip install hypertag-lang               # watch out the name, it is "hypertag-lang"
```

Run:
```python
from hypertag import HyperHTML
html = HyperHTML().render(script)       # rendering of a Hypertag `script` to HTML
```

<!---
### Community
(TODO)

--->

## Acknowledgements

Hypertag was partially modeled on [Python's](https://www.python.org/) syntax, and 
was inspired by indentation-based templating languages:
[Slim](http://slim-lang.com/), [Plim](https://plim.readthedocs.io/en/latest/index.html),
[Shpaml](http://shpaml.com/), [Haml](https://haml.info/).

<h3 style='font-size:24px'>Dedication</h3>

_I dedicate this project to my sons, Franciszek Józef and Brunon Piotr._ &nbsp;&nbsp; -- Marcin Wojnarski

<!--<p style='text-align:right'> (Marcin Wojnarski)</p>-->

<br>
<hr>

# Language Reference


## Blocks

A Hypertag script consists of a list of **blocks**. Some of them may have tags, and/or nested
blocks inside:

    ul
        li 
            | This is the first item of a "ul" list.
            | Pipe (|) marks a plain-text block. HTML is auto-escaped: & < >
        li
            / This is the second item. 
              Slash (/) marks a <b>markup block</b> (no HTML escaping).
              Text blocks may consist of multiple lines, like here.

output:

```html
<ul>
    <li>
        This is the first item of a "ul" list.
        Pipe (|) marks a plain-text block. HTML is auto-escaped: &amp; &lt; &gt;
    </li>
    <li>
        This is the second item.
        Slash (/) marks a <b>markup block</b> (no HTML escaping).
        Text blocks may consist of multiple lines, like here.
    </li>
</ul>
```

During parsing, blocks are first **translated** into Hypertag's native 
[Document Object Model](#dom) (**DOM**),
and then the DOM undergoes **rendering** to generate a document string in a target language. 
Typically, the target language is HTML, although any other language can be supported 
if an appropriate [runtime](#runtime) is implemented to provide language-specific 
built-ins and configuration. For HTML5 generation, the `HyperHTML` standard runtime can be used,
like in this Python 3 code:

```python
from hypertag import HyperHTML

script = \
"""
    ul
        li 
            | This is the first item of a "ul" list.
        li
            | This is the second item. 
"""

html = HyperHTML().render(script)
print(html)
```
The `script` above will be rendered to:

```html
<ul>
    <li>
        This is the first item of a "ul" list.
    </li>
    <li>
        This is the second item.
    </li>
</ul>
```

See the [Runtime](#runtime) section for details about runtimes and script execution.

### Text blocks

The most elementary type of block is a _text block_. It comes in three variants:

- **plain-text** (`|`),
- **markup** (`/`),
- **verbatim** (`!`).

They differ in the way how embedded expressions and raw HTML are handled:

    | Plain-text block may contain {'em'+'bedded'} expressions & its output is HTML-escaped.
    / Markup block may contain expressions; output is not escaped, so <b>raw tags</b> can be used.
    ! In a verbatim $block$ {expressions} are left unparsed, no <escaping> is done.

output:

```html
Plain-text block may contain embedded expressions &amp; its output is HTML-escaped.
Markup block may contain expressions; output is not escaped, so <b>raw tags</b> can be used.
In a verbatim $block$ {expressions} are left unparsed, no <escaping> is done.
```

Plain-text and markup blocks may contain embedded [expressions](#expressions), like `$x` or `{a+b}`,
which are evaluated and replaced with their corresponding values during translation.
Additionally, the output of a plain-text block is converted to the target language 
(_escaped_) before insertion to the DOM. A runtime-specific _escape function_ is used
for this purpose. For example, `hypertag.HyperHTML` [runtime](#runtime) performs HTML-escaping: 
it replaces `<`, `>`, `&` characters with HTML entities (`&lt;` `&gt;` `&amp;`).
For a different target language, the escape function could perform any other operation
that is necessary to convert plain text to a valid string in this language. 

### Comments

Blocks starting with double dash (`--`) or hash (`#`) are treated as comments:
their content is left unparsed (like in a "verbatim" block) and is excluded from the output.
They must follow general rules of block alignment: have the same indentation 
as sibling blocks and deeper indentation than a parent block:

    div
      p | First paragraph
      #   Comment...
      p | Second paragraph

A block comment behaves similarly to text blocks and, like them, can span multiple lines,
if only a proper indentation of subsequent lines is kept:

    -- this is a long ... 
        multiline ...
      block comment

A comment can also be put at the end of a block headline (_inline comment_), but not together 
with inline contents of this block. Comments cannot be used inside text blocks.


## Layout

All top-level blocks in a document (or sub-blocks at any given depth)
must have the same _indentation_. Spaces (` `) and tabs (`\t`) can be used for indenting,
although we recommend only using spaces to avoid confusion:
two indentation strings are considered the same if and only if they are equal
in Python sense, which means that a space in one line cannot be replaced with a tab
in another equally-indented line. These are similar rules as in Python.

All the rules of text layout (inline text, multiline text etc.) that will be discussed later on
hold equally for _all types_ of text blocks (plain-text, markup, verbatim). 
Spaces after special characters: `|/!:$%` - are never obligatory, and in some cases
(inside expressions) may be disallowed. A single leading space right after the text-block
marker (`|/!`) is interpreted as a _marker-content_ separator 
and gets removed from the output, if present; an additional space should be inserted 
by the programmer if a space character is still desired in this place in the output.

### Modifiers

Hypertag defines _layout modifiers_: special symbols that can be put at the beginning 
of a block's headline to change the block's indentation and/or position relative 
to the previous block. There are two types of modifiers: _append_ (`...`) and _dedent_ (`<`).
Modifiers cannot be mixed, and there can be at most one modifier for a given block.

The _append_ modifier (`...`) marks that a block is a continuation of the previous block 
and should be appended to it without a newline:

    i   | word1
    ... | word2
    ... b | word3

output:

```html
<i>word1</i>word2<b>word3</b>
```

There should be no empty lines between the two blocks in the code, otherwise a newline will still 
be inserted. Indentation of the appended block is preserved and applied to any newlines that 
may occur within this block's own body:

    p
        i  | When appending blocks...
        ...|  the indentation in
             a multiline block
             is still preserved!

output:

```html
<p>
    <i>when appending blocks...</i> the indentation in
    a multiline block
    is still preserved!
</p>
```

The "append" modifier can also be used to convert an outline sub-block into an inline one:
   
    p
        ... | Using "..." modifier, a block with no predecessors
        ... |  can be inlined into its parent.

output:

```html
<p>Using "..." modifier, a block with no predecessors can be inlined into its parent.</p>
```

The _dedent_ modifier (`<`) decreases the output indentation of a block by one level 
(makes the indentation equal to the parent's). It can be used with all types of blocks, 
including tagged and control blocks:

    div
        < p
            < i | This line's output indentation is equal to the parent's and grandparent's.

output:

```html
<div>
<p>
<i>This line's output indentation is equal to the parent's and grandparent's.</i>
</p>
</div>
```    

There is also a [built-in](#hypertag-built-ins) tag called _dedent_. 
When used without parameters, or with `full=True`, this tag removes all (multi-level) output
indentation of the inner blocks, up to its own indentation:

    div
      dedent
        div
          p
            | Everything inside "dedent" is de-indented up to the level
              of "dedent" block itself.

output:

```html
<div>
  <div>
  <p>
  Everything inside "dedent" is de-indented up to the level
  of "dedent" block itself.
  </p>
  </div>
</div>
```

When used with `full=False`, the "dedent" tag only removes the top-most indentation of its 
inner blocks. Note that the "dedent" tag _can_ be combined with dedent/append modifiers. 

### The _pass_ keyword

Hypertag has a special keyword, `pass`, that can be used instead of a block, 
as an "empty block" placeholder.
This quasi-block generates no output, similarly to the `pass` keyword in Python. 
The use of `pass` is never enforced by the syntax: empty body is always a valid alternative
and can be used inside parent blocks of all types. In some cases, though, the use of 
explicit `pass` may be preferred due to aesthetic considerations.


## Structural blocks

### Anatomy of a block

Some types of blocks (_structural blocks_) may contain nested blocks inside. 
A list of such nested blocks is called a **body**. The initial part of a block that precedes 
the body is called a **header** - it always fits on a single line (the **headline**). 
For all types of structural blocks (control blocks included!), body is _not_ mandatory 
and can be omitted. Moreover, the "if" and "try" [control blocks](#control-blocks) 
may consist of multiple branches (**clauses**), each branch having its own body.

The most common type of structural block is a [tagged block](#tagged-blocks) whose header
consists of a name of tag, optionally followed by a space-separated list of attributes and a body.

Content of a structural block can be arranged as _inline_, _outline_ (short for "out of the line"),
or mixed inline+outline. Inline content starts right after the header in the headline 
and is usually rendered to a more compact form than outline content 
(without surrounding newlines):

    h1 | This is inline text, no surrounding newlines are printed in the output.
    p
       / These are sub-blocks of an outline content...
       | ...of the parent paragraph block.
  
output:

```html
<h1>This is inline text, no surrounding newlines are printed in the output.</h1>
<p>
   These are sub-blocks of an outline content...
   ...of the parent paragraph block.
</p>
```

Mixed inline+outline content is allowed if a colon `:` is additionally put in the headline:

    div: | This inline text is followed by a sub-block "p".
      p
        i | Line 1
        b | Line 2

output:

```html
<div>This inline text is followed by a sub-block "p".
  <p>
    <i>Line 1</i>
    <b>Line 2</b>
  </p></div>
```

Without a colon, all content is interpreted as multiline text (_fulltext body_):

    div |
      Line 1
      Line 2

output:

```html
<div>
Line 1
Line 2
</div>
```

If no inline content is present, a colon can optionally be put at the end of the block's headline.
The two forms, with and without a trailing colon, are equivalent:

    p
        i | text
    p:
        i | text

output:

```html
<p>
    <i>text</i>
</p>
<p>
    <i>text</i>
</p>
```

### Null tag

A special _null_ tag (`.`) can be used to better align tagged and untagged blocks in the code:

    p
      i | This line is in italics ...
      . | ... and this one is not, but both are vertically aligned in the script.
      . | The null tag helps with code alignment when a tag is missing.

output:

```html
<p>
  <i>This line is in italics ...</i>
  ... and this one is not, but both are vertically aligned in the script.
  The null tag helps with code alignment when a tag is missing.
</p>
```

<!---
In a tagged block, the text may start on the same line (_headline_) as the tag (_inline_ content)
and may extend to subsequent lines (_multiline_ content) unless sub-blocks are present.
Any content that starts below the headline is called _outline_ content (short for "out of the line").
Inline text is rendered to a more compact form than outline text
(no extra newlines between the body and the HTML tags).

    h1 | This is inline text, no surrounding newlines are printed.
    p  | This paragraph is "inline" and "multiline" at the same time,
         it continues on subsequent lines without additional "|" markers.
    div |
      Another way to write a multiline text-only block: with initial "|" marker
      in the headline followed by lines of text and no more markers.

output:

```html
<h1>This is inline text, no surrounding newlines are printed.</h1>
<p>This paragraph is "inline" and "multiline" at the same time,
it continues on subsequent lines without additional "|" markers.</p>
<div>
Another way to write a multiline text-only block: with initial "|" marker
in the headline followed by lines of text and no more markers.
</div>
```

Inline (but not multiline) text can be combined with sub-blocks if a colon (:)
is placed before the text marker. A special _null_ tag (.) can be used to better align
tagged an untagged blocks:

    div: | This inline text can be follow by nested blocks thanks to the ":" marker
      p
        i | This line is in italics ...
        . | ... and this one is not. Both are vertically aligned in the script.
        . | The null tag helps with code alignment when a tag is missing.

output:

```html
<div>This inline text can be follow by nested blocks thanks to the ":" marker
  <p>
    <i>This line is in italics ...</i>
    ... and this one is not. Both are vertically aligned in the script.
    The null tag helps with code alignment when a tag is missing.
  </p></div>
```
--->


## Tagged blocks

The most common type of structural block is a **tagged block**, whose header
consists of a name of tag, optionally followed by a space-separated list of attributes and a body:

    div class='main-content' width='1000px'
        | sub-block 1
        | sub-block 2

Tags can be _chained_ together in a single block using a colon `:`, like here:

    h1 : b : a href='#' :
        | This is a bold heading with an anchor.

output:

    <h1><b><a href="#">
        This is a bold heading with an anchor.
    </a></b></h1>

Each tag in a chain can have its own list of attributes.
Shortcuts are available for the two most common HTML attributes: 
`.CLASS` is equivalent to `class=CLASS`, and `#ID` means `id=ID`.

    p #main-content .wide-paragraph | text...
    
output:

```html
<p id="main-content" class="wide-paragraph">text...</p>
```

The same (keyword) attribute may occur multiple times on the list. In such case, 
all the values get space-concatenated. This semantics simplifies the use 
of `.CLASS` shortcuts with multiple classes, like in:

    p .wide .left .green-text

which is equivalent to a repeated use of the `class=...` attribute, and renders:

```html
<p class="wide left green-text"></p>
```


## Expressions

A Hypertag script may define _variables_ to be used subsequently in _expressions_
inside plain-text and markup blocks, or inside attribute lists.
A variable is created by an _assignment block_ ($). 
Expressions are embedded in text blocks using `{...}`  or `$...` syntax - the latter can only
be used for expressions that consist of a variable with (optionally) some tail operators (. [] ()):

    $ k = 3
    $ name = "Ala"
    | The name repeated $k times is: {name * k}
    | The third character of the name is: "$name[2]"

output:

```html
The name repeated 3 times is: AlaAlaAla
The third character of the name is: "a"
```

Expressions may contain [primitives](#primitives): literal strings, numbers, booleans, collections, `None`.
Escape strings: `{%raw%}{{{%endraw%}`, `{%raw%}}}{%endraw%}`, `$$` can be used inside 
text blocks and strings to produce `{`, `}`, `$`, respectively.

Assignment blocks support _augmented_ assignments, where multiple variables are assigned to,
all at once:

    $ a, (b, c) = [1, (2, 3)]

There are also _in-place_ assignments:

    $ x += 5
    $ y *= 2


## Operators

Each Hypertag variable points to a Python object and can be used with all the standard operators
known from Python. The list is ordered by decreasing operator priority:

    . [] ()                     - tail operators (member access, indexing, function call)
    ** * / // %                 - arithmetic 
    + - unary minus             - arithmetic
    << >>                       - bitwise
    & ^ |                       - bitwise
    A:B:C                       - slice operator inside [...] indexing
    == != >= <= < >             - comparison
    in is "not in" "is not"     - membership & identity
    not and or                  - logical
    X if TEST else Y            - logical

Inside the ternary `if-else` operator, the `else` clause is optional and defaults to `else None`.
Hypertag defines also a number of custom operators: binary, prefix unary, and postfix unary - 
they are described below.


### Non-standard binary operators

Hypertag's custom binary operators include:

- The inequality operator `<>` can be used instead of `!=`
  to avoid ambiguity with a verbatim block mark (`!`) inside `if` blocks.
  When using the standard `!=`, the test expression must typically be
  enclosed in parentheses.

- The _pipeline_ operator (`:`): allows functions and other callables be used as 
  chained _filters_. This operator is described in detail in the [Filters](#filters) section.
  
- The _concatenation_ operator: allows subexpressions to be put one after another, with only 
  a whitespace as a separator, like in `EXPR1 EXPR2 EXPR3 ...` The subexpressions are then
  converted to strings through `str(EXPR)` and concatenated.
  The programmer must ensure that `str(EXPR)` is a valid call for each subexpression.
  
The concatenation operator is an extension of the Python syntax for joining literal strings, 
like in `'Hypertag '  "is"   ' cool'` which is converted by Python parser to a single string:
`'Hypertag is cool'`. In Python, this works for literals only, while in Hypertag, 
all types of expressions can be joined in this way. 
The concatenation operator has a lower priority than binary "or" (`|`) and a pipeline (`:`);
and higher than comparisons.

Note that inside dictionaries `{...}` and array slices `[a:b:c]`, operators other than 
arithmetic and bitwise must be enclosed in parentheses to avoid ambiguity of the colon `:`,
which in Hypertag serves as a pipeline operator, but in dictionaries and slices plays a role
of a field separator.

### Non-standard prefix operators

There are two unary prefix operators that identify variables and tags inside expressions:

- The _variable embedding_ (`$`) operator can precede a variable name (`$VAR`, without space) in an expression,
  which is equivalent to a normal occurrence of the same name without a leading `$` character.
  The variable embedding operator is provided for convenience. The dollar sign as a special symbol is obligatory in some other places in a script, 
  so developers may forget where exactly it is obligatory and where it can be omitted. 
  With the variable embedding operator, the parser is more forgiving for unnecessary uses of the `$` character inside expressions.
  
- The _tag embedding_ (`%`) operator allows tags (`%TAG`, without space) to be put inside expressions, 
  which is not possible otherwise. This can be used, for example, to directly invoke tag expansion,
  like in `%div('this is body')`, passing a plain-text _body_ string and skipping the creation of an intermediate DOM
  as would be the case if a full-blown [tagged block](#tagged-blocks) were used.
  Inside expressions, tags are callable (the call invokes tag expansion) 
  and can be passed positional and keyword arguments, which are interpreted as tag attributes; 
  the first postitional argument is always interpreted as a _body_ attribute, even for a void tag.

A tag embedding constitutes an ordinary expression, and as such, it can occur as a part of a larger expression, 
be used as an attribute value, be inserted into a text block, etc. For example, the following markup block:
```
/ { %div('plain text').upper() }
```
is rendered to:
```
<DIV>PLAIN TEXT</DIV>
```

### Non-standard postfix operators

Hypertag defines two postfix operators called _qualifiers_:

- The _optional expression_ qualifier (`?`) indicates that a given subexpression can be ignored:
  if it evaluates to a false value (`''`, `None`, `False` etc.), or raises an exception, its result shall be replaced with `''`,
  and any exceptions (instances of `Exception` or its subclasses) raised during evaluation should be silently dismissed.
  Note that Python's special exceptions that inherit directly from `BaseException` rather than `Exception` are passed uncaught:
  `SystemExit`, `KeyboardInterrupt`, `GeneratorExit`.
  
- The _obligatory expression_ qualifier (`!`) indicates that a given subexpression must evaluate 
  to a true value (non-empty, not false), otherwise a `FalseValueEx` exception from `hypertag.core.errors` will be raised.

Qualifiers can be put at the end of atomic expressions (`X?`, `X!`, no space),
or right after expression embeddings (`{...}?`, `{...}!`, `$X?`, `$X!`).
Qualifiers are often combined with ["try-else"](#try-block) blocks.
Examples of use can be found in the [Qualifiers](#qualifiers) section.

  

## Filters

Hypertag defines a new operator not present in Python, the _pipeline_ (`:`), for use in expressions.
It is applied in a similar way as pipes `|` in templating languages:
to pass a result of an expression (a _feed_) to a function (a _filter_) as its first argument,
without putting the entire expression inside the function-call parentheses,
as would normally be required. A typical example of filters in a templating language:

    title | truncate(50) | upper

this takes a `title` string, truncates it to no more than 50 characters and then converts 
to upper case. In Hypertag, this expression will look the same, except the pipes are
replaced with colons:

    title : truncate(50) : upper

Templating languages, like Jinja or Django's templates, require that functions are explicitly
declared as filters before they can be used in template code.
In Hypertag, there are no such restrictions. Rather, all _callables_ (functions, methods,
class constructors etc.) can be used in pipelines with no special preparation. 
A pipeline is just another syntax for a function call, so every expression of the form:

    EXPR : FUN(*args, **kwargs)

gets translated internally to:

    FUN(EXPR, *args, **kwarg)

Obviously, pipeline operators can be chained together, such that `EXPR:FUN1:FUN2` is
equivalent to `FUN2(FUN1(EXPR))`. A filter can be specified using a compound expression,
like `obj.fun` or similar constructs (an atom followed by any number of "member access" 
or "indexing" tail operators).
For example, the standard `str.upper` method can be used directly, instead of implementing 
a custom `upper()`. Below, a pipeline is put inside a text block:

    | {'Hypertag' : str.upper : list : sorted(reverse=True)}

that renders:

    ['Y', 'T', 'R', 'P', 'H', 'G', 'E', 'A']

<!---
Remember that all Python built-ins are available in Hypertag, that is why `str`, `list`,
`sorted` etc. are accessible without an explicit import.
--->

If a filter function only takes one argument (the feed), it can be used with or without
parentheses in a pipeline. These two forms are equivalent:

    EXPR : FUN
    EXPR : FUN()

### Django filters

Hypertag seamlessly integrates all of Django's [template filters](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#built-in-filter-reference).
They can be imported from `hypertag.django.filters` and either called as regular functions
or used inside pipelines. The extra filters from [django.contrib.humanize](https://docs.djangoproject.com/en/3.1/ref/contrib/humanize/)
(the "human touch" to data) are also available. Django must be installed on the system.

    from hypertag.django.filters import $slugify, $upper
    from hypertag.django.filters import $truncatechars, $floatformat
    from hypertag.django.filters import $apnumber, $ordinal

    | { 'Hypertag rocks' : slugify : upper }
    | { 'Hypertag rocks' : truncatechars(6) }
    | { '123.45' : floatformat(4) }

    # from django.contrib.humanize:
    | "5" spelled out is "{ 5:apnumber }"
    | example ordinals {1:ordinal}, {2:ordinal}, {5:ordinal}
    
output:

    HYPERTAG-ROCKS
    Hyper…
    123.4500

    "5" spelled out is "five"
    example ordinals 1st, 2nd, 5th


## Symbols

All identifiers in Hypertag - variables, tags, attributes - are case-sensitive.

Names of tags and variables must match the following regular expression:
`[a-zA-Z_][a-zA-Z0-9_]*` - every name that matches this pattern is called _regular_.

Inside names of tag attributes in a tagged block (but not hypertag definition),
a broader set of characters is allowed.
Basically, Hypertag supports the same format as defined for attributes in the XML
(see the [_Name_](https://www.w3.org/TR/REC-xml/#NT-NameStartChar) production in the XML grammar),
with the restriction that a colon `:` must _not_ occur as the first nor the last character.
For example, the following code is valid:

    div ąłę_źó:1-x = ''
    div 更車-賈滑 = ''

output:

```html
<div ąłę_źó:1-x=""></div>
<div 更車-賈滑=""></div>
```

A name that satisfies the broader XML-like rule of naming attributes, 
but not the previous one for regular identifiers, is called _irregular_.

In hypertag definition blocks, names of formal attributes must be regular. Otherwise,
it would be impossible to refer to and make use of such attributes inside hypertag's
definition body.

However, when a tag is implemented in Python as an [external tag](#external-tags),
it can accept the extended set of attribute names, including irregular ones.

### Namespaces

There are two separate _namespaces_ in Hypertag: for tags and variables.
Thanks to the separation, there is no risk of a name collission between local variables 
and predefined tags: "a", "b", "i" etc.
For instance, it is possible to define `$i` as a loop variable, while refering to `%i` 
(an HTML tag) inside the loop at the same time:

    for i in [1,2,3]:
        i | number $i

output:

```html
<i>number 1</i>
<i>number 2</i>
<i>number 3</i>
```

By convention, to avoid confusion and clearly indicate what namespace a given symbol belongs to, 
its name can be prepended in the documentation with `$` or `%`, to denote a variable (`$i`) 
or a tag (`%i`).

### Name scoping

The two global namespaces are internally arranged in a hierarchy that follows the structure 
of the document (_hierarchical name scoping_). Every tagged block, 
as well as a [hypertag definition](#custom-tags) block, creates a new branch in the namespace:
new symbols are only added to this branch and are visible to sibling blocks 
at the same depth and to their sub-blocks, but _not_ to other blocks in the outer scope.
For example:

    p
        $x = 1
        # "x" can be accessed inside the paragraph:
        | $x

    # "x" cannot be accessed outside the paragraph

Obviously, symbols defined at a higher level can be temporarily overwritten 
in a narrower scope down the document tree:

    $ x = 1
    p:
        $ x = 2
        | "x" inside the paragraph equals $x
    | "x" outside the paragraph equals $x

output:

    <p>
        "x" inside the paragraph equals 2
    </p>
    "x" outside the paragraph equals 1

Note that unlike tagged and definition blocks, [control blocks](#control-blocks) do _not_ 
create new branches in namespaces by themselves. Therefore, it is correct to assign a variable
inside an if/try/for/while block and still access its value in sibling blocks:

    if True:
        $x = 1
    else:
        $x = 2
    | x=$x is accessible in a sibling of a control block

output:

    x=1 is accessible in a sibling of a control block


## Primitives

Hypertag supports the following literal expressions:

- `None`, `False`, `True`
- integer/real numbers: `123`, `-987.65`, `3.14e-10`
- formatted strings (f-strings): `"text"`, `'text'`
- raw strings (r-strings): `r"text"`, `r'text'`

Literal strings can be created with the `'...'` or `"..."` syntax, both are equivalent.
This creates **formatted strings** (_f-strings_, analogue of Python's f-strings),
which may contain _embedded expressions_ of both the `$...` and `{...}` form.
If you want to create **raw strings** instead, such that `$`, `{`, `}` are treated as regular
characters, the `r'...'` and `r"..."` syntax should be used:

    | { "this is a formatted string with an embedded expression: {2+3}" }
    | {r"this is a raw string, so the expression is left unparsed: {2+3}" }

output:

    this is a formatted string with an embedded expression: 5
    this is a raw string, so the expression is left unparsed: {2+3}

Inside formatted strings (but not in raw strings), Python's _escape sequences_ 
(`\n`, `\t`, `\xNN`, `\uNNNN`, `\\` etc.) are recognized and converted to 
corresponding characters.

Hypertag syntax allows for creation of standard Python collections: 
_lists_, _tuples_, _sets_, _dictionaries_.
When creating sets and dicts, keep a space between the braces of a collection and the
surrounding embedding, otherwise the double braces may be interpreted as escape strings.

    | this is a list:   { [1,2,3] }
    | this is a tuple:  { (1,2,3) }
    | this is a set:    { {1,2,1,2} }
    | this is a dict:   { {'a': 1, 'b': 2} }

Output:

    this is a list:   [1, 2, 3]
    this is a tuple:  (1, 2, 3)
    this is a set:    {1, 2}
    this is a dict:   {'a': 1, 'b': 2}


## Imports

Variables can be imported from other Hypertag scripts and Python modules
using an _import_ block. Objects of any type can be imported in this way, 
including functions and classes. Symbols can optionally be renamed using the `as` syntax:

    from python_module import $x, $y as z, $fun as my_function, $T as MyClass
    from hypertag_script import $name

    | fun(x) is equal $my_function(x)
    $ obj = MyClass(z)

The HyperHTML standard runtime recognizes the same _package.module_ syntax of import paths
as Python. The "dotted" path syntax can be applied to Python and Hypertag files alike:
the latter must have the ".hy" extension in order to be detected.
The interpretation of import paths is runtime-specific, so some other (custom)
runtime classes could parse these paths differently, for instance, to enable the import 
of scripts from a DB instead of files, or from remote locations etc.
Wildcard import is supported: `from PATH import *`.

Importing an entire module (`import PATH`) is currently _not_ supported.

Tags can be imported in a similar way as variables.
Due to separation of [namespaces](#namespaces) (variables vs. tags), all symbols must be 
prepended with either `$` (to denote a variable), or `%` (a tag):

    from my.utils import $variable
    from my.utils import %tag

When importing [external tags](#external-tags) from a Python module,
the tag name is looked up in a special module-level dictionary `__tags__`,
which must be present and contain a given tag name for the import to succeed.
The value of each entry should be an instance of `hypertag.Tag`.

HyperHTML supports relative (`.PACKAGE.MODULE`) and absolute (`PACKAGE.MODULE`) import paths.
In some cases, when relative paths are used, it may be necessary to pass the value of `__file__` or `__package__` 
of the current module as a context variable to the `render()` method, for the path resolution to work correctly:

```python
html = HyperHTML().render(script, __file__ = __file__, __package__ = __package__)
```

It is allowed that import paths refer to folders that are _not_ valid Python packages (no `__init__.py` inside).


### Context

Hypertag provides a special type of import block for declaring "context" variables and tags, 
which can (and should) be passed by the caller to `runtime.translate()` or `runtime.render()` (see [Runtime](#runtime)) 
when executing the script. These variables/tags constitute a **dynamic context** of script execution, for example:

    context $width          # width [px] of the page
    context $height         # height [px] of the page
    
    | Page dimensions imported from context are $width x $height

This script can be rendered in the following way:

```python
html = HyperHTML().render(script, width = 500, height = 1000)
print(html)
```
and the output is:

    Page dimensions imported from context are 500 x 1000

The _context block_ behaves similar to an import block, in that the declared 
variables/tags get automatically introduced to the script's namespace at the point of the block's occurrence.
Also, like in import blocks, a context block may declare multiple symbols at once, comma-separated,
and each symbol on the list can optionally be renamed using the `as` syntax:

    context $width as W, $height as H

Importantly, unlike import blocks, a context block can only occur at the beginning of a script, i.e., 
it can only be preceeded by comments or other context blocks (there can be multiple context blocks in a script).

Context blocks constitute a _public interface_ of the script: all the variables and tags declared in these blocks
are obligatory and must be present in the call to `translate()` or `render()`, otherwise an exception is raised.
Any extra variables/tags passed by the caller are ignored.

Note that the presence of context blocks in a script implies that this script can _no longer_ be imported 
by other scripts, and it can only be used at the top level of a script execution hierarchy (!),
otherwise there would be no way to supply a context.

<!---
HyperHTML supports also a special import path "~" (tilde), which denotes 
the **dynamic context** of script execution: a dictionary of all variables that have
been passed to the rendering method (`HyperHTML.render()`) as extra keyword arguments.
These variables can only be accessed in the script after they
have been _explicitly_ imported with `from ~ import ...`:

    from ~ import $width, $height
    
    | Page dimensions imported from the context: $width x $height

This script can be rendered in the following way:

```python
html = HyperHTML().render(script, width = 500, height = 1000)
print(html)
```
and the output is:

    Page dimensions imported from the context: 500 x 1000
--->


## Custom tags

Hypertag allows programmers to define _custom tags_, either directly in Hypertag code
(_native tags_), or as Python classes (_external tags_). Both cases are described below.

### Native tags

One of the most distinctive features of Hypertag is the support for custom tag definitions
right inside a Hypertag script. This type of custom tag is called a **native tag** 
or **hypertag**, and is created with a _hypertag definition block_ (`%`):
<!---
One of the key features of Hypertag is the support for custom tags (_hypertags_)
that can be defined directly in a Hypertag script using _hypertag definition_ blocks (%):
--->

    % tableRow name price='UNKNOWN'
        tr        
            td | $name
            td | $price

Here, `tableRow` is a newly defined tag that wraps up plain-text contents of table cells
with appropriate `tr` & `td` tags to produce a listing of products.
A hypertag may accept attributes, possibly with default values, similar to Python functions.
In places of occurrence, hypertags accept positional (unnamed) and/or keyword (named) attributes:

    table
        tableRow 'Porsche'  '200,000'
        tableRow 'Jaguar'   '150,000'
        tableRow 'Maserati' '300,000'
        tableRow name='Cybertruck'

<!---What a clean piece of code it is compared to the always-cluttered HTML? 
In raw HTML, and in many templating languages too, one would need much more typing
to produce the same table:
--->
output:

```html
<table>
    <tr>
        <td>Porsche</td>
        <td>200,000</td>
    </tr>
    <tr>
        <td>Jaguar</td>
        <td>150,000</td>
    </tr>
    <tr>
        <td>Maserati</td>
        <td>300,000</td>
    </tr>
    <tr>
        <td>Cybertruck</td>
        <td>UNKNOWN</td>
    </tr>
</table>
```

<!---No doubt which version is more readable and maintainable?--->

Custom native tags constitute a powerful instrument of code abstraction and deduplication.
They enhance modularity and maintainability of presentation code,
and let programmers fully adhere to the [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principle.

Imagine that, in the example above, we wanted to add a CSS class to all cells of the price column.
In HTML, we would have to walk through all the cells and manually modify 
every single occurrence (HTML is notorious for [code duplication](https://en.wikipedia.org/wiki/Duplicate_code)),
taking care not to modify `<td>` cells of another column accidentally.
With hypertags, it is enough to add `.style-price` in a tag definition, and voilà:
<!---
Hypertag, in contrast, provides powerful ways to deduplicate and modularize code, 
so it is enough to add `.style-price` in the hypertag definition, in one place, and voilà:
--->

    % tableRow name price='UNKNOWN'
        tr        
            td | $name
            td .style-price | $price

This definition can be moved out to a separate "utility" script and loaded with Python-like 
[imports](#imports), or stay in the same file where it is being used, for easy maintenance - 
the programmer can choose whatever location is best in a given case.
In traditional templating languages, there are not so many choices:
often the best we can do is separate out duplicated HTML code into a Python function
(like a [custom tag](https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/#writing-custom-template-tags)
in Django), introducing code fragmentation along the way and spreading presentation code over 
different types of files (views vs. models) and languages (HTML vs. Python) - 
a very unclean and confusing approach.

Not surprisingly, hypertags can refer to other hypertags. Moreover, hypertag definitions
can be nested: a hypertag can be defined inside another one,
such that it can only be used locally within the scope of the outer definition,
like the `%row` inside `%products`, below:

    % products items=[] maxlen=20
        % row name price
            tr        
                td | $name[:maxlen]
                td | $price
        table        
            for item in items:
                row item.name item.price

Notice that the local tag `%row`, which is being used in a loop in the last line, 
can internally access attributes of the outer hypertag (here, `maxlen`).

### "Body" attribute

A crucial element of the hypertag syntax is the **body attribute**.
Imagine that in the example above, we wanted to add another column containing
formatted (rich-text) information about a car model: pictures, funny quotes etc.
Passing this as a regular attribute is inconvenient, as we would have to somehow encode
the entire HTML structure of the description: paragraphs, styles, images.
Instead, we can add a _body attribute_ (@) to the hypertag definition:

    % tableRow @info name price='UNKNOWN'
        tr
            td | $name
            td | $price
            td
               @ info           # inline form can be used as well:  td @ info

This special attribute will hold the _actual body_ of a hypertag's occurrence, 
represented as a hierarchy of nodes of Hypertag's native [Document Object Model](#dom) (DOM),
so that all rich contents and formatting are preserved:

    table
        tableRow 'Porsche' '200,000'
            img src="porsche.jpg"
            / If you insist on <s>air conditioning</s>, 🤔
            / you can always hit the track and roll down the window at <u>160 mph</u>. 😎 
        tableRow 'Jaguar' '150,000'
            img src="jaguar.jpg"
            b | Money may not buy happiness, but I'd rather cry in a Jaguar than on a bus.
        tableRow 'Cybertruck'
            | If you liked Minecraft you will like this one, too.
            / (Honestly, I did it for the memes. <i>Elon Musk</i>)

Output:
```html
<table>
    <tr>
        <td>Porsche</td>
        <td>200,000</td>
        <td>
           <img src="porsche.jpg" />
           If you insist on <s>air conditioning</s>, 🤔
           you can always hit the track and roll down the window at <u>160 mph</u>. 😎
        </td>
    </tr>
    <tr>
        <td>Jaguar</td>
        <td>150,000</td>
        <td>
           <img src="jaguar.jpg" />
           <b>Money may not buy happiness, but I'd rather cry in a Jaguar than on a bus.</b>
        </td>
    </tr>
    <tr>
        <td>Cybertruck</td>
        <td>UNKNOWN</td>
        <td>
           If you liked Minecraft you will like this one, too.
           (Honestly, I did it for the memes. <i>Elon Musk</i>)
        </td>
    </tr>
</table>
```

There can be at most one body attribute in a hypertag; it must be the first one
on the list; it can be missing (then the tag is _void_ and its 
occurrences must have empty body); and it can have arbitrary name: we suggest _@body_ 
if there is no other meaningful alternative. 

Together with the body attribute, Hypertag provides a new type of block:
the _DOM insertion block_ (`@`) that allows embedding of a DOM represented by a body
attribute into a formal body of a hypertag. This type of block was used above when 
defining `%tableRow`:

    td
       @ info

This code inserts external information about a car (`info`) represented by a DOM
into the `<td>` tag within the hypertag's output.
Note that, similar to [text blocks](#text-blocks), DOM insertion blocks can also be used 
as [inline](#anatomy-of-a-block) body of a structural block, so the fragment above can be 
rewritten as:

    td @ info

The inline and outline forms may differ with respect to output indentation and whitespace;
otherwise they are, in most cases, equivalent 
(although this may depend on a specific tag implementation).

Most often, a DOM insertion block contains just a name of the body attribute.
However, in general, any expression is allowed, so the DOM can be 
[preprocessed](#dom-manipulation) before insertion:

    @ info.select('img')[:1]

The above code searches for `img` nodes and inserts the first one, if present.
Note that within insertion blocks, everything is treated as an expression,
so the casual embedding characters, `$...` and `{...}`, are not needed here.

<!---
Yes, associations with Python's `self` - the special argument to non-static methods -
are intended and well justified.

As you can see, Hypertag is much more concise than raw HTML, and with the help of custom
tags it enables cleaner separation between presentation logic (tags) and textual contents.
--->

Although each body attribute is a regular variable, which can be used in all the same places
as other variables (in all types of expressions), embedding it through another 
type of block (other than `@`) will _not_ work as expected. 
For example, although the following code _is_ valid:

    / $info

it will produce a Python representation string of the DOM instance,
instead of merging the DOM into the hypertag's body:

    <hypertag.core.dom.DOM object at 0x7f5de33bcd60>

In some rare cases, you might want to render the DOM straight away and embed it as a string:

    / $info.render()

This is a valid approach, although it prevents any further [manipulation](#dom-manipulation) 
of this part of the DOM upstream in the script, and for this reason it is not recommended.


### External tags

Custom tags can have a form of Python objects of `hypertag.Tag` class or its subclass.
Every new `tag` should have a name (`tag.name`) and expose the `expand` method:

    def expand(self, body, attrs, kwattrs):
        ...

This method is called during DOM rendering in order to convert a `body`
(an instance of `DOM`, see [DOM structure](#dom-structure)) tagged by the `tag` to a string 
in a target language.
Typically, `body.render()` is called inside `expand()` to first convert the body to a string,
and only then a tag-specific surrounding text is added; this can be customized, however.
In general, the tag class is free to do whatever it wants with the input DOM,
including any transformation and manipulation, before an output text is produced.
The tag expansion can be influenced by positional (`attrs`) and keyword attributes (`kwattrs`).
Note that names of keyword attributes may follow the more general [XML rules](#symbols) 
of attribute naming, so they may _not_ be valid Python identifiers.

If you implement a tag that behaves similarly to HTML markup tags, in that it only adds
surrounding plain-text tags `<...>`, possibly with attributes, it may be helpful to
use the standard `hypertag.Markup` class, which can be subclassed or directly instantiated.
This approach can be taken, for example, to implement custom XML tags, not present 
on the list of [standard HTML5 tags](#html-specific-symbols).

Hypertag provides also a convenient wrapper, `hypertag.TagFunction`, for converting
functions into tags. The wrapper can be applied to any function of the form:

    def fun(body, *attrs, **kwattrs)
        ...

The function is called in place of an `expand()` method; it should accept at least one positional 
argument (the `body`) and return a string.
Importantly, the `body` here is passed as an already-rendered string (!), rather than a DOM,
so that existing text-processing functions can be used as they are with the wrapper.
If you need to manipulate the DOM during expansion, you should subclass `hypertag.Tag` instead.

After a new tag is implemented, it should be added to the special module-level dictionary,
`__tags__`, where it could be found by [import](#imports) blocks.


## Control blocks

Control blocks of multiple types are available in Hypertag to help you manipulate input data
directly in a document without going back and forth between Python and presentation code.
The blocks are:

- **if-elif-else**
- **try-else**
- **for-in-else**
- **while-else**

### "if", "for", "while" blocks

The syntax of "if", "for", "while" blocks is analogous to what it is in Python.
Both inline and outline body is supported, although the former comes with restrictions:
the leading expression (a condition in "if/while", a collection in "for") may need to be
enclosed in `(...)` or `{...}` to avoid ambiguity of special symbols `|/!`,
which can be interpreted both as operators inside the expressions and markers of inline body.
Trailing colons in clause headlines are optional.

An example "if" block with an outline body looks like this:

    $size = 5
    if size > 10      
        | large size
    elif size > 3:
        | medium size
    else
        | small size

output:

    medium size

The same code as above, but with inline body (notice the parentheses around expressions):

    $size = 5
    if (size > 10)    | large size
    elif (size > 3)   | medium size
    else              | small size

Trailing colons (`:`) after clause headers are optional.

Examples of loops:

    for i in [1,2,3]  | $i

    for i in [1,2,3]:
        li | item no. $i

    $s = 'abc'
    while len(s) > 0               -- Python built-ins ("len") can be used
        | letter "$s[0]"
        $s = s[1:]                 -- assignments can occur inside loops

output:

```html
123

<li>item no. 1</li>
<li>item no. 2</li>
<li>item no. 3</li>

letter "a"
letter "b"
letter "c"
```

Like in Python, loops can be followed by an optional `else` clause,
however, the semantics is very _different_ to what it is in Python.
Hypertag's `else` was inspired by Django's `empty` clause of the `for ... empty ... endfor` construct
and its role is to provide a fallback when _no iteration_ of the loop was executed, either due to emptiness
of a collection (inside `for` blocks), or due to falseness of a condition right from the beginning of a `while` loop.

This is quite opposite to the Python's semantics of `else`, which is based on the loop's termination cause:
the statement executes only after the loop completes normally (no `break` was encountered).
The Python's semantics seems confusing to many and is rarely used, therefore Hypertag adopts a different, 
more intuitive and probably more useful approach. Example:

```
    for item in []:
        p | $item
    else:
        | No item found.
```

output:
```
No item found.
```

Note that Hypertag does _not_ provide equivalents for Python's loop control keywords: `break` and `continue`.



### "try" block

The "try" block differs from the same-named Python statement.
It consists of a single "try" clause plus any number (possibly none) of "else" clauses.
The first clause that does _not_ raise an exception is returned.
All exceptions that inherit from Python's Exception are caught.
Empty string is rendered if all clauses fail.

Exceptions are checked only after semantic analysis, so if there are any syntactical 
or name resolution errors (e.g., an undefined variable in a clause), they are still being raised.
Also, note that the semantics of "else" is _opposite_ to what it is in Python, where the "else"
clause of a "try-else" statement only gets executed if _no_ exception has occured.

Example:

    $cars = {'ford': 60000, 'audi': 80000}
    try
        | Price of Opel is $cars['opel'].
    else
        | Price of Opel is unknown.

output:

    Price of Opel is unknown.

Similar code as above, but with inline body:

    $cars = {'ford': 60000, 'audi': 80000}
    
    try  | Price of Opel is $cars['opel'].
    else | Price of Opel is not available, but how about Seat: $cars['seat'].
    else | Neither Opel nor Seat is available.
           Let's stick with a Ford: $cars['ford'].

output:

    Neither Opel nor Seat is available.
    Let's stick with a Ford: 60000.

There is a shortcut version "?" of the "try" syntax which can only be used without "else" 
clauses, in order to suppress exceptions:

    ? | Price of Opel is $cars['opel'].

Importantly, the shortcut "?" _can_ be used as a prefix (on the same line) 
with a tagged block, which is not possible with the basic syntax. 
The code below renders empty string instead of raising an exception:

    ? b : a href=$cars.url | the "a" tag fails because "cars" has no "url"

### Qualifiers

The "try" block is particularly useful when combined with [expression qualifiers](#non-standard-postfix-operators):
"optional" (`?`) and "obligatory" (`!`), placed at the end of (sub)expressions to mark 
that a given piece of calculation either:

- can be ignored (replaced with `''`) if it fails with an exception (`?`); or
- must be non-empty (not false), otherwise an exception will be raised (`!`).

Together, these language constructs enable fine-grained control over data post-processing,
sanitization and display.
They can be used to verify the availability of particular elements of input data
(keys in dictionaries, attributes of objects) and to easily create alternative paths 
of calculation that will handle multiple edge cases at once:

    | Price of Opel is {cars['opel']? or cars['audi'] * 0.8}

In the above code, the price of Opel is not present in the dictionary, but thanks 
to the "optional" qualifier `?`, a KeyError is caught early, and a fallback is used 
to approximate the price from another entry. The output is:

    Price of Opel is 64000.0

With the "obligatory" qualifier `!` one can verify that a variable has a non-default 
(non-empty) value, and adapt the displayed message accordingly, with no need for 
more verbose if-else tests:

    %display name='' price=0
        try  | Product "$name!" costs {price}!.
        else | Product "$name!" is available, but the price is unknown yet.
        else | There is a product priced at {price!}.
        else | Sorry, we're closed.

    display 'Pen' 100
    display 'Pencil'
    display price=25

output:

    Product "Pen" costs 100.
    Product "Pencil" is available, but the price is unknown yet.
    There is a product priced at 25.

Qualifiers can also be used in loops to test for non-emptiness of the collections 
to be iterated over:

    try
        for p in products!
            | $p.name costs $p.price
    else
        | No products currently available.

When passed `$products=[]`, the above code outputs:

    No products currently available.

Qualifiers can be placed after all atomic expressions and embeddings, no space is allowed.
More details can be found in the [Operators](#non-standard-postfix-operators) section.


## DOM

The execution of a Hypertag script consists of [multiple phases](#runtime). 
Before the final document is generated, the script is first _translated_ to a native 
Document Object Model (DOM), where every tagged block is mapped to a node in the DOM tree.
During translation:

- all expressions get _evaluated_ (converted to atomic result values); 
- all control blocks get _executed_ (replaced with the DOM of appropriate inner blocks);
  and
- all [native tags](#native-tags) get _expanded_ 
(the actual body from the place of hypertag's occurrence is replaced with this hypertag's 
definition body). 

Importantly, the translation is performed _incrementally_, going from the bottom to the top
of the script's syntax tree (AST). Whenever a hypertag declares a 
[_body attribute_](#body-attribute) (`@`), this attribute's value
(an actual body from the place of occurrence) is passed to the tag
as an _already-translated_ DOM of a particular subtree. This gives hypertags an exceptional
ability to _manipulate_ (actively introspect, truncate, rearrange) the provided subtree 
before it gets merged into the formal body of the hypertag. 
Possible applications include:

- automated generation of a [Table of Contents](#example-toc-generation) of a document;
- automated generation of a list of resources (CSS files, JS files etc.) that are required
  by different HTML components used inside a document, with deduplication of the list 
  and its placement in a predefined location (the `<meta>` section) of the final output;
- automated calculation of (approximate) sizes of particular blocks of contents
  (e.g., length of text), to adapt CSS styles of top-level HTML elements and provide better
  user experience without client-side Javascript;
- many more...

All these can be done directly in Hypertag without falling back to Python code.

The details of the [DOM structure](#dom-structure) and [manipulation](#dom-manipulation)
are discussed in next subsections. We also show how to generate a 
[Table of Contents](#example-toc-generation) in just a few lines of Hypertag code. 


### DOM structure

The DOM is built of instances of the following classes:

- **DOM**: a list of top-level `nodes` constituting a body of another (parent) 
  node, or resulting from DOM manipulation, like `DOM.select()`;
  the list can be empty; all node classes (below) are defined as inner classes of `DOM`;
- **DOM.Node**: a regular (tagged) node, and a base class for other types of nodes;
  contains a `body` represented as a `DOM` instance, a `tag` that refers to an instance of `Tag`,
  positional and keyword attributes for the tag (`attrs`, `kwattrs`), 
  and configuration of output layout (`indent`, `outline`);
- **DOM.Text**: a text node; has `text` string instead of a structural `body`, and no tag;
- **DOM.Root**: a regular node that serves as a root of the entire document tree.

The `DOM` class can be imported from Hypertag's root package:

    from hypertag import DOM

During expansion of custom tags, both [native](#native-tags) and [external](#external-tags) ones, 
the [body attribute](#body-attribute) is passed as an instance of `DOM`.
For the entire document, the result of script translation is additionally wrapped up
in `Root` and returned as an instance of this class.

If you want to check what DOM is being produced by a given script, you may call
`runtime.translate()` instead of `runtime.render()`, and then `tree()` of the returned DOM
to get its textual representation:

    dom = runtime.translate(script)
    print(dom.tree())

For example, the following script:

    ul .short-list
        li : i | Item
    
    for i in [1,2,3]:
        b class="row$i" | Row no. $i
    
is translated to the DOM:

    <Root>
      <Text>
      ul class=short-list
        li
          i
            <Text>
      <Text>
      b class=row1
        <Text>
      b class=row2
        <Text>
      b class=row3
        <Text>
      <Text>

As you can notice, all text blocks get converted to `Text` nodes.
Vertical whitespace surrounding or separating the blocks is also encoded as `Text`.
Control blocks (`for`) are replaced with the result of their execution.
Expressions are evaluated and replaced with their values (`row1` etc.).
Tags and their attributes are preserved. All positional attributes of hypertags
(but not of external tags) are converted to keyword attributes.
Chained tags (`li : i`) are mapped onto separate parent-child nodes in the DOM.

In places where `Node` instances occur, the `tree()` method prints names of tags
instead of `<Node>`, for brevity.


### DOM manipulation

There is one fundamental reason why Hypertag employs an intermediate DOM representation 
and performs the AST-to-DOM translation as a separate phase during script execution
instead of rendering the entire script to a string at once:
this reason is to allow _document manipulation_ inside hypertags, before the final document
gets rendered, so that hypertags can assume active role in document generation,
and be able to communicate more efficiently with other parts of code. 
In a typical scenario, the incoming DOM is passively transferred to the output of a hypertag.
However, with DOM manipulation routines, the DOM can be freely modified along the way,
and can also be used as a means of communication between hypertags, or as a carrier of 
internal data that control hypertags' expansion.

<!---
The incoming DOM can be used as a carrier of internal data that controls hypertag's execution, 
and not just as a passive fragment that can only be transfered blindly to the output.

The input DOM can serve not only as a passive document fragment that should be 
blindly transfered to the output; rather, the DOM can encode any type of
extra information that may influence hypertag's execution.
-->

The DOM base classes, `DOM` and `Node`, provide two general-purpose methods for traversing a DOM:

- **walk** (skip = None, order = "preorder"): 
  
  traverses the DOM hierarchy in "preorder" or "postorder" and yields all visited nodes. 
  An optional function, `skip(node)`, can be supplied to omit certain subtrees: 
  whenever skip(node) is True for a node, this node and its descendants are omitted.  
  <!--
  a generator of all nodes inside the DOM: parent nodes and descendants.
  Parents are yielded before descendants if order='preorder' (default), or after descendants 
  if order='postorder'. The stream of nodes is _not_ being wrapped up in a DOM object.
  The same method is available in the Node class: Node.walk().
  -->
  
- **alter** (transform, skip = None, order = "preorder"):
  
  traverses the DOM hierarchy in "preorder" or "postorder" and applies a given `transform(child)`
  function to all child nodes, at every nesting level.
  The `transform` produces a sequence or list of nodes to replace
  a given input node in the child list of its parent, or in a node list of a DOM container;
  an empty sequence accounts to removing a given node entirely. 
  An optional `skip(node)` function plays a similar role as in `walk()`:
  whenever skip(node) is true for a particular node, the recursive `alter`
  does _not_ walk into children and descendants of this node.
  However, the `transform` may still be applied to the node itself, to replace its own
  occurrence in a parent node.

The `DOM` class provides also higher-level methods that can be used to 
apply constraints to a DOM hierarchy and select subsets of nodes. Each of these methods returns
the nodes wrapped up in a newly created instance of `DOM`, with the original DOM left
unmodified:

- **select** (tag = None, attr = None, value = ATTR_DEFINED, order = 'preorder', **attrs):
  
  walks through the DOM in a given `order`, collects all the nodes that satisfy the
  constraints, and inserts them into a list of top-level `nodes` of a newly created `DOM`,
  which is then returned. The nodes are _not_ copied.
  The selected nodes can be related: an ancestor and its descendant can both satisfy 
  the constaints and get inserted as siblings to the `nodes` list, with the ancestor 
  still linking to its children and (directly or indirectly) to the descendant.
  For this reason, the returned DOM can take a form of a graph 
  (DAG, Directed Acyclic Graph) rather than a tree.
  
- **skip** (tag = None, attr = None, value = ATTR_DEFINED, **attrs):

  creates a mostly-deep copy of the original DOM, then truncates the subtrees
  rooted at selected nodes (the ones that satisfy the constraints).
  The new DOM is returned. All the nodes are copies of the original ones and can be 
  altered without affecting the original DOM.

Constraints for `select` and `skip` are defined through function arguments, which restrict
what nodes get selected. The conditions below can be combined:

- if `tag` argument is a string, only the nodes that are tagged, and internal names
  (`Tag.name`) of their tags are equal to this string, are selected; note that in some cases 
  the internal name may differ from the name under which a given tag is used in Hypertag code,
  for example, when a tag was renamed (`as`) during import; the internal name of the special
  [null tag](#null-tag) (`.`) is "null";
- if `tag` is present and not a string (should be a Tag instance), 
  only the nodes tagged with this tag (checked by `is` comparison) are selected;
- if `attr` is given, the selected nodes must have a keyword attribute of this name,
  and its value should be `value` (_not_ checked if `value` is `DOM.ATTR_DEFINED`);
- if `attrs` are given, the selected nodes must have at least the attributes and values
  listed in `attrs`.

Other methods may be added in the future to handle more generic classes of selector
expressions (XPath, CSS).

Additionally, the `DOM` and `Node` classes override the indexing operator `[...]` to
provide shortcuts for accessing top-level nodes and attributes, and for node selection:

- `dom[k]` is equivalent to `dom.nodes[k]`;
- `dom[a:b:c]` is equivalent to `DOM(dom.nodes[a:b:c])`, the sublist of nodes is returned as a `DOM`;
- `dom[tag]` is equivalent to `dom.select(tag)`, where `tag` can be a `Tag` or a string (tag name);
- `node[attr]` is equivalent to `node.kwattrs[attr]`;
- `node.get(attr)` is equivalent to `node.kwattrs.get(attr)`.


### Example: ToC generation

The DOM manipulation routines can be utilized to automatically generate the Table of Contents (ToC)
of an arbitrary Hypertag document. Below, we assume that `h2` is the tag that marks
occurrences of top-level headings and therefore should be detected and its contents 
put in the ToC.
A hypertag that performs this detection and generates a ToC takes as few as four lines of code:

    %toc @document
        for heading in document['h2']
            $ id = heading.get('id','')
            li : a href="#{id}" @ heading.body

Here:

- `@document` is a body attribute that contains the full DOM of an input document;
- `document['h2']` is a collection (DOM) of all `h2` headings in the document;
- `heading.get('id','')` retrieves the `id` of a heading for subsequent URL generation;
- `heading.body` retrieves the contents of a heading (the outer `h2` tag is dropped),
  for its subsequent placement inside an HTML anchor (`a`) enclosed in a list item (`li`).

With `%toc` hypertag in place, we can define one more tag, `%with_toc`, to add an introductory
text and print the full document together with the ToC:

    %with_toc @document
        | Table of Contents:
        ol
            toc @document

        | The document:
        @document

Now, to add a ToC to an arbitrary document, it is enough to tag it with `with_toc`, like here:

    with_toc
        h2 #first  | First heading
        p  | text...
        h2 #second | Second heading
        p  | text...
        h2 #third  | Third heading
        p  | text...

The output is:

```html
Table of Contents:
<ol>
    <li><a href="#first">First heading</a></li>
    <li><a href="#second">Second heading</a></li>
    <li><a href="#third">Third heading</a></li>
</ol>

The document:
<h2 id="first">First heading</h2>
<p>text...</p>
<h2 id="second">Second heading</h2>
<p>text...</p>
<h2 id="third">Third heading</h2>
<p>text...</p>
```


## Runtime

Execution of a Hypertag script is performed by a **runtime**: an instance of `hypertag.Runtime` class. 
The execution constists of 3 phases:

1. **parsing** of the script to an Abstract Syntax Tree (AST); the syntactic and semantic analysis
   of the script is performed;
2. **translation** of the AST to a native [Document Object Model](#dom) (DOM), where 
   tagged and textual blocks are mapped to nodes of a DOM tree; during translation,
   all expressions are evaluated, native hypertags get expanded, control blocks are executed;
3. **rendering** of the DOM to a final document (a string) in a target language.

Typically, client code calls runtime's `render()` to perform all the above 
steps at once. If a client wants to obtain a structured representation
of the document - the DOM - rather than a flat string, the runtime's method `translate()` 
should be called instead, followed by a call to  `render()` on the DOM tree. Between the calls,
the DOM can be manipulated and modified according to the caller's needs.

The runtime specifies what target language the scripts will be rendered to, and defines
a list of built-in symbols (tags and/or variables, see `Runtime.DEFAULT`) 
that will be automatically imported at the beginning of script execution.

Additionally, the runtime specifies an escape function (`Runtime.escape`) that will be applied
to all outputs of plain-text blocks in order to convert them to a target language.
This function can perform simple character encoding, like entity encoding in the
case of HTML, but it can also do any other more complex operation that is necessary to
convert plain text to a valid string in the target language.


### HyperHTML

Hypertag implementation provides a standard runtime, `hypertag.HyperHTML`,
for generation of HTML5 documents. This runtime implements HTML-specific tags 
and an escape function.

The escape function performs character encoding: the special characters (`<`, `>`, `&`) 
are replaced with corresponding HTML entities (`&lt;` `&gt;` `&amp;`).

The symbols imported by HyperHTML as built-ins upon startup include:

1. [Python built-ins](#python-built-ins).
1. [General-purpose](#hypertag-built-ins) tags & functions.
1. [HTML-specific](#html-specific-symbols) tags.

See the [Standard library](#standard-library) section for details.


## Standard library

Hypertag comes with a number of predefined tags and functions
that can be used in scripts. Some of them are declared as built-ins and automatically
imported by the standard runtime (HyperHTML), while others can be imported manually
using [import blocks](#imports).

Importantly, all predefined tags are implemented as _external tags_, which means they get
rewritten into the DOM nodes during translation (rather than expanded right away), 
and can subsequently be used in selectors during [DOM manipulation](#dom-manipulation)
inside other (native) tags or outside the parser code.


### Python built-ins

First and foremost, the HyperHTML's list of built-in symbols includes all of Python's
built-ins (`builtins.*`), therefore all the commonly used types and functions:
`list`, `set`, `dict`, `int`, `min`, `max`, `enumerate`, `sorted` etc.,
are available to a Hypertag script.

    | $len('cat'), $list('cat')
    | $int('123'), $min(4,5,6)
    for i, c in enumerate(sorted('cat')):
        | $i, $c  

output:

    3, ['c', 'a', 't']
    123, 4
    0, a
    1, c
    2, t

Python built-ins can also be imported explicitly from the usual path.
Remember to prepend every name with the variable marker (`$`):

    from builtins import $sorted, $list as LIST
    | $sorted(LIST((3,2,1)))

output:

    [1, 2, 3]


### Hypertag built-ins

Hypertag defines a number of its own general-purpose tags and functions (filters)
that can be used with different runtimes and target languages.
Each of the names below refer both to a tag (e.g., `%dedent`), and a same-named 
function (`$dedent`):

- **doctype** tag inserts `<!DOCTYPE html>` string;
  an optional attribute can be used to replace "html" with a custom type name;
- **dedent**: removes all line indentation in a given text or body;
- **merge**: strips leading/trailing whitespace, replaces newlines and tabs with spaces, 
  merges adjacent spaces; similar to normalize-space() in XPath;
- **inline**: converts all newline characters to HTML entities `&#10;` 
  for safe inclusion in indentation-sensitive blocks like `<pre>` or `<textarea>`;
- **unique**: removes duplicate lines, the order of remaining lines is preserved;
  if the attribute `strip=True` (default), the lines are stripped of leading & trailing whitespace 
  before comparison, and all empty lines are removed; 
- **lower**: converts a string or block of text to lower-case;
- **upper**: converts a string or block of text to upper-case;
- **crop**: truncates a string at a given length and appends an ellipsis string
  (`...` by default);
- **truncate**: alias for `crop()`.

In HyperHTML, all the above symbols are declared as built-ins and imported automatically: 

    unique
        merge |
            Hypertag
            rocks !!!
        | { upper('  hyperTAGS   rock   ') : lower : merge }
        | Hypertag rocks !!!

output:

    Hypertag rocks !!!
    hypertags rock

The following symbols are only available as functions. They are declared as built-ins in HyperHTML:

- **changes** (sequence, first = True):
  iterates over a given sequence and yields `(value,change)` pairs, where `value` is the next
  element of `seq`, and `change` is True if the value differs from the previous one, 
  False otherwise. In the first tuple, `change` equals `first` (True by default).
  This generator can be used in loops as an equivalent of Django's
  [_ifchanged_ tag](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#ifchanged).

- **cycle** (*sequences, stop = 'first'):
  a generator that cycles through each of the iterables in parallel and yields tuples
  containing consecutive elements, one per iterable - like `zip()` - but the cycling runs 
  indefinitely (if stop=False), or until the first iterable gets exhausted (stop='first', default),
  or until the longest iterable gets exhausted (stop='longest'). 
  This function is inspired by Django's [_cycle_ tag](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#cycle),
  yet it differs from this tag in that it does not require maintaining a hidden state,
  which enhances code readability.
  `cycle()` can be used, for instance, to alternate colors of columns/rows in a table:
  
      for item, color in cycle([1,2,3,4], ['blue','grey']):
          td class=$color | $item
  
  output:
  
      <td class="blue">1</td>
      <td class="grey">2</td>
      <td class="blue">3</td>
      <td class="grey">4</td>
  
If needed, all the symbols listed above can be imported explictly from the 
`hypertag.builtins` path:

    from hypertag.builtins import %unique, $unique, $cycle

<!--Note that `%unique` (tag) and `$unique` (function) are two different objects.-->


### Foreign symbols

If Django is installed, you can use all of its template filters inside Hypertag,
either as standalone functions, or filters in pipeline expressions.
The details are described in the [Filters](#django-filters) section.


### HTML-specific symbols

For every standard HTML5 tag, HyperHTML provides two corresponding Hypertag tags:
written in lower case and upper case.
For example, for the HTML tag `<div>`, there are `%div` and `%DIV` hypertags available.
Their output differs by letter case of the HTML tag name produced, otherwise the behavior
is the same. It is up to the programmer to decide what variant to use:

    div class='search'
        span | text

    DIV class='search'
        SPAN | text

output:

```html
<div class="search">
    <span>text</span>
</div>

<DIV class="search">
    <SPAN>text</SPAN>
</DIV>
```

In addition to standard HTML tags, HyperHTML provides a number of utility tags,
as described below.

The **custom "NAME"** tag outputs a non-standard HTML element of a given `NAME`,
which allows the use of [HTML Custom Elements](https://en.wikipedia.org/wiki/Web_Components)
(Web Components) inside target documents. Example:
    
    custom "my-fancy-widget" id="widget" | ...
    
output:
    
    <my-fancy-widget id="widget">...</my-fancy-widget>
       
Keyword attributes for the output element can be provided after `NAME`, as above.

The **comment** tag outputs an HTML comment. It is typically used 
with _verbatim_ body (`!`) to avoid misinterpretation of any special symbols:

    comment ! This is an HTML comment

output:

    <!--This is an HTML comment-->

Whenever HyperHTML runtime is used, all built-in HTML tags are automatically imported
to a script. They can also be imported explicitly from the `hypertag.html` module:

    from hypertag.html import %div, %DIV

An explicit import can be used, for example, when a script is being rendered with a
non-HTML runtime and the target document is mostly written in a different language,
but some HTML markup still needs to be inserted.

<!--
In addition to standard HTML tags, HyperHTML provides also a few extra tags:

Like all other predefined tags, they are implemented as external tags, 
which means they can label nodes of DOM trees and be used for DOM manipulation.

- **document** - inserts `<!DOCTYPE html>` at the beginning of a document;
  takes the DOM of an entire document and rearranges parts of the content:
  finds all nodes marked as "resource", concatenates them, performs uniquification,
  and appends to the `<head>` section of the document;
- **resource** - marks a given part of a document as a listing of resources that should be
  uniquified across the entire document and moved to the `<head>` section.
- **TOC** @document - collects all h1,h2,h3 elements of a @document and creates a list
  of anchors linking to corresponding headings (each heading should have an "id" for linking)


## Final remarks

There is a number of additional elements of Hypertag that have not been mentioned so far.

There are some _gotcha!_ you need to keep in mind when coding with Hypertag:
- So far, Hypertag hasn't been yet optimized for performance.
--->


## Django connector

Hypertag fully integrates with [Django](https://www.djangoproject.com/). 
As described earlier, all of Django's [template filters](#django-filters) are available for Hypertag scripts out of the box.
There is also a Django-Hypertag **backend** class: `hypertag.django.backend.Hypertag` - when put 
in `settings.py` of a Django project, this class allows Hypertag scripts to be found 
by the template discovery mechanism, so that Hypertag scripts can be loaded and rendered
just like standard Django's or Jinja2 templates.

The Hypertag backend configuration should be put on the `TEMPLATES` list inside Django project's `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'hypertag.django.backend.Hypertag',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {},
    },
    # ... other engines here ...
]
```

By default, Hypertag scripts are looked for in the `hypertag` subfolder of the Django project directory.
Their file names must have `.hy` extension. 
For example, to load a Hypertag script, `my_script.hy`, into a Django view function, `my_view()`, 
and render it through the Hypertag backend while setting a value of a [context variable](#context), `title`, 
you can use the following code:

```python
from django.template.loader import get_template

def my_view(request):
    template = get_template('my_script.hy')
    context = {'title': 'Hypertag sample template'}
    return template.render(context, request)
```

Note that when a Hypertag script [imports](#imports) other scripts, Hypertag's own loading mechanism is used, not Django's.
Therefore, there is no need to tweak global Django settings to import scripts from outside the `hypertag` folder:
the related scripts (imported by the top-level one) can be located in any folder or package that is accessible
through a dotted path, absolute _or_ relative. It is also possible to import scripts from subfolders of `hypertag`
by using a relative path. For example, the following import block, when placed in a top-level Hypertag script:

    from .users.profile import %photo_editor
    
will load a `photo_editor` tag from a `profile.hy` script located in `hypertag/users` subfolder.

In some cases, when relative import paths are used, it may be necessary to pass `__file__` or `__package__` of the current module 
to the `render()` method as a context variable, for the import path resolution to work correctly:

```python
# (...)
context = {'title': 'Hypertag sample template', '__file__': __file__, '__package__': __package__}
return template.render(context, request)
```





