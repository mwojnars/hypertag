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
writing HTML5 and other markup documents in a way similar to writing Python scripts,
where _indentation_ determines relationships between nested elements 
and removes the need for explicit closing tags.
Hypertag provides advanced control of page rendering with native control blocks;
high level of modularity thanks to Python-like imports and DOM manipulation; 
unprecedented support for code reuse with native custom tags (_hypertags_), 
and [more](#why-to-use-hypertag). 
See the [Quick Start](#quick-start) below, or the 
[Language Reference](http://hypertag.io) for details.

Authored by [Marcin Wojnarski](http://www.linkedin.com/in/marcinwojnarski).

<!---
**NOTE:** Hypertag is currently in Alpha phase. The documentation is under development.
--->

### Setup

Install: _git clone_

Usage:
```python
from hypertag import HyperHTML
html = HyperHTML().render(script)       # rendering of a Hypertag `script` to HTML
```

<!---
Run in Python 3 (example):
```python
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
--->

### Why to use Hypertag

- **Concise syntax**: inspired by Python, the indentation-based syntax is a lot cleaner, 
  more readable and maintainable than raw markup; it requires less typing, is less redundant,
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
  where control structures are artificially overlaid on top of another language (HTML).
- **Modularity** in Hypertag is modeled after Python's: 
  every script may import tags and variables from other scripts,
  from Python modules, and from the dynamic _context_ of script rendering;
  scripts and modules are arranged into packages;
  with these mechanisms in place, building libraries of reusable components is easy and fun.
- **Applicability** to different target languages. 
  Hypertag is _not_ just a templating system put on top of HTML. 
  Hypertag is a full-featured standalone programming language tailored to the generation
  of documents of all kinds. By defining new tags, Hypertag can be adapted to produce an arbitrary
  document description language.
  
<!---
- **Code reuse** by means of functions/classes is the corner stone of programming,
  yet it is missing from HTML; this is fixed now with Hypertag:
  programmers can create reusable components in a form of **custom tags** (_hypertags_), 
  defined either as Python functions (_external tags_) 
  or directly in a document using Hypertag syntax (_native tags_);
  hypertags can be parameterized and may represent complex pieces 
  of combined: content, style and layout - for a reuse across documents.
- **DOM manipulation**:

  Hypertag is *not* limited to (X)HTML; by defining new tags,
  it can be adapted to produce an arbitrary document description language.
  HTML templating is one of applications, but Hypertag's capabilities are much bigger than that.
  whose one of use cases is being a replacement for web templating languages.
- **consistency** (monolithic architecture): Hypertag combines presentation and logic in one language; 
  you no longer have to mix presentation code (HTML) with foreign syntax of a 
  templating language, or PHP etc.
- **Object-Oriented Programming** (OOP) inside markup, through native language structures (??)
- **high performace** in web applications achieved through caching of parsed AST,
  combined with their **compactification**: constant parts of the AST are
  pre-rendered and merged into single nodes, to avoid repeated rendering
  with every web page request.

If you try Hypertag, you will never miss old-school HTML templating.
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

Indentation of blocks gets preserved in the output during rendering:

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

There are three types of _text_ blocks: _plain-text_ (|), _markup_ (/), _verbatim_ (!).

    | Plain-text block may contain {'em'+'bedded'} expressions & its output is HTML-escaped.
    / Markup block may contain expressions; output is not escaped, so <b>raw tags</b> can be used.
    ! In a verbatim $block$ {expressions} are left unparsed, no <escaping> is done.

output:

```html
Plain-text block may contain embedded expressions &amp; its output is HTML-escaped.
Markup block may contain expressions; output is not escaped, so <b>raw tags</b> can be used.
In a verbatim $block$ {expressions} are left unparsed, no <escaping> is done.
```

### Tags

Content of a tagged block can be arranged as _inline_, _outline_ ("out of the line"),
or mixed inline+outline. Inline content starts right after the tag in the _headline_ 
and is rendered to a more compact form.

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

Without a colon, all content is interpreted as _multiline_ text:

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

Tags may have _attributes_ and can be _chained_ together using a colon `:`, like here:

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

Shortcuts are available for the two most common HTML attributes: 
`.CLASS` is equivalent to `class=CLASS`, and `#ID` means `id=ID`.

    p #main-content .wide-paragraph | text...
    
output:

```html
<p id="main-content" class="wide-paragraph">text...</p>
```


### Expressions

A Hypertag script may define _variables_ to be used in _expressions_
inside plain-text and markup blocks, or inside attribute lists.
A variable is created by an _assignment block_ ($). 
Expressions are embedded in text blocks using `{...}`  or `$...` syntax:

    $ k = 3
    $ name = "Ala"
    | The name repeated $k times is: {name * k}
    | The third character of the name is: "$name[2]"

output:

```html
The name repeated 3 times is: AlaAlaAla
The third character of the name is: "a"
```

Assignment blocks support _augmented assignments_:

    $ a, (b, c) = [1, (2, 3)]

Each variable points to a Python object and can be used with all the standard operators
known from Python:

    ** * / // %
    + - unary minus
    << >>
    & ^ |
    == != >= <= < > in is "not in" "is not"
    not and or
    X if TEST else Y    - the "else" clause is optional and defaults to "else None"
    A:B:C               - slice operator inside [...]
    .                   - member access
    []                  - indexing
    ()                  - function call

Python collections: _lists_, _tuples_, _sets_, _dictionaries_, can be created in a standard way:

    | this is a list:   { [1,2,3] }
    | this is a tuple:  { (1,2,3) }
    | this is a set:    { {1,2,1,2} }
    | this is a dict:   { {'a': 1, 'b': 2} }

output:

    this is a list:   [1, 2, 3]
    this is a tuple:  (1, 2, 3)
    this is a set:    {1, 2}
    this is a dict:   {'a': 1, 'b': 2}

Variables can be imported from other Hypertag scripts and Python modules using an _import_ block:

    from python_module import $x, $y as z, $fun as my_function, $T as MyClass
    from hypertag_script import $name

    | fun(x) is equal $my_function(x)
    $ obj = MyClass(z)

Wildcard import is supported: 

    from PATH import *

A special import path `~` (tilde) denotes the _dynamic context_ of script execution: 
a dictionary of all variables that have been passed to the rendering method 
as extra keyword arguments.

    from ~ import $width, $height
    
    | Page dimensions imported from the context: $width x $height

The above script can be rendered in the following way:

```python
html = HyperHTML().render(script, width = 500, height = 1000)
print(html)
```
and the output is:

    Page dimensions imported from the context: 500 x 1000


### Custom tags

Custom tags (_hypertags_) can be defined directly in a Hypertag script 
using _hypertag definition_ blocks (%):

    % tableRow name price='UNKNOWN'
        tr        
            td | $name
            td | $price

A hypertag may declare attributes, possibly with default values. 
In places of occurrence, hypertags accept positional (unnamed) and/or keyword (named) attributes:

    table
        tableRow 'Porsche'  '200,000'
        tableRow 'Jaguar'   '150,000'
        tableRow name='Cybertruck'

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
        <td>Cybertruck</td>
        <td>UNKNOWN</td>
    </tr>
</table>
```

<!---
If, at some point, you decided to add a CSS class `.style-price` to all cells in the price column,
it is enough to modify the hypertag definition instead of walking through
all the rows and manually updating corresponding `td` occurrences:

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

Let's say you wanted to add another column containing formatted (rich-text) information 
about a car model: funny quotes, pictures etc. Passing it as a regular attribute would be
difficult, as you'd have to somehow encode the entire HTML structure: paragraphs, styles, images.
Instead, you can add a special _body attribute_ (@) to the hypertag definition:
--->

If you want to pass structured (rich-text) data to a hypertag, you can declare 
a _body attribute_ (@) in the hypertag definition block, and then paste its contents
in any place you wish:

    % tableRow @info name price='UNKNOWN'
        tr
            td | $name
            td | $price
            td
               @ info           # inline form can be used as well:  td @ info

This special attribute will hold the _actual body_ of hypertag's occurrence, 
represented as a tree of nodes of Hypertag's native Document Object Model (DOM),
so that all rich contents and formatting are preserved:
<!---
This special attribute (here, `info`; an arbitrary name can be chosen) will hold the 
_actual body_ of hypertag's occurrence and will pass it in a structured form of the 
Hypertag's native Document Object Model (DOM), so that all rich contents and formatting 
are preserved:
--->

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

output:
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

<!---
There can only be one _body_ attribute in a hypertag; it must be the first one
on the list; it can be missing (then the tag is _void_ and its 
occurrences must have empty body); and it can have arbitrary name: we suggest _@body_ 
if there is no other meaningful alternative... 
Yes, any associations with Python's "self" are intended and well justified.
--->

Like variables, tags can also be imported from Hypertag scripts and Python modules.
Due to separation of namespaces (variables vs. tags), all symbols must be 
prepended with either `$` (denotes a variable) or `%` (a tag):

    from my.utils import $variable
    from my.utils import %tag


### Filters

Hypertag defines a colon `:` as a _pipeline operator_ that allows functions (and all callables)
to be used in expressions as chained _filters_. A pipeline expression of the form:

    EXPR : FUN(*args, **kwargs)

gets translated internally to:

    FUN(EXPR, *args, **kwarg)

For example, the expression:

    'Hypertag' : str.upper : list : sorted(reverse=True)

evaluates to:

    ['Y', 'T', 'R', 'P', 'H', 'G', 'E', 'A']

Functions do _not_ have to be explicitly registered as filters before use, unlike in
popular templating languages (Jinja, Django templates etc.).

<!---
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

Obviously, pipeline operators can be chained together, so `EXPR:FUN1:FUN2` is
equivalent to `FUN2(FUN1(EXPR))`. The function can be given as a compound expression,
such that the use of `obj.fun` or similar constructs is possible. For example, the standard
`str.upper` can be used instead of implementing a custom `upper()` function:

    'Hypertag' : str.upper : list : sorted(reverse=True)

output:

    ['Y', 'T', 'R', 'P', 'H', 'G', 'E', 'A']

Remember that all Python built-ins are available in Hypertag, that is why `str`, `list`,
`sorted` etc. are accessible without an explicit import.
--->

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


### Control blocks

There are _control blocks_ in Hypertag: "if", "try", "for", "while". For example:

    $size = 5
    if size > 10      
        | large size
    elif size > 3:
        | medium size
    else
        | small size

output:

    medium size

Clauses may have inline body; notice the parentheses around expressions:

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

The "try" block consists of a single `try` clause plus any number (possibly none) of `else` clauses.
The first clause that does _not_ raise an exception is returned.
All exceptions that inherit from Python's Exception are caught (this cannot be changed). Example:

    $cars = {'ford': 60000, 'audi': 80000}
    try
        | Price of Opel is $cars['opel'].
    else
        | Price of Opel is unknown.

output (the 'opel' key is missing in the dictionary):

    Price of Opel is unknown.

<!---
Similar code as above, but with inline body:

    $cars = {'ford': 60000, 'audi': 80000}
    
    try  | Price of Opel is $cars['opel'].
    else | Price of Opel is not available, but how about Seat: $cars['seat'].
    else | Neither Opel nor Seat is available.
           Let's stick with a Ford: $cars['ford'].

output:

    Neither Opel nor Seat is available.
    Let's stick with a Ford: 60000.
--->

There is a shortcut version "?" of the "try" syntax, which has no "else" clauses, so its 
only function is to suppress exceptions:

    ? | Price of Opel is $cars['opel'].

Importantly, unlike the basic form of "try", the shortcut "?" can prepend a tagged block. 
The code below renders empty string instead of raising an exception:

    ? b : a href=$cars.url | the "a" tag fails because "cars" has no "url" member

The "try" block is particularly useful when combined with _qualifiers_: 
"optional" (`?`) and "obligatory" (`!`), placed at the end of (sub)expressions to mark 
that a given piece of calculation either:

- can be ignored (replaced with `''`) if it fails with an exception (`?`); or
- must be non-empty (not false), otherwise an exception will be raised (`!`).

Together, these language constructs enable fine-grained control over data post-processing,
sanitization and display.
They can be used to verify the availability of particular elements of data
(keys in dictionaries, attributes of objects) and create alternative paths of calculation 
that will handle multiple edge cases at once:

    | Price of Opel is {cars['opel']? or cars['audi'] * 0.8}

In the above code, the price of Opel is not present in the dictionary, but thanks 
to the "optional" qualifier `?`, a KeyError is caught early, and a fallback is used 
to approximate the price from another entry:

    Price of Opel is 64000.0

With the "obligatory" qualifier `!` one can verify that a variable has a non-default 
(non-empty) value, and adapt the displayed message if not:

    % display name='' price=0
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

When initialized with `$products=[]`, the above code outputs:

    No products currently available.

<!---
Qualifiers can be placed after all atomic expressions and embeddings, no space is allowed.
--->

### Built-ins

HyperHTML runtime automatically imports all Python built-in symbols (`builtins.*`) 
at the beginning of script rendering, so all common types and functions: 
`list`, `set`, `dict`, `int`, `min`, `max`, `enumerate`, `sorted` etc., 
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

Additionally, Hypertag provides a number of predefined tags and functions:

1. General-purpose tags.
2. Functions & filters.
3. HTML-specific tags.

All of the above are automatically imported as built-in symbols by HyperHTML runtime.

(TODO...)

### Further reading

There are still many features in Hypertag that have not been mentioned 
in this Quick Start: [pipelines & filters](http://hypertag.io/#filters) (`:`); 
block layout [modifiers](http://hypertag.io/#modifiers) (_dedent_, _append_); 
[comments](http://hypertag.io/#comments) (`#` and `--`);
[built-in](http://hypertag.io/#hypertag-built-ins) tags and functions;
raw (r-) vs. formatted (f-) strings; 
_pass_ keyword; concatenation operator; 
[DOM manipulation](http://hypertag.io/#dom-manipulation); and more... 

See the [Language Reference](http://hypertag.io/#language-reference) for details.


## Cheat Sheet

### Text blocks

| &nbsp;<br> Syntax <br><img width=200/> | &nbsp;<br> Description <br>&nbsp; |
| ------------- | --------------- | 
| &#124; _text_   | plain-text block; may contain embedded expressions; output is HTML-escaped |
| / markup        | markup block; may contain embedded expressions; output is *not* HTML-escaped |
| ! _verbatim_    | verbatim block; expressions are *not* parsed; output is *not* HTML-escaped |
| &#124; _multi-line_<br>&nbsp;&nbsp;_text....._ | text blocks may span *multiple lines*, also when preceded by a tag; subsequent lines must be indented |
| -- _comment_ <br> # _comment_ | line of comment; is excluded from output; may occur at the end of a block's headline (_inline comment_) or on a separate line (_block comment_) |
| < BLOCK       | _dedent_ modifier (<): when put on the 1st line of a BLOCK, causes the output to be dedented by one level during rendering; applies to blocks of all types (text, control etc.) |
| ... BLOCK     | _append_ modifier (...): when put on the 1st line of a BLOCK, causes the output to be appended to the previous block without a newline |

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
| $$ {{ }}  | escape strings; render $ or { or } in a plaintext/markup block and inside formatted strings |
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
