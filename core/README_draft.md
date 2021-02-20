## Introduction

Hypertag is a modern language for front-end development that allows
writing (X)HTML pages and other types of documents in a way similar to writing a Python script,
where indentation marks nested HTML elements and thus removes the need for explicit
closing tags. 

Hypertag enables advanced control of document rendering process through
native **control blocks** (if-elif-else, for, while, try) and provides **modularity** 
through custom tags and import blocks. 

Why to use Hypertag:
- less typing; cleaner code 
- no need to remember about (reduntant) closing tags; no more unmatched open-closing tags
- unprecedented support for **modularity** and **code re-use**

<!--- (TODO)
- Object-Oriented Programming (**OOP**) inside markup,
  through native language structures (???)
  
- high performace in web applications achieved through caching of parsed AST,
  combined with their **compactification**: constant parts of the AST are
  pre-rendered and merged into single nodes, to avoid repeated rendering
  with every web page request.
--->

If you try Hypertag, you will never go back to an old-school templating language.

## Quick Start

## Cheat Sheet

| Symbol | Description |
| ------ | --------------- | 
| %tag ...  | hypertag definition block |
| %tag      | reference to a tag in an expression |
| @body     | body attribute in attributes list of a hypertag definition |
| @body[1:] | DOM embedding block  |
| $x=       | assignment block |
| $x        | expression embedding in a text block or string |
| {x}       | expression embedding in a text block or string |
| x!        | obligatory qualifier for an expression |
| x?        | optional qualifier for an expression |
| ? ...     | "try" block |
| < ...     | "dedent" marker for a block |
| &#124; text   | normal text block (may contain expressions, will be HTML-escaped) |
| / text        | markup text block (may contain expressions, will NOT be HTML-escaped) |
| ! text        | verbatim text block (expressions will NOT be parsed, text will NOT be HTML-escaped) |
| -- comment    | block or inline comment |
| # comment     | block or inline comment |
| .CLASS    | shortcut attribute in a tagged block, same as: class="CLASS" |
| #ID       | shortcut attribute in a tagged block, same as: id="ID" |
| r'text'   | r-string (raw string), no embedded expressions |
| r"text"   | r-string (raw string), no embedded expressions |
| 'text'    | f-string (formatted string), may contain embedded expressions: $... and {...} |
| "text"    | f-string (formatted string), may contain embedded expressions: $... and {...} |
| $$        | escape string to render $ in a normal/markup text block and inside formatted strings |
| {{        | escape string to render { in a normal/markup text block and inside formatted strings |
| }}        | escape string to render } in a normal/markup text block and inside formatted strings |


## Terminology

- block
- body
- tag, attributes
- script >  AST > DOM ... tree, node, body
- rendering

((?? move Script Execution here))


## Syntax

### Basic blocks

#### Text blocks

Normal, markup, verbatim:

    | normal block with {'em'+'bedded'} $expressions
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

- tags chain (:)
- body: inline / outline / headline
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
