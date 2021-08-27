import re, itertools
from hypertag.nifty.util import unique as unique_list, merge_spaces
from hypertag.core.dom import del_indent
from hypertag.std.registry import Registry


register = Registry()


########################################################################################################################################################
#####
#####  GENERAL PURPOSE tags
#####

_re_dedent = re.compile(r'(?m)^\s+')
_re_merge  = re.compile(r'\s+')


@register.tag
@register.var
def doctype(text, value = 'html'):
    return f"<!DOCTYPE {value}>"

@register.tag
@register.var
def dedent(text, full = True):
    """
    Remove all line indentation in `text` (if full=True); or the longest common indentation shared by all
    lines with at least one non-whitespace character.
    The indentation may differ between lines and it still gets fully removed.
    """
    # return _re_dedent.sub('', text)
    if full: return _re_dedent.sub('', text)
    else:    return del_indent(text)

@register.tag
@register.var
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

@register.tag
@register.var
def merge(text):
    """
    Strip leading/trailing whitespace in `text`, replace newlines and tabs with spaces, merge multiple adjacent spaces.
    Similar to normalize-space() in XPath.
    """
    return _re_merge.sub(' ', text).strip()

@register.tag
@register.var
def inline(text):
    """
    Convert all newline characters to HTML entities: &#10;
    This can be used to prevent Hypertag from indenting lines of `text` when rendering parent nodes,
    and to safely insert `text` inside <pre>, <textarea>, or similar elements.
    """
    return text.replace('\n', '&#10;')

@register.tag
@register.var
def lower(text):
    """A tag/function/filter that converts `text` to lowercase. Inner tag names and attributes are converted, too (!)."""
    return text.lower()

@register.tag
@register.var
def upper(text):
    """A tag/function/filter that converts `text` to uppercase. Inner tag names and attributes are converted, too (!)."""
    return text.upper()

@register.var
def cycle(*sequences, **params):   #stop = 'first'
    """
    A generator that cycles through each of the provided iterables IN PARALLEL and yields tuples containing
    one element from each iterable - like zip(), but the cycling runs indefinitely (if stop=False), or until
    the FIRST iterable gets exhausted (if stop='first', default), or until the LONGEST iterable gets exhausted
    (stop='longest'). When an iterable is exhausted along the way, its sequence of elements is repeated.
    This function is inspired by Django's {%cycle%} tag, yet it differs from this tag in that it doesn't require
    maintaining a hidden state, which enhances code readability.
    This function can be used, for instance, to alternate colors of rows in a table.
    """
    stop = params.pop('stop', 'first')
    if params: raise Exception('unrecognized keyword argument "%s" in cycle()' % list(params.keys())[0])
    
    if not sequences: return []
    length = None
    
    if stop == 'first':
        sequences = list(sequences)
        sequences[0] = list(sequences[0])               # convert the 1st iterable to a list, so that we can check its length
        length = len(sequences[0])                      # length of the output sequence
        
    elif stop == 'longest':
        sequences = list(map(list, sequences))          # convert each sequence to a list, so that we can check their lengths
        length = max(map(len, sequences))               # ...and find the longest one
    
    cycles = map(itertools.cycle, sequences)            # create indefinite-loop iterators over each iterable
    
    return itertools.islice(zip(*cycles), length)

@register.var
def changes(seq, first = True):
    """
    Iterates over a given sequence and yields pairs (value, change), where `value` is the next element of `seq`,
    and `change` is True if the value differs from the previous one, False otherwise.
    In the first tuple, `change` equals `first` (True by default).
    This generator can be used in loops as a replacement for Django's {%ifchanged%} tag.
    """
    prev = None
    for i, value in enumerate(seq):
        if i == 0:
            yield value, first
        else:
            yield value, (value != prev)
        prev = value

@register.var
def crop(s, length = 255, end = '...', killwords = False, maxdrop = 10, leeway = 0):
    """
    If `killwords` is false, the last word will be discarder, unless the resulting string
    gets shorter than `maxdrop` characters only due to word preservation,
    otherwise the word gets split (rather than discarded) anyway.
    """

    # the implementation below was inspired by Jinja's truncate(): https://github.com/pallets/jinja/blob/main/src/jinja2/filters.py
    assert isinstance(s, str), f"expected a string, got {type(s)}"
    assert length >= len(end), f"expected length >= {len(end)}, got {length}"
    assert leeway >= 0, f"expected leeway >= 0, got {leeway}"

    if len(s) <= length + leeway:
        return s
    
    maxlen = length - len(end)          # maximum string length before appending the `end`
    
    if killwords:
        return s[:maxlen] + end

    result = s[:maxlen].rsplit(" ", 1)[0]
    if len(result) < maxlen - maxdrop:
        result = s[:maxlen]
        
    return result + end
    
truncate = crop
register.var('truncate', truncate)          # truncate() is an alias for crop(), for similarity with Jinja/Django


########################################################################################################################################################

"""
Terminal tags:
- resource            -- terminal tag that marks a given block as a resource that shall be moved to HTML's <meta> section
- error               -- inserts a standard error message in a place of occurrence; root document node might collect all <error> nodes and produce a combined (hidden) error message

Functions inspired by Django/Ninja:
- findchange(seq)            -- similar to enumerate() but outputs a binary flag whenever a value of the sequence changes relative to the previous one;
                                replacement for Django's {%ifchanged%}
  finddiff() changes()
  
- url ??

Filters:
- groupby(key, d=None)       -- when applied to a list of dicts, returns a list of groups of records having the same value of `key`;
                                each group is a list of records; `key` can be a tuple of key names, names can refer to related objects "x.y.z";
                                replacement for Django's {%regroup%}
"""

