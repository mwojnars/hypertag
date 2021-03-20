# run:  python3 -m hypertag.test.sample_usage > hypertag/test/sample_usage.html
#

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
