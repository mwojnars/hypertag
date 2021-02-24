## Introduction

Hypertag is a modern language for front-end development that allows
writing (X)HTML documents in a way similar to writing Python scripts,
where _indentation_ determines relations between nested elements 
and thus removes the need for explicit closing tags.
Hypertag provides: advanced control of page rendering with
native control blocks, high level of modularity with Python-like imports,
and unprecedented support for code reuse thanks to native custom tags (_hypertags_).

**NOTE:** Hypertag is currently in Alpha phase. The documentation is under development.

### Usage

Install: _git clone_

Run in Python 3:
```python3
from hypertag import HyperHTML

script = \
"""
    import $title_color
    html: body:
        h1 style="color: $title_color"
            / Example document with a <u>list of items</u>
        ul
            li | item <1>
            li | item #{1+1}
        p : a href='http://hypertag.io' | See the Hypertag site for more!
"""

html = HyperHTML().render(script, title_color = '#00f')
print(html)
```

The above code outputs
(see a [preview](http://htmlpreview.github.io/?https://github.com/mwojnars/hypertag/blob/main/test/sample_usage.html)):

```html
<html><body>
    <h1 style="color: #00f">
        Example document with a <u>list of items</u>
    </h1>
    <ul>
        <li>item &lt;1&gt;</li>
        <li>item #2</li>
    </ul>
    <p><a href="http://hypertag.io">See the Hypertag site for more!</a></p>
</body></html>
```


## Examples

.....

## Acknowledgements

Hypertag was inspired by [Python](https://www.python.org/) and
a number of indentation-based templating languages:
[Slim](http://slim-lang.com/), [Plim](https://plim.readthedocs.io/en/latest/index.html),
[Shpaml](http://shpaml.com/), [Haml](https://haml.info/).
