import re
from nifty.util import unique as unique_list
from hypertag.std.registry import Registry


register = Registry()


########################################################################################################################################################
#####
#####  GENERAL PURPOSE tags
#####

_re_dedent = re.compile(r'(?m)^\s+')

@register.tag
def dedent(text):
    """Remove all line indentation in `text`. The indentation may differ between lines and it still gets fully removed."""
    return _re_dedent.sub('', text)
    # if full: return _re_indent.sub('', text)
    # return del_indent(text)

@register.tag
def unique(text, strip = True):
    """
    Remove duplicate lines in `text`. The order of remaining lines is preserved.
    If strip=True (default), the lines are stripped of leading & trailing whitespace before comparison,
    and all empty lines are removed.
    """
    lines = text.splitlines()
    if strip: lines = list(filter(None, map(str.strip, lines)))
    uniq = unique_list(lines)
    return '\n'.join(uniq)



########################################################################################################################################################

"""
TODO
- unique_blocks
- inline merge=True   -- convert block to "inline" (no margin, no indent); merge newlines and spaces to a single space if merge=True
- resource            -- terminal tag that marks a given block as a resource that shall be moved to HTML's <meta> section
- error               -- inserts a standard error message in a place of occurrence; root document node might collect all <error> nodes and produce a combined (hidden) error message
? lower, upper        -- convert rendered body to all lower/upper case; will convert tag names and attrs too if applied to an html-tagged block

Functions inspired by Django/Ninja:
- alternate(seq1, seq2, ...) -- like zip() but cycles over each sequence until the *longest* one is exhausted;
                                can be used to alternate colors of rows in a table; replacement for Django's {%cycle%} tag
- findchange(seq)            -- similar to enumerate() but outputs a binary flag whenever a value of the sequence changes relative to the previous one;
                                replacement for Django's {%ifchanged%}
- url ??

Filters:
- groupby(key, d=None)       -- when applied to a list of dicts, returns a list of groups of records having the same value of `key`;
                                each group is a list of records; `key` can be a tuple of key names, names can refer to related objects "x.y.z";
                                replacement for Django's {%regroup%}
"""

