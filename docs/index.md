<style type="text/css" rel="stylesheet">
    header h1 { text-transform: uppercase; }

    /*.tag-h1 { text-decoration: underline }*/
    /*.tag-h2 { font-weight: bold; }*/

    body {
     font:16px/24px 'Quattrocento Sans', "Helvetica Neue", Helvetica, Arial, sans-serif;
     color:#333;
    }
    
    section {
      /* width: 590px; */
      width: 850px;
      /* padding: 30px 30px 50px 30px; */
      padding: 40px 50px 50px 50px; 
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
        max-height: 176px;
        overflow-y: auto;
    }

    pre {
      /* background: #333333; */
      /* background: #444; */
      background: #f4f6f8;                  /* #f9f7f4; */
      /* border: 1px solid #c7c7c7; */
      border: 1px solid #ddd;
    }
    code {
      /* background: #333; */
      /* background: #444; */
      background: #f4f6f8;
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
    a {
      /* color: #3399cc; */
      color: #0594db;
    }
</style>


# Introduction

Hypertag is a modern language for front-end development that allows
writing (X)HTML documents in a way similar to writing Python scripts,
where _indentation_ determines relationships between nested elements 
and removes the need for explicit closing tags.
Hypertag provides advanced control of page rendering with native control blocks;
high level of modularity thanks to Python-like imports; unprecedented support for code reuse 
with native custom tags (_hypertags_), and more. 
If you are new to Hypertag, see the [Github page](https://github.com/mwojnars/hypertag)
and a [Quick Start](https://github.com/mwojnars/hypertag#quick-start) for a brief introduction.

Authored by [Marcin Wojnarski](http://www.linkedin.com/in/marcinwojnarski).

**NOTE:** Hypertag is currently in Alpha phase. The documentation is under development.

## Install

(TODO)

# Language Reference

## Blocks

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

## Layout

All top-level blocks in a document (or sub-blocks at any given depth)
must have the _same indentation_. Both a space (` `) and a tab character (`\t`)
can be used for indenting, although we recommend only using spaces to avoid confusion:
two indentation strings are considered the same if and only if they are equal
in Python sense, which means that a space in one line cannot be replaced with a tab
in another equally-indented line. These are similar rules as in Python.

All the rules of text layout and processing as described in the next examples 
(inline text, multiline text etc.) hold equally for _all types_ of text blocks.
Spaces after special characters: |/!:$% - are never obligatory, and in some cases
(inside expressions) they may be disallowed.

Sometimes it is useful to put comments that will be excluded from the output.
This can be done using either `--` or `#` prefix.

## Tags

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

If no inline content is present, a colon can optionally be put at the end of 
the block's headline. The two forms, with and without a trailing colon, are equivalent.

<!---
and so are the "div" blocks below:

    div:
      p | Some contents...
    
    div
      p | Some contents...
--->

Tags may have _attributes_ and can be _chained_ together using a colon `:`,
like the three tags below:

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

## Expressions

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

Each variable points to a Python object and can be used with all the standard operators
known from Python:

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
`{%raw%}{{{%endraw%}`, `{%raw%}}}{%endraw%}`, or `$$`. Hypertag supports also literal 
`None`, `False`, `True` and allows for creation of standard Python collections: 
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

Assignment blocks support _augmented assignments_, where multiple variables 
are assigned to all at once:

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

```python
html = HyperHTML().render(script, width = 500, height = 1000)
print(html)
```
and the output is:

    Page dimensions imported from the context: 500 x 1000


## Custom tags

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
               @ info           # inline form can be used, as well:  td @ info

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

There can only be one _body_ attribute in a hypertag; it must be the first one
on the list; it can be missing (then the tag is _void_ and its 
occurrences must have empty body); and it can have arbitrary name: we suggest _@body_ 
if there is no other meaningful alternative... 
Yes, any associations with Python's "self" are intended and well justified.

<!---
As you can see, Hypertag is much more concise than raw HTML, and with the help of custom
tags it enables cleaner separation between presentation logic (tags) and textual contents.
--->

Like variables, custom tags can also be imported from other Hypertag scripts and from 
Python modules. Because of separation of namespaces (variables vs. tags),
every import block must clearly indicate whether a particular symbol is a variable or a tag.
This is done be prepending the imported name with `$` (a variable) or `%` (a tag).

    from my.utils import $variable
    from my.utils import %tag

<!---
This is something that differentiates hypertags from plain Python functions.
--->

## Filters

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
class instantiation etc.) can be used in pipelines without special preparation. 
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

Hypertag seamlessly integrates all of Django's [template filters](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#built-in-filter-reference).
They can be imported from `hypertag.django.filters` and either called as regular functions
or used inside pipelines. Extra filters from [django.contrib.humanize](https://docs.djangoproject.com/en/3.1/ref/contrib/humanize/)
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


## Control blocks

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

There is a shortcut version "?" of the "try" syntax which
can only be used without "else" clauses, to suppress exceptions:

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

With the "obligatory" qualifier `!` one can verify that a variable has a non-default 
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


## Built-ins

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


## Extras

There is a number of additional elements of Hypertag that have not been mentioned so far.
These include:

- The _dedent_ modifier (`<`): when put at the beginning of a block's headline,
  it decreases the output indentation of this block by one level (makes the indentation
  equal to the parent's). The dedent modifier can be used with all types of blocks, 
  including tagged and control blocks.
- The _append_ modifier (`...`): when put at the beginning of a block, it marks that
  this block is a continuation of the previous block and should be appended to it without a newline.
  There should be no empty line between the two blocks, otherwise a newline will still be inserted.
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


