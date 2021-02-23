## Introduction

Hypertag is a modern language for front-end development that allows
writing (X)HTML pages and documents in a way similar to writing Python scripts,
where _indentation_ encodes relationships between nested elements 
and thus removes the need for explicit closing tags.
Hypertag provides advanced control of document rendering with
native control blocks; high level of modularity with Python-like imports;
and unprecedented support for code re-use thanks to native custom tags (_hypertags_).

<!---
Hypertag enables advanced control of document rendering process through
native **control blocks** (if-elif-else, for, while, try);
and let the programmer define **custom tags** (_hypertags_), either directly
in the document using Hypertag syntax (_native tags_), 
or as Python functions (_external tags_).
and provides high level of **modularity** through custom tags and import blocks. 
--->

Why to use Hypertag:
- **concise syntax**: inspired by Python, the indentation-based syntax is a lot cleaner, 
  more readable and maintainable than raw HTML; it requires less typing, is less redundant,
  and lets you concentrate on coding rather than chasing unmatched opening-closing tags;
  <!--
  makes the problem of unmatched opening-closing tags non-existent
  forget about unmatched opening-closing tags;
  -->
- **code re-use** is the corner stone of programming: 
  without reusable functions and classes, implementing advanced software
  would be impossible; HTML has been missing this important element, 
  but this is fixed now with Hypertag, in which programmers can
  create re-usable components in a form of **custom tags** (_hypertags_), 
  defined either as Python functions (_external tags_) 
  or directly in a document using Hypertag syntax (_native tags_);
  hypertags can be parameterized and may represent complex pieces 
  of combined: content, style and layout - for re-use across multiple documents;
- **control blocks** (for, while, if-elif-else, try-else) enable fine-grained control
  over document rendering process; Hypertag's control structures constitute
  a core part of the language syntax, unlike in templating languages, 
  where control structures are artificially overlaid on top of another language (HTML);
- **modularity** in Hypertag is modeled after Python's: 
  every script may import (hyper)tags and variables from other scripts,
  as well as from Python modules and from _dynamic context_ of script rendering;
  scripts and modules can be structured into packages;
  with this mechanism, building libraries of re-usable components is easy and fun.
  
<!--- (TODO)
- **consistency**: Hypertag combines presentation and logic in one language; 
  you no longer have to mix presentation code (HTML) with foreign syntax of a 
  templating language, or PHP etc.

- Object-Oriented Programming (**OOP**) inside markup,
  through native language structures (???)
- **high performace** in web applications achieved through caching of parsed AST,
  combined with their **compactification**: constant parts of the AST are
  pre-rendered and merged into single nodes, to avoid repeated rendering
  with every web page request.
--->

If you try Hypertag, you will never miss old-school HTML templating.

## Quick Start

## Cheat Sheet

### Text blocks

| &nbsp;<br> Symbol <br><img width=400/> | &nbsp;<br> Description <br>&nbsp; |
| ------------- | --------------- | 
| &#124; _text_   | plain-text block; may contain embedded expressions; output is HTML-escaped |
| / markup        | markup block; may contain embedded expressions; output is *not* HTML-escaped |
| ! _verbatim_    | verbatim block; expressions are *not* parsed; output is *not* HTML-escaped |
| &#124; _multi-line_<br>&nbsp;&nbsp;_text....._ | text blocks may span *multiple lines*, also when preceded by a tag; subsequent lines must be indented |
| -- _comment_ <br> # _comment_ | line of comment; is excluded from output; may occur at the end of a block's headline (_inline comment_) or on a separate line (_block comment_) |
| < BLOCK       | _dedent marker_ (<) put on the 1st line of a BLOCK causes its output to be dedented by one level during rendering; applies to blocks of all types (text, control etc.) |

### Expressions

| &nbsp;<br> Symbol <br><img width=300/> | &nbsp;<br> Description <br>&nbsp; |
| :------:          | --------------- | 
| $x = a-b          | assignment block; space after $ is allowed |
| $x <br> $x.v[1]   | embedding of a factor expression (a variable with 0+ tail operators) in a text block or string |
| {x+y}             | embedding of an arbitrary expression in a text block or string |
| x! <br> {x*y}!    | "obligatory" qualifier (!) for an atomic or embedded expression; raises as exception if the expression is false |
| x? <br> {x*y}?    | "optional" qualifier (?) for an atomic or embedded expression; replaces exceptions and false values with empty strings |
| 'text'    | f-string (formatted string), may contain embedded expressions: $... and {...} |
| "text"    | f-string (formatted string), may contain embedded expressions: $... and {...} |
| r'text'   | r-string (raw string), no embedded expressions |
| r"text"   | r-string (raw string), no embedded expressions |
| $$        | escape string; renders $ in a plaintext/markup block and inside formatted strings |
| {{        | escape string; renders { in a plaintext/markup block and inside formatted strings |
| }}        | escape string; renders } in a plaintext/markup block and inside formatted strings |
| %TAG      | reference to a tag in an expression (_not implemented yet_) |

### Tags

| &nbsp;<br> Symbol <br><img width=1100/> | &nbsp;<br> Description <br>&nbsp; |
| ------------- | --------------- | 
| h1 &#124; _text_ <br> div <br>&nbsp;&nbsp;&nbsp;&nbsp; p &#124; _text_  | _tagged block_: starts with a tag name (_header_), which can be followed by contents (_body_) on the same line (_inline body_) and/or on indented lines beneath (_outline body_) |
| box: &#124; _Title_<br>&nbsp;&nbsp;&nbsp; li &#124; _item1_<br>&nbsp;&nbsp;&nbsp; li &#124; _item2_ | mixing inline and outline contents is possible if the colon (:) and a text-block marker (&#124;/!) are both present |
| h1 : b : a href='' : <br>&nbsp;&nbsp;&nbsp;&nbsp; &#124; _text_  | multiple tags can be chained together using colon (:); trailing colon is optional |
| box "top" x=1.5 <br>a href=$url <br>a href={url} | unnamed and named (keyword) attributes can be passed to a tag as a space-separated list, no parentheses; values can have a form of expressions (embedded $, {}, or atoms) |
| %TAG x y=0 ...    | hypertag definition; may have _formal attributes_ (space-separated), possibly with defaults; may be followed by a body (inline or outline); space after % is allowed |
| %TAG @body ...    | the "at" sign (@) marks a special _body attribute_, which can have an arbitrary name; must be the 1st attribute on the list; if missing, the hypertag is _void_ (doesn't accept actual body in places of occurrence) |
| @body <br> @body[2:] | _embedding block_ (@): inserts DOM nodes represented by an expression (typically a body attribute inside hypertag definition) |
| div .CLASS        | (shortcut) equiv. to *class="CLASS"* on attributes list of a tag |
| div #ID           | (shortcut) equiv. to *id="ID"* on attributes list of a tag |
| pass              | special _pass tag_ generates no output, does *not* accept attributes nor a body |
| . <br> . &#124; _text_ | special _null tag_ (.) outputs its body without changes; helps improve vertical alignment of text in adjecent blocks; does *not* accept attributes |
<!---
| TAG x=1.0 y={v+1} | named (keyword) attributes of a tag occurrence; space-separated, no parentheses |
| TAG "yes" 3 True  | unnamed attributes of a tag occurrence; values are matched to formal attributes in a way similar to how Python matches function arguments (by order) |
--->

### Control blocks

| &nbsp;<br> Syntax <br><img width=1000/> | &nbsp;<br> Description <br>&nbsp; |
| ------------- | --------------- | 
| import $x <br> from ~ import $x as y <br> from PATH import $x, %TAG <br> | importing a variable ($NAME) or a tag (%NAME) from another module (PATH) or from the dynamic context of rendering ("~" default) |
| if COND &#124; _text_ <br> if COND:<br>&nbsp;&nbsp;&nbsp;&nbsp;BLOCKS...<br> elif: ... <br>else: ... | _if-elif-else_ construct behaves similarly as in Python; trailing colons (:) are optional |
| try-else | may have a body (inline, outline), but cannot be followed by tags on the same line |


| Symbol    | Syntax     | Description     |
| :-------: | --------------- | --------------- | 
| ?         |       | *optional block*; like a "try" without an "else" branch; can be applied to a tagged block (on the same line) |
| for       | for-in |
| while     | while EXPR |

Trailing colon (:) in a headline of a control block (for/while) or a clause (if/elif/else/try)
is _optional_ and can be omitted in most cases - with an exception for a mixed
text+structural body (text title in a headline + structural sub-blocks beneath),
which requires that a text marker in a headline is preceeded by a colon.

    box: | This box has a title and a list of sub-blocks at the same time
        li : b | item 1
        li : b | item 2

## Terminology

**Headline**. The first line of a tagged or control block. 
Contains a tag, or multiple tags, or a keyword.

**Header**. The initial part of a headline, up to the last marker (see below).

**Marker**. A special symbol (one of &#124;/!@:) that marks the beginning of a body 
of a tagged or control block. Typically, there is exactly one marker in a headline.
There can be none, though (when a body starts in a new line); or more than one
().

If the entire body of a block fits in the headline, it is called an **inline body**.
If the body starts on a new line after the headline, it is called an **outline body**.
 - is called a **header**.

**headline** = **header** + **marker** of body type + **title** (inline body)

**inline body** - consists of a title only
**multiline body** - 
**outline body** - consists of sub-blocks, no title

Trailing colon (:) after a header indicates that subsequent lines will contain blocks
rather than multi-line text - even if there is a text-block marker .

- block
- body
- tag, attributes
- script >  AST > DOM ... tree, node, body
- rendering

((?? move Script Execution here))


## Syntax

### Basic blocks

#### Text blocks

Plain-text, markup, verbatim:

    | plain-text (normal) block with {'em'+'bedded'} $expressions
    / markup <b>block</b> with no HTML escaping
    ! verbatim $block$, expressions left unparsed

Multiline block:

    |   text block
      may span
        multiple
      lines...

##### Embedded expressions

Text blocks (normal and markup) may contain embedded expressions.
An embedding may come in two forms, either using the {...} syntax:

    | value of x = {x}

or using the $... syntax:

    | value of x = $x

The former syntax can handle all types of expressions, while the latter 
can only be used for variables, possibly extended with tail operators:

    | $x.value
    | $x[index]
    | $x(arg1, arg2)

Both forms, {...} and $..., allow the use of a trailing qualifier (? or !)
to test for errors or false results:

    | {x+y}?  -- is converted to empty string if false, or if exception was raised
    | $x.call()!  -- raises an exception if x.call() is false


#### Assignments

A block that starts with $ marks an assignment to a local variable:

    $ x = 5
    $ dash = x * '-'
    $ title = dash + ' TITLE ' + dash

Hypertag supports also _augmented assignments_ as known in Python:

    $ a, (b, c) = [1, (2, 3)]


#### DOM embedding

    @ body
    @ body[0]
    @ body.METHOD()


#### Tagged blocks

- tags chain (:) -- multiple tags can be put one after another on the same line; 
  each tag can have its own attributes; special tags (_pass_, _null_ tag) cannot be used 
  in this way
- body layout: inline / outline / headline
- there is still a way to explicitly write raw (X)HTML tags
  through the use of /-blocks which allow writing unescaped markup


#### Hypertag definition

A Hypertag script may contain definitions of custom tags, called **hypertags**,
which can be viewed as equivalents of Python functions
and be used in all the same places as built-in tags.
Like functions in traditional programming languages, hypertags enable _modularization_
and _code de-duplication_: repeated parts of a script can be moved out
to a hypertag and re-used instead of being copy-pasted multiple times; also, hypertags 
can be placed in separate files, then imported and re-used across different scripts
and applications, as a library of predefined **widgets**.
This realization of the DRY principle is an important aspect of the Hypertag language,
one that has been missing in standard front-end languages (HTML, XML).

A hypertag definition block starts with "%" followed by a name of a new tag,
its attributes (optional) and formal body (optional). 
Default values in a form of literals or expressions can be provided for (selected) attributes.
If the first attribute on the list is prefixed with a special symbol "@",
this attribute will be assigned the actual body of the block of occurrence
(where the new tag is used); the "body" attribute can have any valid name, 
but it cannot have a default value. If a body attribute is missing, the hypertag
is "void", which means its occurrences must always have empty body.

An example hypertag definition may look like this:

    % fancy_text @body size='10px':
        | *****
        p style=("color: blue; font-size: " size)
            @body
        | *****

The above block defines a new tag "fancy_text", which can be used like this:

    fancy_text '20px'
        | This text is rendered through a FANCY hypertag!

During rendering of this block the definition body of `fancy_tag` gets expanded
and the actual `@body` is inserted, resulting in the following output:

    *****
    <p style="color: blue; font-size: 20px">
        This text is rendered through a FANCY hypertag!
    </p>
    *****


Hypertag definition blocks can be nested in tagged blocks and in other
definition blocks (_nested definitions_), but not in control blocks.


### Control blocks

#### Block "try"

Basic form:

    try ...
    or ...
    else ...

If used with a single tagged block, try block can be written in a shorter form:

    ?tag ...
    ? tag ...

This works with a default tag specification, as well:

    ? .some-class ...
    ? #some-id ...

#### Block "if"

#### Block "for"
    
- break & continue

#### Block "import"

1. Import from the global context:
  
        import $OBJECT
        import %TAG
or
        from ~ import $OBJECT
        from ~ import %TAG

The special import path "~" denotes the current global context of script execution.
When the `from PATH` clause is omitted the `from ~` path is assumed.
When a script is imported to another script, the context stays the same for both.

2. Import from a Python module:

from PATH import NAME -- import from a module denoted by PATH, which can be any string
  consisting of [...] characters that can be correctly interpreted by the currently used
  Environment subclass

3. Import from a Hypertag script:

...

4. Import from a combined Python-Hypertag module:

...



### Comments

Comments start with either "#" or "--". There are two types of comments:
_block comments_ (outline comments) and _inline comments_.

#### Block comments

A block comment starts with # (hash) or -- (double dash),
followed by any verbatim text that gets ignored during parsing.
It must follow general rules of block alignment: have the same indentation 
as neighboring blocks and deeper indentation than a parent block. For example:

    div
      p | First paragraph
      #   Comment...
      p | Second paragraph

A block comment behaves similar to text blocks and, like them, can span multiple lines,
if a proper indentation of subsequent lines is kept:

    # this is a long ... 
        ... multiline
      block comment


#### Inline comments

An inline comment occurs at the end of a line containing a header of any structural block
(a block that may contain nested blocks, i.e., any block except text blocks). Examples:

    p      -- comment
    p:     -- comment
    p:     #  comment
    for i in [1,2,3]:     -- comment
        pass
    if test               # comment
        | test is true

Comments can NOT be mixed with textual contents of text blocks.


### Expressions

#### Literals

Integers, real numbers, strings, boolean literals (True, False), None.

    True, False, None

#### Strings

- raw strings (_r-strings_)
- formatted strings (_f-strings_)



#### Collections

Lists, dicts ...

#### Operators

Hypertag implements majority of standard operators available in Python.

Arithmetic and binary operators:

    ** * / // %
    + - unary minus
    << >>
    & ^ |

Logical operators:

    == != >= <= < > in is "not in" "is not"
    not and or

A more general variant of the ternary "if-else" operator is available, 
with the "else" branch being optional, imputed with "else None" if missing:

    X if TEST else Y
    X if TEST

Tail operators:

    .     member access
    []    indexing
    ()    function call

Slice operator when used inside [...]:

    start : stop : step

Above these, Hypertag implements a non-standard binary **concatenation operator** (space),
as well as tail operators: **optional value** ("?") and **obligatory value** ("!").
They are described in next sections.


#### Concatenation operator

If multiple expressions are put one after another separated by 1+ whitespace:

    EXPR1 EXPR2 EXPR3 ...

their values are converted to strings and concatenated.
This is an extension of Python syntax for concatenating literal strings, like in:

       'Hypertag '  "is"   ' cool'

which is parsed by Python into a single string:

       'Hypertag is cool'

In Hypertag, concatenation using whitespace as an operator is performed on runtime,
hence all (possibly non-literal) expressions are supported as operands, not just literals;
and values of other types than `<str>` are automatically converted to strings 
before concatenation.

The programmer must guarantee that the values of all sub-expressions 
can be converted to `<str>` through the call: `str(value)`

#### Qualifiers: ? and !

? = _optional value_: fall back to an empty string if an error/None/False/0/... was returned

! = _obligatory value_: raise an exception if an empty value (None/False/0/''/...) was returned

A qualifier (? or !) can be appended at the end of an atomic expression (X?, X!)
to test against errors during evaluation, or emptiness (falseness) of the returned value.

With ? qualifier, if X evaluates to a false value or an exception was raised during evaluation,
empty string '' is returned instead. A value, X, is false, if bool(X) == False.
Empty string '', None, 0, False are examples of false values.

With ! qualifier, if X is false, MissingValue exception is raised. 
Typically, this exception is caught with a surrounding "optional value" qualifier:

    (... expr! ...)?

or with a "try" block higher in the script.

In any case (X? or X!), if X is true, the value of X is returned unchanged.

Examples:

    {(post.authors ', ')? post.title}  -- prints title only if "authors" field is missing in "post"
    
### Name spaces

Every tagged block, as well as a hypertag definition, creates a new (nested) name space,
so any assignments performed in this block do NOT influence any other part 
of the script outside the block. For example:

    $ x = 1
    p:
        $ x = 2
        | {x}
        # the line above outputs "2"
    | {x}
    # the line above outputs "1"

This does NOT apply to control blocks, which modify the top-level namespace, 
so it is fine to assign a variable inside an if/try/for/while block 
and the value will be visible in subsequent blocks:

    

Note that in Hypertag, there are _two separate name spaces_:
1. **Tags namespace**
2. **Variables namespace**

The separation of these name spaces is justified by the fact that in the most
typical use case - HTML generation - there are several dozens of predefined tags,
all of which must be directly accessible. Many of these tags have very common
names (i, b, p, code, form, head, body, ...), and without separation of name spaces,
name collissions between tags and local variables would be very frequent 
and lead to confusion.

((As a consequence of name spaces separation, it is not possible to directly refer
to tag names inside expressions. THERE WILL BE A WAY through %TAG operator))

### Special tags

#### Null tag (.)

In blocks that allow tags, you can put a dot "." instead of a tag name.
The dot represents a _null tag_ that creates a node in the DOM (like any regular tag) 
but during rendering it passes the body unchanged to the output.
In other words, a _null tag_ is a tag that performs no processing of its body,
something like an identity function.

Typically, a null tag is used in either of two cases:

1. to vertically align text contents of mixed: tagged and untagged blocks;
   using a null tag allows all blocks to have the same indentation of text contents,
   even despite some blocks need more horizontal space for their (regular) tags;
1. to visually group in the script related blocks; note that sub-indentation of the
   dotted block will be preserved in the output.

Both cases are illustrated in the example below:

    h1                        | TITLE
    .
        a href="http://..."   | click HERE!
        .                     | and see our new marvelous web page


#### Pass tag

A block consisting of a single keyword `pass` (the _"pass" tag_), no attributes, no body - 
constitutes a "pass block" that serves as a placeholder that does simply nothing, 
not even rendering a newline (unlike the null tag). The pass tag corresponds 
to Python's "pass" keyword. Typically, a pass block is used inside control blocks 
(for/if/else) to mark an empty branch, which may appeal to aesthetics or be a way to mark 
unfinished implementation. Example:

    if condition
        p | render something
    else
        pass

The above code is equivalent to:

    if condition
        p | render something

### Indentation

Normally, _script indentation_ is stored in the DOM nodes and translates to 
_output indentation_ of the text produced during rendering.
You can modify this behaviour and remove output indentation in two ways, by using:

- Dedent marker (<): removes output indentation of a single block
  the marker is used with
- Dedent tag (builtin): removes output indentation of all nested blocks
  (but the indentation of the dedent block itself stays untouched)

Often, _dedent marker_ and _dedent tag_ are used together.

Example:

    div
        < dedent : a
            p:    / These <p> blocks will be aligned with their parent (<a>) after rendering.
                b | Deeper-level nested block are dedented, too!
            p     / And the parent's indentation is removed, as well
                    (<a> is aligned with top-level <div>), thanks to 
                    the use of the <i>dedent marker</i>.
    

## DOM

DOM = Document Object Model

### DOM classes

### DOM manipulation

Selectors as methods of Sequence ...

### Selectors (??)

**Terminal tag** is a tag that does not use any tags inside its (formal) body and thus 
its expansion does NOT create any new tagged nodes, except possibly those that have been
passed to it in the @body attribute.
Terminal tags are important, because they are the only tags that may occur in a DOM tree
after translation of the AST; and consequently, they are the only tags that are visible 
to **selectors** and can be operated on during expansion of other (non-terminal) tags.

Note that:
- All external tags that return plain text (their property `terminal = True`) are terminal.
- All native hypertags that .......


## Modules

### Import

Special symbols available inside a Hypertag script: `__file__`, `__package__` - 
for proper interpretation of import paths. They can be initialized
through same-named arguments of Runtime.render() and Runtime.translate().

- absolute vs. relative import paths

### Export

Regular Python modules (.py files) can export symbols for use in Hypertag scripts.
Any global variable defined by a module that can be imported into another Python module
can also be imported to a Hypertag script as an object ($NAME).

Additionally, if a module defines a `__tags__` global - which should be a dict
with strings (tag names) as keys and Tag objects as values - the content of this 
dictionary can be imported as tags (%NAME) into a Hypertag script.


## Script execution

Execution of a Hypertag script constists of 3 phases:

1. **parsing** (script > AST)
2. **translation** (AST > DOM) -- all *native* hypertags expanded, 
   external hypertags NOT expanded; DOM can be manipulated
3. **rendering** (DOM > markup)

Typically, the client code will call `Hypertag.render()` to perform all the above 
steps at once. In some cases, the client may wish to obtain the structured representation
of the resulting document - the DOM (Document Object Model) - for example, to manipulate
the DOM tree before it gets rendered. In such case, the client should call 
`Hypertag.translate()` and then `render()` on the resulting DOM tree.


**Environment** ... **context** consisting of any python objects can be provided ...

## SDK ??

- class Tag, ExternalTag, MarkupTag -- for implementing custom tags
- class HNode
- class Sequence
- class Environment

## Questions & Answers

If you have technical questions related to Hypertag, please post them
on [StackOverflow](https://stackoverflow.com/questions/ask) 
and tag them with, guess... the "**hypertag**" tag.

Other questions can be posted in the _Discussions_ section on Hypertag's page in GitHub.
