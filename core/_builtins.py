import re
from hypertag.core.DOM import Sequence, get_indent, del_indent
from hypertag.core.tag import ExternalTag


########################################################################################################################################################
#####
#####  BUILT-IN functional hypertags
#####

"""
TODO
- dedent full=True    -- remove leading indentation of a block, either at the top level only (full=False), or at all nested levels (full=True)
- unique strip=True   -- render body to text and remove duplicate lines (or blocks?)
- unique_lines
- unique_blocks
- inline merge=True   -- convert block to "inline" (no margin, no indent); merge newlines and spaces to a single space if merge=True
- css                 -- marks its content as a CSS script that shall be moved to a <style> section of the document
- js                  -- JavaScript code to be put into a <script> section
- error               -- inserts a standard error message in a place of occurrence; root document node might collect all <error> nodes and produce a combined (hidden) error message

Tags inspired by Django/Ninja:
- lower, upper        -- convert rendered body to all lower/upper case; will convert tag names and attrs too if applied to an html-tagged block
-

Functions inspired by Django/Ninja:
- alternate(seq1, seq2, ...) -- like zip() but cycles over each sequence until the *longest* one is exhausted;
                                can be used to alternate colors of rows in a table; replacement for Django's {%cycle%} tag
- findchange(seq)            -- similar to enumerate() but outputs a binary flag whenever a value of the sequence changes relative to the previous one;
                                replacement for Django's {%ifchanged%}
- now(fmt)                   -- current date & time string; equivalent to Django's {%now%}
- url ??

Filters:
- groupby(key, d=None)       -- when applied to a list of dicts, returns a list of groups of records having the same value of `key`;
                                each group is a list of records; `key` can be a tuple of key names, names can refer to related objects "x.y.z";
                                replacement for Django's {%regroup%}
- date ??                    -- allows for more advanced formatting than Python's datetime; Django's implementation could be reused here?
- default(val)
- default_if_none(val)
- dictsort(key, reversed=False)  -- takes a list of dictionaries and returns that list sorted by the key
  dictsortreversed(key)
- divisibleby(divisor)
- filesizeformat                 -- take from Django?
- first
- lower, upper

"""

class DedentTag(ExternalTag):
    text = True
    def expand(self, text, nested = True, _re_indent = re.compile(r'(?m)^\s+')):
        if nested: return _re_indent.sub('', text)
        return del_indent(text, get_indent(text))
        
class JavascriptTag(ExternalTag):
    """Typically, a `javascript` tag should be used with verbatim (!...) contents inside."""
    text = True

    _block = del_indent("""
        <script type="text/javascript">
        <!--
        %s
        -->
        </script>
    """.strip())
    
    def expand(self, js_code):
        return self._block % js_code
        

def _unique():
    pass

BUILTIN_TAGS = {
    'dedent':       DedentTag,
    'javascript':   JavascriptTag,
}

# instantiate tag classes
for name, tag in BUILTIN_TAGS.items():
    if isinstance(tag, type):
        BUILTIN_TAGS[name] = tag()
        

