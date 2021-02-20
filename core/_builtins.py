import re
from hypertag.core.DOM import Sequence, get_indent, del_indent
from hypertag.core.tag import ExternalTag


########################################################################################################################################################
#####
#####  BUILT-IN functional hypertags
#####

"""
TODO
- dedent full=False   -- remove leading indentation of a block, either at the top level only (full=False), or at all nested levels (full=True)
- unique strip=True   -- render body to text and remove duplicate lines (or blocks?)
- unique_lines
- unique_blocks
- inline merge=True   -- convert block to "inline" (no margin, no indent); merge newlines and spaces to a single space if merge=True
- css                 -- marks its content as a CSS script that shall be moved to a <style> section of the document
- js                  -- JavaScript code to be put into a <script> section
- error               -- inserts a standard error message in a place of occurrence; root document node might collect all <error> nodes and produce a combined (hidden) error message
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
        

