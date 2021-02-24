# run:  python3 -m hypertag.test.sample_usage > hypertag/test/sample_usage.html
#

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
