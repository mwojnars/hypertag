from hypertag import HyperHTML

script = \
"""
    import $title_color
    html: body:
        h1 style="font-color: $title_color"
            / Example document with a <b>list of items</b>
        ul
            li | item <1>
            li | item <2>
"""

html = HyperHTML().render(script, title_color = '#ff0000')
print(html)
