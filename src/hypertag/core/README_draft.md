## Introduction

<!---
If you want to build commercial websites with Hypertag
I can supervise or consult on your projects.
Please drop me an e-mail or contact me via LinkedIn.

Hypertag enables advanced control of document rendering process through
native **control blocks** (if-elif-else, for, while, try);
and let the programmer define **custom tags** (_hypertags_), either directly
in the document using Hypertag syntax (_native tags_), 
or as Python functions (_external tags_).
and provides high level of **modularity** through custom tags and import blocks. 
--->

## Cheet Sheet

### Control blocks

| &nbsp;<br> Syntax <br><img width=600/> | &nbsp;<br> Description <br>&nbsp; |
| ------------- | --------------- | 
| import $x <br> from ~ import $x as y <br> from hypertag.html import %a, %img <br> from PATH import $x, %TAG <br> | _import block_ reads a variable ($NAME) or a tag (%NAME) from another Hypertag or Python module (PATH) or from the dynamic context of rendering ("~" default) and adds it to the namespace of the current script |
| if COND &#124; _text_ <br> if COND:<br>&nbsp;&nbsp;&nbsp;&nbsp;BLOCKS...<br> elif: ... <br>else: ... | _if-elif-else_ construct behaves similarly as in Python; trailing colons (:) are optional |
| try-else | may have a body (inline, outline), but cannot be followed by tags on the same line |


| Symbol    | Syntax     | Description     |
| :-------: | --------------- | --------------- | 
| ?         |       | *optional block*; like a "try" without an "else" branch; can be applied to a tagged block (on the same line) |
| for       | for VAR in SEQ |
| while     | while EXPR |

Trailing colon (:) in a headline of a control block (for/while) or a clause (if/elif/else/try)
is _optional_ and can be omitted in most cases - with an exception for a mixed
text+structural body (text title in a headline + structural sub-blocks beneath),
which requires that a text marker in a headline is preceeded by a colon.

    box: | This box has both an inline "title" and a list of sub-blocks
        li : b | item 1
        li : b | item 2

## Terminology

**Headline**. The first line of a tagged or control block. 
Contains a tag, or multiple tags, or a keyword.

**Header**. The initial part of a headline, up to the last marker (see below).

**Marker**. A special symbol (one of &#124;/!@:) that marks the beginning of a body 
of a tagged or control block. Typically, there is exactly one marker in a headline,
though it can be omitted altogether (when a body starts in a new line).
There is also a special case when the colon (:) can be followed 
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


## Blocks

Contents of a text block may span multiple lines. The additional lines
must be indented more than the first line. Sub-indentation is preserved in the output:

    |   a text block
      may span
        multiple
      lines...

renders to

      a text block
    may span
      multiple
    lines...


### Tagged blocks

<!---
body layout: inline / outline / headline

The entire header must fit in the first line of a block.
For a body, there are several possibilities: it may follow directly after
the header on the same line (_inline body_), occupy subsequent lines
(_outline body_), mix both of these approaches (__), or contain a multi-line
text contents (_multiline body_).
--->

A **tag** is a function-like object belonging to the _tags namespace_ 
(see section ........) that performs some kind of transformation 
of the block's body represented by a DOM (see section .......).
The execution of this transformation is called **tag expansion**:
a DOM or a string is produced as a result, which is subsequently concatenated
with the output of adjacent blocks to form final output of script rendering.
Tag expansion can be moderated by values of attributes.

For example, the built-in tag `div` as provided by HyperHTML runtime 
wraps up the rendered body of a block with `<div>...</div>`
prefix and suffix during expansion, and pastes into the opening `<div>` 
any attributes that have been declared in the block.

Technically speaking, every tag is an instance of `hypertag.core.tag.Tag` that
accepts - through the method `Tag.expand()` - any number of positional 
and/or keyword arguments (attributes) plus the special _body_ argument 
that holds the DOM of a translated body of the tag's occurrence -
in the example above this would be a DOM holding two plain-text nodes.

<!---
The tag can perform any kind of processing of input DOM and 
returns a DOM or a string that will be concatenated with the output of adjacent blocks
to form the final output of rendering.
(See section ...... for details about DOM.)
--->

A tag can be implemented in Python (_external tag_) and imported to a script 
using an _import_ block (see section ......), or defined directly in Hypertag
using a _hypertag definition_ block (_native tag_, see section ......).
In both cases, the parser represents the tag internally as an instance
of a `hypertag.core.tag.Tag` subclass (`ExternalTag` or `NativeTag`, respectively).

Every Hypertag runtime may define a list of _built-in tags_ that will be imported
automatically when script parsing begins.
For example, `HyperHTML` provides built-in Tags for all valid HTML tags,
and there are two variants available for each tag: lower-case and upper-case.
(see section ....... for details).

 
### Special tags

#### Null tag (.)

Normally, a Hypertag script reads top-to-bottom through a vertical sequence of blocks;
however, it can also exhibit left-to-right arrangement of tags vs. textual contents. 
In blocks that could have a tag, but don't need one in a particular place,
you can put a dot "." instead of a tag name to provide valid indentation and still 
ensure consistent vertical alignment of *tags* on the left and *text* on the right,
like here:

    div:
        p
            i   | this line is in italics and so it requires a tag
            .   | this line needs no tags, hence the null tag is used as a placeholder 
            
The dot represents a _null tag_ that creates a node in the DOM (like any regular tag) 
but during rendering it passes the body unchanged to the output.
In other words, a _null tag_ serves as a placeholder that performs no processing 
of its body, similar to an identity function.

The null tag can also be used as a root node for a group of sub-blocks, 
to provide visual grouping in the source code and/or allow finer control
over node filtering and selection if the blocks were to be passed to a hypertag (as _@body_)
and processed with DOM selectors.

<!---
Typically, a null tag is used in either of two cases:

1. to vertically align text contents of mixed: tagged and untagged blocks;
   using a null tag allows all blocks to have the same indentation of text contents,
   even despite some blocks need more horizontal space for their (regular) tags;
1. to visually group in the script related blocks; note that sub-indentation of the
   dotted block will be preserved in the output.
--->

Both use cases are illustrated in the example below:

    h1                | TITLE
    .
        a href=$url   | click HERE!
        .             | to visit our website


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


### Hypertag definition

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

A hypertag definition block starts with "%" followed by spaces (optional),
then a name of new tag (obligatory), its attributes (optional) and formal body (optional). 
Default values in a form of literals or expressions can be provided for attributes.
If the first attribute on the list is prefixed with a special symbol "@",
this attribute will be assigned the actual body of the block of occurrence
(where the new tag is used); the "body" attribute can have an arbitrary name, 
but it cannot have a default value. If a body attribute is missing, the hypertag
is "void", which means its occurrences must always have empty contents.

An example hypertag definition looks like this:

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


### DOM embedding

    @ body
    @ body[0]
    @ body.METHOD()


### Assignments

A block that starts with $ marks an assignment to a local variable:

    $ x = 5
    $ dash = x * '-'
    $ title = dash + ' TITLE ' + dash


### Control blocks

#### Block "try"

Basic form:

    try ...
    else ...
    else ...

If there are no "else" branches, a try block can be written in a shorter form using `?`:

    ?tag ...
    ? tag ...
    ?
        block1
        block2

During translation, a "try" block returns a DOM generated by the first clause 
that does _not_ raise an exception; or an empty DOM if all clauses have failed
(the exception from the last clause is _not_ re-raised).

Note that here, the semantics of "else" is _opposite_ to what it is in Python, where
the "else" clause of a "try-else" statement only gets executed if _no_ exception occured.

All exceptions that inherit from Python's Exception are caught, including Hypertag exceptions.
There is no way to define a different set of exceptions to be caught.
Python's special exceptions that inherit directly from BaseException:
SystemExit, KeyboardInterrupt, GeneratorExit - are being passed up the tree.

Note that exceptions are caught during _translation_ of the block only.
If there are syntactical or name resolution errors (e.g., an undefined variable
was found in any clause), these errors are still passed up the tree.


#### Block "if"

#### Block "for"
    
- break & continue

#### Block "while"

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
  runtime

3. Import from a Hypertag script:

...

4. Import from a combined Python-Hypertag module:

...


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



### Indentation

Normally, _script indentation_ is stored in the DOM and translates to 
_output indentation_ of the text produced during rendering.
You can modify this behaviour and remove output indentation in two ways, by using:

- Dedent marker (<): removes output indentation of a single block
  the marker is used with
- Dedent tag (builtin): removes output indentation of all nested blocks
  (but the indentation of the dedent block itself stays untouched)

The _dedent marker_ and _dedent tag_ can be used together. Example:

    div
        < dedent : a
            p:    / These <p> blocks will be aligned with their parent (<a>) after rendering.
                b | Deeper-level nested block are dedented, too!
            p     / And the parent's indentation is removed, as well
                    (<a> is aligned with top-level <div>), thanks to 
                    the use of the <i>dedent marker</i>.


## Symbols

### Namespaces

During translation of a script to a DOM, Hypertag maintains two separate namespaces:

- **tags namespace**
- **variables namespace**

Only symbols in the tags namespace can be used as tags in tagged blocks.
Only symbols in the variables namespace can occur in expressions,
unless the `%` prefix is added to inform that a given symbol should be taken
from the tags namespace instead (NOT IMPLEMENTED YET).

The same name can be present in both namespaces at the same time and link to different 
objects _without_ causing a collission. This is an important feature when 
generating HTML documents. The HTML defines dozens of tags, whose names are fixed 
and often very short (i, b, p, code, form, head, body, ...) - 
without separation of namespaces, they would often collide with names 
commonly used by programmers for naming variables.

<!---
Maintaining separate namespaces is justified by the fact that in 
typical use cases - like HTML generation - there are dozens of predefined tags
with short names, all of which must be directly accessible. 
Many of these tags have very common names (i, b, p, code, form, head, body, ...),
and without separation of name spaces, name collissions between tags and local variables 
would be very frequent and lead to confusion. 
--->

The ways to add symbols to the two namespaces:

- Both namespaces can be initialized with built-in symbols by the runtime.
- Both namespaces can be extended with new symbols by `import` blocks.
- A hypertag definition block (`%...`) adds the name of a new tag to the tags namespace
  in the outer scope, while adding symbols of formal attributes to the variables
  namespace in the inner scope.
- Assignments (`$...`) and `for` blocks add symbols to the variables namespace.

### Name scoping

The two main namespaces (tags namespace, variables namespace) are _not_ flat, 
rather they are arranged in a hierarchy that follows the structure 
of the document (_hierarchical name scoping_). Every tagged block, 
as well as a hypertag definition block, creates a new branch in the namespace:
new symbols are only added to this branch; they are visible to sibling blocks 
at the same depth and to their sub-blocks, but are _not_ accessible from the outer scope.
For example:

    p
        $x = 1
        -- "x" can be accessed inside the paragraph
        | $x
    -- "x" cannot be accessed outside the paragraph

Obviously, symbols defined at a higher level can be overwritten at a lower level
down the document tree:

    $ x = 1
    p:
        $ x = 2
        | x inside the paragraph equals $x
    | x outside the paragraph equals $x

outputs:

    <p>
        x inside the paragraph equals 2
    </p>
    x outside the paragraph equals 1

Note that unlike tagged and definition blocks, control blocks do _not_ create new branches
in namespaces by themselves. Therefore, it is correct to assign a variable inside 
an if/try/for/while block and access its value in sibling blocks:

    if True:
        $x = 1
    else:
        $x = 2
    | x=$x is accessible in a sibling of a control block

outputs:

    x=1 is accessible in a sibling of a control block


## Expressions

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


### Operators

Hypertag implements majority of standard operators available in Python.

**Arithmetic and binary operators:**

    ** * / // %
    + - unary minus
    << >>
    & ^ |

**Logical operators:**

    == != >= <= < > in is "not in" "is not"
    not and or

A more general variant of the ternary "if-else" operator is available, 
with the "else" branch being optional, imputed with "else None" if missing:

    X if TEST else Y
    X if TEST

**Tail operators:**

    .     member access
    []    indexing
    ()    function call

Access to attributes of Python objects and elements of collections.
Calls to methods and functions.

**Slice operator** when used inside [...]:

    start : stop : step

Above these, Hypertag implements a non-standard binary **concatenation operator** (space),
as well as tail operators: **optional value** ("?") and **obligatory value** ("!").
They are described in next sections.


### Qualifiers: ? and !

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
    

## DOM

DOM = Document Object Model

### DOM classes

### DOM manipulation

Selectors as methods of DOM ...

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


## SDK ??

- class Tag, ExternalTag, Markup -- for implementing custom tags
- class DOM and inner classes (Node, Root, Text)
- class Runtime

## Questions & Answers

If you have technical questions related to Hypertag, please post them
on [StackOverflow](https://stackoverflow.com/questions/ask) 
and tag them with, guess... the "**hypertag**" tag.

Other questions can be posted in the _Discussions_ section on Hypertag's page in GitHub.

