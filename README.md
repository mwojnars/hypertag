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
and thus removes the need for explicit closing tags.
Hypertag provides: advanced control of page rendering with
native control blocks, high level of modularity with Python-like imports,
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
    import $blue
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

The `script` in the code above is translated to
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
- **Code reuse** through functions/classes is the corner stone of programming,
  yet it is missing from HTML; this is fixed now with Hypertag:
  programmers can create reusable components in a form of **custom tags** (_hypertags_), 
  defined either as Python functions (_external tags_) 
  or directly in a document using Hypertag syntax (_native tags_);
  hypertags can be parameterized and may represent complex pieces 
  of combined: content, style and layout - for reuse across documents.
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
  Hypertag is *not* limited to (X)HTML; through defining new tags,
  it can be adapted to produce (potentially) any other document description language.


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

There are three types of text blocks: _plain-text_ (|), _markup_ (/) and _verbatim_ (!).
They differ in the way how embedded expressions and HTML special symbols are handled.

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
(inside expressions) they may be forbidden.

### Tags

In a tagged block, text may start on the same line as the tag (_inline_ contents),
and it may extend to subsequent lines (_multiline_ contents) unless sub-blocks are present.
Inline text gets rendered to a consise form: with no surrounding newlines 
between the body and the HTML tags.

    h1 | This is inline text, no surrounding newlines are printed.
    p  | This paragraph is "inline" and "multiline" at the same time,
         it continues on subsequent lines without additional "|" markers.
    div |
      Another example of how a multiline text-only block can be written
      using an initial "|" marker in the headline and no other markers thereafter.

output:

```html
<h1>This is inline text, no surrounding newlines are printed.</h1>
<p>This paragraph is "inline" and "multiline" at the same time,
it continues on subsequent lines without additional "|" markers.</p>
<div>
Another example of how a multiline text-only block can be written
using an initial "|" marker in the headline and no other markers thereafter.
</div>
```

Inline (but not multiline) text can be combined with other sub-blocks if a colon (:)
is placed before the text marker. A special _null_ tag (.) can be used to better align
tagged an untagged blocks:

    div: | This inline text can be follow by nested blocks thanks to ":" marker
      p
        i | This line is in italics ...
        . | ... but this one is not. 
        . | The null tag does nothing, only helps with code alignment when a tag is missing.

output:

```html
<div>This inline text can be follow by nested blocks thanks to ":" marker
  <p>
    <i>This line is in italics ...</i>
    ... but this one is not.
    The null tag does nothing, only helps with code alignment when a tag is missing.
  </p></div>
```

If no inline contents is present, a colon can optionally be put at the end of 
the block's headline. The two forms, with and without a trailing colon, are equivalent.

<!---
and so are the "div" blocks below:

    div:
      p | Some contents...
    
    div
      p | Some contents...
--->

Tags may have _attributes_ and can be _chained_ together, like here:

    a href="http://hypertag.io" style="color:#00f"
        | Attributes are passed to a tag in a space-separated list, no parentheses.
    
    h1 class='big-title' : a href='http://hypertag.io' : b
        | Tags can be chained together using a colon ":".
        | Each tag in a chain can have its own attributes.

output:

```html
<a href="http://hypertag.io" style="color:#00f">
    Attributes are passed to a tag in a space-separated list, no parentheses.
</a>

<h1 class="big-title"><a href="http://hypertag.io"><b>
    Tags can be chained together using a colon ":".
    Each tag in a chain can have its own attributes.
</b></a></h1>
```

Shortcut syntax can be used for the two most common HTML attribute names: 
.CLASS is equivalent to class=CLASS, and #ID means id=ID, for example:

    p #main-contents .wide-paragraph | text...
    
output:

```html
<p id="main-contents" class="wide-paragraph">text...</p>
```

### Expressions

A Hypertag script may define _variables_ to be used subsequently in _expressions_
inside plain-text and markup blocks, or inside attribute lists.
A variable is created by an _assignment block_ ($). 
Expressions are embedded in text blocks using {...}  or $... syntax - the latter can only
be used for expressions that consist of a variable with (optionally) 
some tail operators (. [] ()):

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
standard operators that are available in Python:

    ** * / // %
    + - unary minus
    << >>
    & ^ |
    == != >= <= < > in is "not in" "is not"
    not and or
    X if TEST else Y    - the "else" clause is optional and defaults to "else None"
    .                   - member access
    []                  - indexing
    ()                  - function call

All identifiers (of variables and tags) are case-sensitive.
There are separate namespaces for tags and variables, so you don't need to worry
about possible name collissions between local variables and predefined tags: "i", "a" etc.

Variables can also be imported from other Hypertag scripts and Python modules
using an _import_ block. Objects of any type can be imported in this way, 
including functions and classes:

    from python_module import $x, $y as z, $fun as my_function, $T as MyClass
    from hypertag_script import $name

    | fun() of x is equal: $my_function(x)
    $ obj = MyClass(z)

The HyperHTML runtime understands the same _package.module_ syntax of import paths
as Python. This syntax can be applied to Python and Hypertag files alike.
Hypertag scripts must have the ".hy" extension in order to be recognized.
Note, however, that interpretation of import paths is runtime-specific and other
Runtime subclasses can parse these paths differently.
For example, a custom runtime could provide its own path syntax to enable 
the import of scripts from a DB instead of files, or from remote locations etc.

HyperHTML supports also a special import path "~" (tilde), which denotes 
the _dynamic context_ of script execution: a dictionary of all variables that have
been passed to the rendering method (`HyperHTML.render()`) as extra keyword arguments.
These variables are _only_ accessible in the script after they
are _explicitly_ imported with "from ~ import ..." or "import ..." blocks:

    from ~ import $width
    import $height
    
    | Dimensions imported from the context: $width x $height

This script can be rendered in Python like this:

```python3
html = HyperHTML().render(script, width = 500, height = 1000)
print(html)
```
and the output is:

    Dimensions imported from the context: 500 x 1000


### Custom tags

One of the key features of Hypertag is the support for custom tags (_hypertags_)
that can be defined directly in a Hypertag script using _hypertag definition_ blocks (%):

    % tableRow name price='UNKNOWN'
        tr        
            td | $name
            td | $price

Here, `tableRow` is a custom tag that wraps up plain-text contents of table cells
with appropriate `tr` & `td` tags to produce a listing of products.
As you can see, a hypertag may accept attributes and they can have default values,
just like arguments of Python functions. This hypertag can be used with named (keyword) 
or unnamed attributes, similar to a Python function:

    table
        tableRow 'Porsche'  '200,000'
        tableRow 'Jaguar'   '150,000'
        tableRow 'Maserati' '300,000'
        tableRow 'Cybertruck'

What a clean piece of code it is compared to the always-cluttered HTML? In raw HTML, 
and in many templating languages too, you would need much more typing:

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
In HTML, you'd have to manually go through all the cells and modify 
every single occurrence (HTML is notorious for [code duplication](https://en.wikipedia.org/wiki/Duplicate_code)!),
taking care not to modify `<td>` cells of another column accidentally.

Hypertag provides powerful ways to deduplicate code, so it is enough to modify
the hypertag definition in one place adding `.style-price`, and voilà:

    % tableRow name price='UNKNOWN'
        tr        
            td | $name
            td .style-price | $price

This definition can be moved out to a separate "utility" script,
or stay in the same file where it is used for easy maintenance - 
the programmer can choose whatever location is best in a given case.
In other templating languages, there are not so many choices:
typically the best you can do is separate out duplicated HTML code into a Python function,
introducing code fragmentation along the way and spreading the presentation code over 
different types of files (views vs. models) and languages (HTML vs. Python) - 
a very unclean and confusing approach.

Needless to say, hypertags can refer to other hypertags.
Even more, hypertag definitions can be nested, so that one hypertag is defined 
inside another - the former can only be used locally within the scope 
of the outer definition.

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

One more important element of hypertag syntax is the _body attribute_.
Imagine that in the example above, we wanted to add another column containing
formatted (rich-text) information about a given car model.
Passing it as a regular attribute is not convenient, because we'd have to encode
somehow the entire HTML structure of the description: paragraphs, styles, images.
Instead, we can add a _body attribute_ (@) named "info" to the hypertag definition:

    % tableRow @info name price='UNKNOWN'
        tr
            td | $name
            td | $price
            td
               @ info           # this could be inlined as well:  td @ info

and then apply the hypertag to a non-empty _actual body_ which will be passed 
as a DOM structure through the "info" attribute and will get printed in the right 
place inside the output table with all its rich contents and formatting preserved:

    table
        tableRow 'Porsche' '200,000'
            / If you insist on <s>air conditioning</s>,
            / you can always hit the track and roll down the window at <u>160 mph</u>.
        tableRow 'Jaguar' '150,000'
            img src="jaguar.jpg"
            | Money may not buy happiness, but I'd rather cry in a Jaguar than on a bus.
        tableRow 'Maserati' '300,000'
            img src="maserati.jpg"
            i | no funny quotes for Maserati 🙄 
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
           If you insist on <s>air conditioning</s>,
           you can always hit the track and roll down the window at <u>160 mph</u>.
        </td>
    </tr>
    <tr>
        <td>Jaguar</td>
        <td>150,000</td>
        <td>
           <img src="jaguar.jpg" />
           Money may not buy happiness, but I'd rather cry in a Jaguar than on a bus.
        </td>
    </tr>
    <tr>
        <td>Maserati</td>
        <td>300,000</td>
        <td>
           <img src="maserati.jpg" />
           <i>no funny quotes for Maserati 🙄</i>
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

As you can see, Hypertag is much more concise than raw HTML, and with the help of custom
tags it enables cleaner separation between presentation logic (tags) and textual contents.

<!---
This is something that differentiates hypertags from plain Python functions.
Sometimes it is useful to put comments that will be excluded from the output.
You can do this in Hypertag with either `--` or `#` prefix:

--->

### Control blocks

Last but not least, control blocks of multiple types are available in Hypertag
to help you manipulate input data directly in the document without going back and forth
between Python and the template code. These include:

- **if-elif-else**
- **try-else**
- **for**
- **while**

The semantics of "if", "for", "while" blocks is analogous to what it is in Python:

    ......

The "try" block behaves differently than the corresponding Python statement.

    ......


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
| pass              | the special _pass tag_ generates no output, does *not* accept attributes nor a body |
| . <br> . &#124; _text_ | the special _null tag_ (.) outputs its body without changes; helps improve vertical alignment of text in adjecent blocks; does *not* accept attributes |
<!---
| TAG x=1.0 y={v+1} | named (keyword) attributes of a tag occurrence; space-separated, no parentheses |
| TAG "yes" 3 True  | unnamed attributes of a tag occurrence; values are matched to formal attributes in a way similar to how Python matches function arguments (by order) |
--->


## Acknowledgements

Hypertag was inspired by indentation-based templating languages, including:
[Slim](http://slim-lang.com/), [Plim](https://plim.readthedocs.io/en/latest/index.html),
[Shpaml](http://shpaml.com/), [Haml](https://haml.info/).
