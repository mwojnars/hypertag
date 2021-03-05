<!---
<style type="text/css" rel="stylesheet">
  div.highlight {
    max-height: 200px;
    overflow-y: auto;
  }
</style>
--->

## Introduction

Hypertag is a modern language for front-end development that allows
writing (X)HTML documents in a way similar to writing Python scripts,
where _indentation_ determines relationships between nested elements 
and hence removes the need for explicit closing tags.
Hypertag provides advanced control of page rendering with native control blocks, 
high level of modularity with Python-like imports,
unprecedented support for code reuse with native custom tags (_hypertags_),
and [much more](#why-to-use-hypertag). Authored by [Marcin Wojnarski](http://www.linkedin.com/in/marcinwojnarski).

**NOTE:** Hypertag is currently in Alpha phase. The documentation is under development.

### Usage

Install: _git clone_

Run in Python 3 (example):
```python3
from hypertag import HyperHTML

script = \
"""
    from ~ import $blue
    html: body:
        h1 style="color: $blue"
            / Example document with a <u>list of items</u>
        ul
            li | item <1>
            li | item no. {1+1}
        p : a href='http://hypertag.io' | See the Hypertag site for more!
"""

html = HyperHTML().render(script, blue = '#00f')
print(html)
```

The `script` in the code above is rendered to `html` as shown below
(see a [preview](http://htmlpreview.github.io/?https://github.com/mwojnars/hypertag/blob/main/test/sample_usage.html)):

```html
<html><body>
    <h1 style="color: #00f">
        Example document with a <u>list of items</u>
    </h1>
    <ul>
        <li>item &lt;1&gt;</li>
        <li>item no. 2</li>
    </ul>
    <p><a href="http://hypertag.io">See the Hypertag site for more!</a></p>
</body></html>
```

### Why to use Hypertag

- **Concise syntax**: inspired by Python, the indentation-based syntax is a lot cleaner, 
  more readable and maintainable than raw HTML; it requires less typing, is less redundant,
  and lets you concentrate on coding rather than chasing unmatched opening-closing tags.
- **Code reuse** by means of functions/classes is the corner stone of programming,
  yet it is missing from HTML; this is fixed now with Hypertag:
  programmers can create reusable components in a form of **custom tags** (_hypertags_), 
  defined either as Python functions (_external tags_) 
  or directly in a document using Hypertag syntax (_native tags_);
  hypertags can be parameterized and may represent complex pieces 
  of combined: content, style and layout - for a reuse across documents.
- **Fine-grained control** over rendering process is possible with
  a range of native _control blocks_ (for, while, if-elif-else, try-else) 
  constituting a core part of Hypertag syntax, unlike in templating languages, 
  where control structures are artificially overlaid on another language (HTML).
- **Modularity** in Hypertag is modeled after Python's: 
  every script may import tags and variables from other scripts,
  from Python modules, and from the dynamic _context_ of script rendering;
  scripts and modules are arranged into packages;
  with these mechanisms in place, building libraries of reusable components is easy and fun.
- **Applicability** to different target languages: 
  Hypertag is _not_ just a templating system added on top of HTML. 
  Hypertag is a full-featured standalone programming language tailored to the generation
  of documents of all kinds: by defining new tags, it can be adapted to produce an arbitrary
  document description language.
  
<!---
  Hypertag is *not* limited to (X)HTML; by defining new tags,
  it can be adapted to produce an arbitrary document description language.
HTML templating is one of applications, but Hypertag's capabilities are much bigger than that.
whose one of use cases is being a replacement for web templating languages.
--->

## Quick Start

### Blocks

A typical Hypertag script consists of nested blocks with tags:

    ul
        li 
            | This is the first item of a "ul" list.
            | Pipe (|) marks a plain-text block. HTML is auto-escaped: & < >
        li
            / This is the second item. 
              Slash (/) marks a <b>markup block</b> (no HTML escaping).
              Text blocks may consist of multiple lines, like here.
    p
        | Indentation of blocks gets preserved in the output.

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
<p>
    Indentation of blocks gets preserved in the output.
</p>
```

There are three types of _text_ blocks: _plain-text_ (|), _markup_ (/), _verbatim_ (!).
They differ in the way how embedded expressions and raw HTML are handled.

    | Plain-text block may contain {'em'+'bedded'} expressions & its output is HTML-escaped.
    / Markup block may contain expressions; output is not escaped, so <b>raw tags</b> can be used.
    ! In a verbatim $block$ {expressions} are left unparsed, no <escaping> is done.

output:

```html
Plain-text block may contain embedded expressions &amp; its output is HTML-escaped.
Markup block may contain expressions; output is not escaped, so <b>raw tags</b> can be used.
In a verbatim $block$ {expressions} are left unparsed, no <escaping> is done.
```

All the rules of text layout and processing as described in the next examples 
(inline text, multiline text etc.) hold equally for _all types_ of text blocks.
Spaces after special characters: |/!:$% - are never obligatory, and in some cases
(inside expressions) they may be disallowed.

### Tags

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

<!---
      Another example of how a multiline text-only block can be written
      using an initial "|" marker in the headline and no more markers thereafter.
--->

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

Inline (but not multiline) text can be combined with other sub-blocks if a colon (:)
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

If no inline content is present, a colon can optionally be put at the end of 
the block's headline. The two forms, with and without a trailing colon, are equivalent.

<!---
and so are the "div" blocks below:

    div:
      p | Some contents...
    
    div
      p | Some contents...
--->

Tags may have _attributes_ and can be _chained_ together with a colon `:`,
like the h1+b+a tags below:

    h1 class='big-title' : b : a href="http://hypertag.io" style="color:DarkBlue"
        | Tags can be chained together using a colon ":".
        | Each tag in a chain can have its own attributes.
        | Attributes are passed in a space-separated list, no parentheses.

output:

```html
<h1 class="big-title"><b><a href="http://hypertag.io" style="color:DarkBlue">
    Tags can be chained together using a colon ":".
    Each tag in a chain can have its own attributes.
    Attributes are passed in a space-separated list, no parentheses.
</a></b></h1>
```

Shortcut syntax can be used for the two most common HTML attribute names: 
.CLASS is equivalent to class=CLASS, and #ID means id=ID, for example:

    p #main-content .wide-paragraph | text...
    
output:

```html
<p id="main-content" class="wide-paragraph">text...</p>
```

### Expressions

A Hypertag script may define _variables_ to be used subsequently in _expressions_
inside plain-text and markup blocks, or inside attribute lists.
A variable is created by an _assignment block_ ($). 
Expressions are embedded in text blocks using {...}  or $... syntax - the latter can only
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

Each variable points to a Python object and can be used with all the same 
standard operators as in Python:

    ** * / // %
    + - unary minus
    << >>
    & ^ |
    == != >= <= < > in is "not in" "is not"
    not and or
    X if TEST else Y    - the "else" clause is optional and defaults to "else None"
    A:B:C               - array slice operator
    .                   - member access
    []                  - indexing
    ()                  - function call

To put a literal `{`, `}`, or `$` inside a text block you should use an escape string:
`{{`, `}}`, or `$$`. Hypertag supports also literal `None`, `False`, `True` and allows for 
creation of standard Python collections: _lists_, _tuples_, _sets_, _dictionaries_.
When creating sets and dicts, keep a space between the braces of a collection and the
surrounding embedding, otherwise the double braces `{{` and `}}` may be interpreted
as escape strings.

    | this is a list:   { [1,2,3] }
    | this is a tuple:  { (1,2,3) }
    | this is a set:    { {1,2,1,2} }
    | this is a dict:   { {'a': 1, 'b': 2} }

Output:

    this is a list:   [1, 2, 3]
    this is a tuple:  (1, 2, 3)
    this is a set:    {1, 2}
    this is a dict:   {'a': 1, 'b': 2}

Assignment blocks can handle _augmented assignments_, where multiple variables 
are assigned to, all at once:

    $ a, (b, c) = 1, (2, 3)

All identifiers (of variables and tags) are case-sensitive.
There are separate namespaces for tags and variables, so you don't need to worry
about possible name collissions between local variables and predefined tags: "a", "b", "i" etc.

Variables can also be imported from other Hypertag scripts and Python modules
using an _import_ block. Objects of any type can be imported in this way, 
including functions and classes:

    from python_module import $x, $y as z, $fun as my_function, $T as MyClass
    from hypertag_script import $name

    | fun(x) is equal $my_function(x)
    $ obj = MyClass(z)

The HyperHTML standard runtime understands the same _package.module_ syntax of import paths
as Python. This syntax can be applied to Python and Hypertag files alike:
the latter must have the ".hy" extension in order to be recognized.
The interpretation of import paths is runtime-specific, so some other (custom)
runtime classes could parse these paths differently, for instance, to enable the import 
of scripts from a DB instead of files, or from remote locations etc.
Wildcard import is supported: `from PATH import *`.

HyperHTML supports also a special import path "~" (tilde), which denotes 
the _dynamic context_ of script execution: a dictionary of all variables that have
been passed to the rendering method (`HyperHTML.render()`) as extra keyword arguments.
These variables can only be accessed in the script after they
have been _explicitly_ imported with `from ~ import ...`:

    from ~ import $width, $height
    
    | Page dimensions imported from the context: $width x $height

This script can be rendered in the following way:

```python3
html = HyperHTML().render(script, width = 500, height = 1000)
print(html)
```
and the output is:

    Page dimensions imported from the context: 500 x 1000


### Custom tags

One of the key features of Hypertag is the support for custom tags (_hypertags_)
that can be defined directly in a Hypertag script using _hypertag definition_ blocks (%):

    % tableRow name price='UNKNOWN'
        tr        
            td | $name
            td | $price

Here, `tableRow` is a custom tag that wraps up plain-text contents of table cells
with appropriate `tr` & `td` tags to produce a listing of products.
As you can see, a hypertag may accept attributes, and they can have default values,
similar to Python functions. A hypertag can be used with named (keyword) or unnamed attributes:

    table
        tableRow 'Porsche'  '200,000'
        tableRow 'Jaguar'   '150,000'
        tableRow 'Maserati' '300,000'
        tableRow name='Cybertruck'

What a clean piece of code it is compared to the always-cluttered HTML? 
In raw HTML, and in many templating languages too, you would need much more typing
to produce the same table:

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

No doubt which version is more readable and maintainable?

Imagine that at some point you decided to add a CSS class to all cells in the price column?
In HTML, you'd have to walk through all the cells and manually modify 
every single occurrence (HTML is notorious for [code duplication](https://en.wikipedia.org/wiki/Duplicate_code)!),
taking care not to modify `<td>` cells of another column accidentally.
In Hypertag, which provides powerful ways to deduplicate code, it is enough to modify
the hypertag definition adding `.style-price` in one place, and voilà:

    % tableRow name price='UNKNOWN'
        tr        
            td | $name
            td .style-price | $price

This definition can be moved out to a separate "utility" script,
or stay in the same file where it is being used, for easy maintenance - 
the programmer can choose whatever location is best in a given case.
In traditional templating languages, there are not so many choices:
often the best you can do is separate out duplicated HTML code into a Python function,
introducing code fragmentation along the way and spreading presentation code over 
different types of files (views vs. models) and languages (HTML vs. Python) - 
a very unclean and confusing approach.

Needless to say, hypertags can refer to other hypertags.
Even more, hypertag definitions can be nested: a hypertag can be defined inside another one,
such that it can only be used locally within the scope of the outer definition.

<!---
    % products items=[]
        % row name price
            tr        
                td | $name
                td | $price
        table        
            for item in items:
                row item.name item.price
--->

One more crucial element of the hypertag syntax is the _body attribute_.
Imagine that in the example above, we wanted to add another column containing
formatted (rich-text) information about a car model: funny quotes, pictures etc.
Passing it as a regular attribute is inconvenient, as we'd have to somehow encode
the entire HTML structure of the description: paragraphs, styles, images.
Instead, we can add a _body attribute_ (@) to the hypertag definition:

    % tableRow @info name price='UNKNOWN'
        tr
            td | $name
            td | $price
            td
               @ info           # this could be inlined instead:  td @ info

and then apply this hypertag to a non-empty _actual body_ which will be passed
in a structural form via the "info" attribute and will get printed in the right 
place inside the output table with all its rich contents and formatting preserved:

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

Note that there can only be one _body_ attribute in a hypertag; it must be the first one
on the list; it can be missing (then the tag is _void_ and its 
occurrences must have empty body); and it can have arbitrary name: we suggest _@body_ 
if there is no other meaningful alternative... 
Yes, any associations with Python's "self" are intended and well justified.

<!---
As you can see, Hypertag is much more concise than raw HTML, and with the help of custom
tags it enables cleaner separation between presentation logic (tags) and textual contents.
--->

Like variables, custom tags can also be imported from other Hypertag scripts and from 
Python modules. The syntax is a bit different, though. Because of separation of 
namespaces (variables vs. tags), every import block must clearly indicate whether
a particular symbol is a variable or a tag. This is done be prepending 
the imported name with `$` (a variable) or `%` (a tag).

    from my.utils import $variable
    from my.utils import %tag

<!---
This is something that differentiates hypertags from plain Python functions.
Sometimes it is useful to put comments that will be excluded from the output.
You can do this in Hypertag with either `--` or `#` prefix:

--->

### Filters

Hypertag defines a new operator not present in Python, the _pipeline_ (`:`), for use in expressions.
It is applied in a similar way as pipes `|` in templating languages:
to pass a result of an expression to a function (a _filter_) as its first argument,
without putting the entire expression inside the function-call parentheses,
as would normally be required. A typical example of filters in a templating language:

    title | truncate(50) | upper

this takes a `title` string, truncates it to no more than 50 characters and then converts 
to upper case. In Hypertag, this expression will look the same, except the pipes are
replaced with colons:

    title : truncate(50) : upper

Templating languages, like Jinja or Django's templates, require that functions are explicitly
declared as filters before they can be used in template code.
In Hypertag, there are _no_ such restrictions. Rather, all _callables_ (functions, methods,
class constructors etc.) can be used in pipelines without special preparation. 
A pipeline is just another syntax for a function call, so every expression of the form:

    EXPR : FUN(*args, **kwargs)

gets translated internally to:

    FUN(EXPR, *args, **kwarg)

Obviously, pipeline operators can be chained together, so `EXPR:FUN1:FUN2` is
equivalent to `FUN2(FUN1(EXPR))`. The function can be given as a compound expression,
such that the use of `obj.fun` or similar constructs is possible. For example, the standard
`str.upper` can be used instead of implementing a custom `upper()` function:

    'Hypertag' : str.upper : list : sorted(reverse=True)

output:

    ['Y', 'T', 'R', 'P', 'H', 'G', 'E', 'A']

<!---
Remember that all Python built-ins are available in Hypertag, that is why `str`, `list`,
`sorted` etc. are accessible without an explicit import.
--->
As an addition to the pipeline syntax, Hypertag provides seamless integration of Django's 
several dozens of well-known [template filters](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#built-in-filter-reference).
They can be imported from `hypertag.django.filters` and either called as regular functions
or used inside pipelines. Django must be installed on the system.

    from hypertag.django.filters import $slugify, $upper
    from hypertag.django.filters import $truncatechars, $floatformat

    | { 'Hypertag rocks' : slugify : upper }
    | { 'Hypertag rocks' : truncatechars(6) }
    | { '123.45' : floatformat(4) }
    
output:

    HYPERTAG-ROCKS
    Hyper…
    123.4500

Django's extra filters from [django.contrib.humanize](https://docs.djangoproject.com/en/3.1/ref/contrib/humanize/)
(the "human touch" to data) are also available:

    from hypertag.django.filters import $apnumber, $ordinal
    | "5" spelled out is "{ 5:apnumber }"
    | example ordinals {1:ordinal}, {2:ordinal}, {5:ordinal}

output:

    "5" spelled out is "five"
    example ordinals 1st, 2nd, 5th


### Control blocks

Control blocks of multiple types are available in Hypertag to help you manipulate input data
directly inside the document without going back and forth between Python and templating code.
The blocks are:

- **if-elif-else**
- **try-else**
- **for**
- **while**

The semantics of "if", "for", "while" blocks is analogous to what it is in Python.
Both inline and outline body is supported, although the former comes with restrictions:
the preceeding expression (a condition in "if/while", a collection in "for") may need to be
enclosed in (...) or {...}. Trailing colons in clause headlines are optional.

An example "if" block with outline body:

    $size = 5
    if size > 10      
        | large size
    elif size > 3:
        | medium size
    else
        | small size

output:

    medium size

The same code as above, but with inline body, notice the parentheses around expressions:

    $size = 5
    if (size > 10)    | large size
    elif (size > 3)   | medium size
    else              | small size

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

The "try" block differs from the corresponding Python statement.
It consists of a single "try" clause plus any number (possibly none) of "else" clauses.
The first clause that does _not_ raise an exception is returned.
All exceptions that inherit from Python's Exception are caught.
Empty string is rendered if all clauses fail.

Exceptions are checked only after semantic analysis, so if there are any syntactical 
or name resolution errors (e.g., an undefined variable in a clause), they are still being raised.
Also, note that the semantics of "else" is _opposite_ to what it is in Python,
where the "else" clause of a "try-else" statement only gets executed if _no_ exceptions occured.

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

There is a shortcut version "?" of the "try" syntax. 
It can only be used without "else" clauses, to suppress exceptions:

    ? | Price of Opel is $cars['opel'].

Importantly, the shortcut "?" _can_ be used as a prefix (on the same line) 
with a tagged block, which is not possible with the basic syntax. 
The code below renders empty string instead of raising an exception:

    ? b : a href=$cars.url | the "a" tag fails because "cars" has no "url"

The "try" block is particularly useful when combined with expression
_qualifiers_: "optional" (`?`) and "obligatory" (`!`), placed at the end
of (sub)expressions to mark that a given piece of calculation either:

- can be ignored (replaced with `''`) if it fails with an exception (`?`); or
- must be non-empty (not false), otherwise an exception will be raised (`!`).

Together, these language constructs enable fine-grained control over data post-processing,
sanitization and display.
They can be used to verify the availability of particular elements of input data
(keys in dictionaries, attributes of objects) and to easily create alternative paths 
of calculation that will handle multiple edge cases at once.

    try | Price of Opel is {cars['opel']? or cars['audi'] * 0.8}

In the above code, the price of Opel is not present in the dictionary, but thanks 
to the "optional" qualifier `?`, a KeyError is caught early, and a fallback is used 
to approximate the price from another entry. The output:

    Price of Opel is 64000.0

The "obligatory" qualifier `!` can be used to verify that a variable has a non-default 
(non-empty) value, and adapt the displayed message accordingly, with no need for 
a more verbose if-else test:

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

Qualifiers can be used in loop headlines, as well, to test for non-emptiness
of collections to be iterated over:

    try
        for p in products!
            | $p.name costs $p.price
    else
        | No products currently available.

When passed `$products=[]`, the above code outputs:

    No products currently available.

Qualifiers can be used after all atomic expressions and embeddings, no space is allowed.


### Built-ins

When using HyperHTML runtime, all Python built-in symbols (`builtins.*`) are automatically
imported as variables at the beginning of script rendering, so all commonly used Python
types and functions: `list`, `set`, `dict`, `int`, `min`, `max`, `enumerate`, `sorted` etc., 
are available to a script.

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

As mentioned earlier, Hypertag allows easy import of Django template filters to be used as
standalone functions or inside pipelines.

Additionally, Hypertag provides a number of predefined tags and functions:

1. General-purpose tags.
2. Functions & filters.
3. HTML-specific tags.

All of the above are automatically imported as built-in symbols by HyperHTML runtime.

(TODO...)


### Extras

There is a number of additional elements of Hypertag that have not been mentioned so far.
These include:

- The _dedent_ modifier (`<`): when put at the beginning of a block's headline,
  it decreases the output indentation of this block by one level (makes the indentation
  equal to the parent's). The dedent modifier can be used with all types of blocks, 
  including tagged and control blocks.
- The _append_ modifier (`...`): when put at the beginning of a block, it marks that
  this block is a continuation and should be appended to the previous one without a newline.
- The `pass` keyword can be used in place of a block, as an "empty block" placeholder.
  This quasi-block generates no output, similarly to the `pass` keyword in Python. 
  The use of `pass` is never enforced by the syntax: empty body is always a valid alternative
  and can be used inside parent blocks of all types. In some cases, though, the use of 
  explicit `pass` may be preferred due to aesthetic considerations.
- In expressions, you can create literal strings with the `'...'` and `"..."` syntax.
  This actually creates _formatted strings_ (equivalent to Python's f-strings),
  which may contain _embedded expressions_ of both the `$...` and `{...}` form.
  If you want to create raw strings instead, such that `$` and `{}` are treated as regular
  characters, the `r'...'` and `r"..."` syntax shall be used.
- Hypertag provides a special _concatenation operator_. If multiple expressions are put 
  one after another separated by 1+ whitespace (a space is the operator): EXPR1 EXPR2 EXPR3 ...
  their values get automatically converted to strings `str(EXPR)` and concatenated.
  This is an extension of Python syntax for concatenating literal strings, like in:
  `'Hypertag '  "is"   ' cool'` which is parsed into a single string: `'Hypertag is cool'`.
  In Python, this works for literals only, while in Hypertag, all types of expressions
  can be joined in this way. The concatenation operator has lower priority than binary "or" (`|`)
  and a pipeline (`:`); and higher than comparisons.

There are also some _gotcha!_ you need to keep in mind when coding with Hypertag:

- Inside dicts `{...}` and array slices `[a:b:c]`, operators other than arithmetic and bitwise 
  must be enclosed in parentheses. This is to avoid ambiguity of the colon ":",
  which normally serves as a pipeline operator, but in dicts and slices plays a role 
  of a field separator.
- So far, Hypertag hasn't been yet optimized for performance.


## Cheat Sheet

### Text blocks

| &nbsp;<br> Syntax <br><img width=200/> | &nbsp;<br> Description <br>&nbsp; |
| ------------- | --------------- | 
| &#124; _text_   | plain-text block; may contain embedded expressions; output is HTML-escaped |
| / markup        | markup block; may contain embedded expressions; output is *not* HTML-escaped |
| ! _verbatim_    | verbatim block; expressions are *not* parsed; output is *not* HTML-escaped |
| &#124; _multi-line_<br>&nbsp;&nbsp;_text....._ | text blocks may span *multiple lines*, also when preceded by a tag; subsequent lines must be indented |
| -- _comment_ <br> # _comment_ | line of comment; is excluded from output; may occur at the end of a block's headline (_inline comment_) or on a separate line (_block comment_) |
| < BLOCK       | _dedent marker_ (<): when put on the 1st line of a BLOCK, causes the output to be dedented by one level during rendering; applies to blocks of all types (text, control etc.) |

### Expressions

| &nbsp;<br> Syntax <br><img width=150/> | &nbsp;<br> Description <br>&nbsp; |
| :------:          | --------------- | 
| $x = a-b          | assignment block; space after $ is allowed |
| $x <br> $x.v[1]   | embedding of a factor expression (a variable with 0+ tail operators) in a text block or string |
| {x+y}             | embedding of an arbitrary expression in a text block or string |
| x! <br> {x*y}!    | "obligatory" qualifier (!) for an atomic or embedded expression; raises as exception if the expression is false |
| x? <br> {x*y}?    | "optional" qualifier (?) for an atomic or embedded expression; replaces exceptions and false values with empty strings |
| 'text'    | f-string (formatted string), may contain embedded expressions: $... and {...} |
| "text"    | f-string (formatted string), may contain embedded expressions: $... and {...} |
| r'text'   | r-string (raw string), expressions are left unparsed |
| r"text"   | r-string (raw string), expressions are left unparsed |
| $$        | escape string; renders $ in a plaintext/markup block and inside formatted strings |
| {{        | escape string; renders { in a plaintext/markup block and inside formatted strings |
| }}        | escape string; renders } in a plaintext/markup block and inside formatted strings |
<!---
| %TAG      | reference to a tag in an expression (_not implemented yet_) |
--->

### Tags

| &nbsp;<br> Syntax <br><img width=700/> | &nbsp;<br> Description <br>&nbsp; |
| ------------- | --------------- | 
| div <br>&nbsp;&nbsp;&nbsp;&nbsp; p &#124; _text_  | _tagged block_ starts with a tag name (_header_) that can be followed by contents (_body_) on the same line (_inline body_) and/or on subsequent lines (_outline body_) |
| p &#124; _this is_<br>&nbsp;&nbsp;&nbsp;&nbsp; _a multiline_<br>&nbsp;&nbsp;&nbsp;&nbsp; _paragraph_ | a tagged block with exclusively text contents may span multiple lines |
| box: &#124; _Title_<br>&nbsp;&nbsp;&nbsp; li &#124; _item1_<br>&nbsp;&nbsp;&nbsp; li &#124; _item2_ | mixing inline and outline contents is possible when the colon (:) and a text-block marker (&#124;/!) are both present |
| h1 : b : a href='' : <br>&nbsp;&nbsp;&nbsp;&nbsp; &#124; _text_  | tags can be chained together using colon (:); trailing colon is optional |
| box "top" x=1.5 <br>a href=$url <br>a href={url} | unnamed and named (keyword) attributes can be passed to a tag in a space-separated list, no parentheses; expressions can be used as values |
| %SUM x y=0 &#124; _sum is_ {x+y}<br>%TAB @cells n:<br>&nbsp;&nbsp;&nbsp;&nbsp; &#124; _Table no. $n_<br>&nbsp;&nbsp;&nbsp;&nbsp; @cells | _hypertag definition_ block (%) may declare attributes, possibly with defaults, and may have a body; the "at" sign (@) marks a special attribute that will hold actual body of hypertag's occurrence: without this attribute the hypertag is _void_ (must have empty contents in places of occurrence) |
| @body <br> @body[2:] | _embedding block_ (@): inserts DOM nodes represented by an expression (typically a body attribute inside hypertag definition) |
| div .CLASS        | (shortcut) equiv. to *class="CLASS"* on attributes list of a tag |
| div #ID           | (shortcut) equiv. to *id="ID"* on attributes list of a tag |
| pass              | "empty block" placeholder; generates no output, does *not* accept attributes nor a body |
| . <br> . &#124; _text_ | the special _null tag_ (.) outputs its body without changes; helps improve vertical alignment of text in adjecent blocks; does *not* accept attributes |
<!---
| TAG x=1.0 y={v+1} | named (keyword) attributes of a tag occurrence; space-separated, no parentheses |
| TAG "yes" 3 True  | unnamed attributes of a tag occurrence; values are matched to formal attributes in a way similar to how Python matches function arguments (by order) |
--->


## Acknowledgements

Hypertag was inspired by indentation-based templating languages:
[Slim](http://slim-lang.com/), [Plim](https://plim.readthedocs.io/en/latest/index.html),
[Shpaml](http://shpaml.com/), [Haml](https://haml.info/).
