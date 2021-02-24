## Introduction

Hypertag is a modern language for front-end development that allows
writing (X)HTML documents in a way similar to writing Python scripts,
where _indentation_ determines relations between nested elements 
and thus removes the need for explicit closing tags.
Hypertag provides: advanced control of page rendering with
native control blocks, high level of modularity with Python-like imports,
unprecedented support for code reuse thanks to native custom tags (_hypertags_),
and much more...

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

The `script` in the code above will be translated to
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
  constituting a core part of the language syntax, unlike in templating languages, 
  where control structures are artificially overlaid on another language (HTML).
- **Modularity** in Hypertag is modeled after Python's: 
  every script may import tags and variables from other scripts,
  from Python modules, and from the dynamic _context_ of script rendering;
  scripts and modules are arranged into packages;
  with these mechanisms in place, building libraries of reusable components is easy and fun.


## Examples

(TODO)

## Cheat Sheet

### Text blocks

| &nbsp;<br> Symbol <br><img width=200/> | &nbsp;<br> Description <br>&nbsp; |
| ------------- | --------------- | 
| &#124; _text_   | plain-text block; may contain embedded expressions; output is HTML-escaped |
| / markup        | markup block; may contain embedded expressions; output is *not* HTML-escaped |
| ! _verbatim_    | verbatim block; expressions are *not* parsed; output is *not* HTML-escaped |
| &#124; _multi-line_<br>&nbsp;&nbsp;_text....._ | text blocks may span *multiple lines*, also when preceded by a tag; subsequent lines must be indented |
| -- _comment_ <br> # _comment_ | line of comment; is excluded from output; may occur at the end of a block's headline (_inline comment_) or on a separate line (_block comment_) |
| < BLOCK       | _dedent marker_ (<): when put on the 1st line of a BLOCK, it causes the output to be dedented by one level during rendering; applies to blocks of all types (text, control etc.) |

### Expressions

| &nbsp;<br> Symbol <br><img width=150/> | &nbsp;<br> Description <br>&nbsp; |
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

| &nbsp;<br> Symbol <br><img width=600/> | &nbsp;<br> Description <br>&nbsp; |
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
| pass              | special _pass tag_ generates no output, does *not* accept attributes nor a body |
| . <br> . &#124; _text_ | special _null tag_ (.) outputs its body without changes; helps improve vertical alignment of text in adjecent blocks; does *not* accept attributes |
<!---
| TAG x=1.0 y={v+1} | named (keyword) attributes of a tag occurrence; space-separated, no parentheses |
| TAG "yes" 3 True  | unnamed attributes of a tag occurrence; values are matched to formal attributes in a way similar to how Python matches function arguments (by order) |
--->


## Acknowledgements

Hypertag was inspired by a number of indentation-based templating languages, including:
[Slim](http://slim-lang.com/), [Plim](https://plim.readthedocs.io/en/latest/index.html),
[Shpaml](http://shpaml.com/), [Haml](https://haml.info/).
