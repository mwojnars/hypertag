## Introduction

Hypertag is a modern language for front-end development that allows
writing (X)HTML documents in a way similar to writing Python scripts,
where _indentation_ determines relations between nested elements 
and thus removes the need for explicit closing tags.
Hypertag provides advanced control of page rendering with
native control blocks, high level of modularity with Python-like imports,
and unprecedented support for code reuse thanks to native custom tags (_hypertags_).

**NOTE:** Hypertag implementation is currently in Alpha phase. 
The documentation is under development.

### Usage

Install: _git clone_

Run in Python 3:

    from hypertag import HyperHTML
    
    script = \
    """
        import $title_color
        html: body:
            h1 style="color: $title_color"
                / Example document with a <b>list of items</b>
            ul
                li | item <1>
                li | item #{1+1}
    """
    
    html = HyperHTML().render(script, title_color = '#00f')
    print(html)

The above code will output:

    <html><body>
        <h1 style="color: #00f">
            Example document with a <b>list of items</b>
        </h1>
        <ul>
            <li>item &lt;1&gt;</li>
            <li>item #2</li>
        </ul>
    </body></html>



## Examples

.....

## Acknowledgements

Hypertag was inspired by [Python](https://www.python.org/) and
a number of indentation-based templating languages:
[Slim](http://slim-lang.com/), [Plim](https://plim.readthedocs.io/en/latest/index.html),
[Shpaml](http://shpaml.com/), [Haml](https://haml.info/).
