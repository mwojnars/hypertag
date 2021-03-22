## Introduction

If you are new to Hypertag, see the 
**[Quick Start](https://github.com/mwojnars/hypertag#quick-start)** for a brief introduction,
or the complete **[Language Reference](http://hypertag.io/#language-reference)** for details.

Hypertag is a modern language for front-end development that allows
writing HTML5 and other markup documents in a way similar to writing Python scripts,
where [indentation](http://hypertag.io/#layout) determines relationships between nested elements 
and removes the need for explicit closing tags. Hypertag provides:

- Advanced control of rendering process with native [control blocks](http://hypertag.io/#control-blocks) 
  (_if_, _for_, _while_, _try_).
- High level of modularity thanks to Python-like [imports](http://hypertag.io/#imports).
- Unprecedented support for code reuse with native [custom tags](http://hypertag.io/#custom-tags).
- Native [DOM](http://hypertag.io/#dom) representation and [DOM manipulation](http://hypertag.io/#dom-manipulation) during rendering.
- Embedded [expressions](http://hypertag.io/#expressions) of any complexity.
- Standard Python [operators](http://hypertag.io/#operators) to manipulate arbitrary Python objects.
- Custom [pipeline](http://hypertag.io/#filters) operator (`:`) for chaining multiple functions as [filters](http://hypertag.io/#filters).
- Expression [qualifiers](http://hypertag.io/#qualifiers) (`!?`) for creation of alternative paths of calculation and easy handling of edge cases.
- Built-in tags for [HTML5](http://hypertag.io/#html-specific-symbols) generation and for [general](http://hypertag.io/#hypertag-built-ins) purposes.
- Integrated [Python built-ins](http://hypertag.io/#python-built-ins).
- Integrated [Django filters](http://hypertag.io/#django-filters).
  

### Setup

Install:
```
pip install hypertag-lang               # watch out the name, it is "hypertag-lang"
```

Usage:
```python
from hypertag import HyperHTML
html = HyperHTML().render(script)       # rendering of a Hypertag `script` to HTML
```

## Why to use Hypertag

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
  

## Acknowledgements

Hypertag was inspired by [Python's](https://www.python.org/) syntax
and by indentation-based templating languages:
[Slim](http://slim-lang.com/), [Plim](https://plim.readthedocs.io/en/latest/index.html),
[Shpaml](http://shpaml.com/), [Haml](https://haml.info/).

