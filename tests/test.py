"""
Run:
$
$  pytest -vW ignore::DeprecationWarning hypertag/tests/test.py
$

"""

# import unittest
import os, re, pytest

from hypertag import HyperHTML


#####################################################################################################################################################
#####
#####  UTILITIES
#####

def render(script, **ctx):
    return HyperHTML(**ctx).render(script)

def merge_spaces(s, pat = re.compile(r'\s+')):
    """Merge multiple spaces, replace newlines and tabs with spaces, strip leading/trailing space."""
    return pat.sub(' ', s).strip()


#####################################################################################################################################################
#####
#####  TESTS
#####

def test_001_basic():
    src = """"""
    assert render(src) == ""
    src = """      """
    assert render(src) == ""
    src = """ |Ala    """
    assert render(src) == " Ala"                # trailing spaces in lines are removed
    src = """\n|Ala\n"""
    assert render(src) == "\nAla\n"             # leading/trailing newlines of a document are preserved
    src = """\n\n\t|Ala\n\n"""
    assert render(src) == "\n\n\tAla\n\n"
    src = """\n\n \t | Ala\n\n"""
    assert render(src) == "\n\n \t Ala\n\n"

    src = """| $$ {{ }} {'.'}"""                # escape sequences
    assert render(src) == "$ { } ."

def test_002_qualifiers():
    # the code below contains NESTED qualifiers: unsatisfied ! within ?
    src = """ | kot { 'Mru' "czek" 123 0! }? {456}! {0}? """
    out = """   kot  456   """
    assert render(src).strip() == out.strip()

    src = """ | kot { 'Mru' "czek" 123 0? }! {456}? {0}? """
    out = """   kot Mruczek123 456   """
    assert render(src).strip() == out.strip()

    with pytest.raises(Exception, match = 'Obligatory expression') as ex_info:
        render("| {0}!")
    
    # assert str(ex_info.value) == 'some info'
    
def test_003_empty_blocks():
    src = """
        p
        p:
        p |
        div /
        form !
        |
        /
        !
        B: |
    """
    out = """
        <p></p>
        <p></p>
        <p></p>
        <div></div>
        <form></form>



        <B></B>
    """
    assert render(src).strip() == out.strip()

def test_004_layout():
    src = """
        h1
            p : b | Ala
            p
                |     Ola
                    i kot
    """
    out = """
        <h1>
            <p><b>Ala</b></p>
            <p>
                    Ola
                  i kot
            </p>
        </h1>
    """
    assert render(src).strip() == out.strip()
    src = """
        div
        

        p
        
            i
    """
    out = """

        <div></div>


        <p>

            <i></i>
        </p>
    """
    assert render(src).strip() == out.strip()
    
    src = """
        p
            <p: | Ala
                | kot
            b | i pies
            < if True:
                / clause of
                | dedented "if"
            if True:
                < p | dedented clause in indented "if"
    """                             # clear indentation (dedent) marker, dedented blocks
    out = """
        <p>
        <p>Ala
            kot</p>
            <b>i pies</b>
        clause of
        dedented "if"
            <p>dedented clause in indented "if"</p>
        </p>
    """
    assert render(src).strip() == out.strip()
    src = """
        DIV
            < try | {True}!
            < try | {False}!
            <? | {True}!
            <? | {False}!
    """
    out = """
        <DIV>
        True
        True
        </DIV>
    """
    assert render(src).strip() == out.strip()
    src = """
        | Ala ma
        ...| kota
    """
    assert render(src).strip() == "Ala makota"
    src = """
        | Ala ma
        ...|  kota
    """
    assert render(src).strip() == "Ala ma kota"
    src = """
        p
            i  | line1
            ...| line2
        ... |line3
    """
    out = """
        <p>
            <i>line1</i>line2
        </p>line3
    """
    assert render(src).strip() == out.strip()
    src = """
        i  | line1
        ...| line2
        ... b | line3
    """
    out = """
        <i>line1</i>line2<b>line3</b>
    """
    assert render(src).strip() == out.strip()
    src = """
        %H x | $x
        | (
        ... H 1
        ... | ,
        ... H 2
        ... | )
    """
    assert render(src).strip() == "(1,2)"
    src = """
        p
            i  | line1
            ...|  + a multiline block
                 is appended
                 with indentation preserved
    """
    out = """
        <p>
            <i>line1</i> + a multiline block
            is appended
            with indentation preserved
        </p>
    """
    assert render(src).strip() == out.strip()
    src = """
        p
            ... | a block with no predecessors
            ... /  can be inlined into its parent
    """
    out = """
        <p>a block with no predecessors can be inlined into its parent</p>
    """
    assert render(src).strip() == out.strip()

def test_005_doc_margins():
    src = """\n\n p | text  \n  \n  """
    out = """\n\n <p>text</p>\n\n"""
    assert out == render(src)           # no .strip()

def test_006_if():
    # src = """
    #     if {False}:
    #         |Ala
    #     elif True * 5:
    #         div | Ola
    # """                     # ^ here, {False} is interpreted as an embedded expression {...} that evaluates to False
    # assert render(src).strip() == "<div>Ola</div>"
    src = """
        if (False):
            |Ala
        elif True * 5:
            div | Ola
    """                     # ^ embeddings, like {False}, are no longer allowed in "if" and "for"; should be replaced with (..)
    assert render(src).strip() == "<div>Ola</div>"
    src = """
        if {} | Ala
        elif 5 | Ola
    """                     # ^ here, {} is interpreted as an empty set() not an embedded expression {...} - the latter can't be empty
    assert render(src).strip() == "Ola"
    src = """
        if {} | Ala
        else / Ola
    """
    assert render(src).strip() == "Ola"
    src = """
        $test = False
        if test ! Ala
        elif (not test) / Ola
    """
    assert render(src).strip() == "Ola"
    src = """
        if True | true
    """
    assert render(src).strip() == "true"

def test_007_variables():
    src = """
        if True:
            $ x = 5
        else:
            $ x = 10
        | {x}
    """
    assert render(src).strip() == "5"
    src = """
        $ x = 1
        p:
            $ x = 2
            | {x}
            # the line above outputs "2"
        | {x}
        # the line above outputs "1"
    """
    assert merge_spaces(render(src)) == "<p> 2 </p> 1"
    src = """
        if False:
            $ x = 5
        else:
            $ x = 10
        | {x}
    """
    assert render(src).strip() == "10"

    src = """
        $ y = 0
        div : p
            $ y = 5
            | {y}
    """
    assert merge_spaces(render(src)) == "<div><p> 5 </p></div>"

    src = """
        $x = 0
        if False:
            $x = 1
        elif x > 0:
            $x = 2
        | $x
    """
    assert render(src).strip() == "0"
    src = """
        $ a, (b, c) = 1, (2, 3)
        | $a, $b, $c
    """
    assert render(src).strip() == "1, 2, 3"


def test_008_variables_err():
    with pytest.raises(Exception, match = 'referenced before assignment') as ex_info:
        render("""
            if False:
                $ x = 5
            else:
                $ y = 10
            | {x}
        """)
    with pytest.raises(Exception, match = 'not defined') as ex_info:
        render("""
            p
                $ y = 5
            | {y}
        """)
    
def test_009_collections():
    src = "| { () }"            # empty tuple
    assert merge_spaces(render(src)) == "()"
    src = "| { (1 , ) }"
    assert merge_spaces(render(src)) == "(1,)"
    src = "| { (1,2, 3) }"
    assert merge_spaces(render(src)) == "(1, 2, 3)"

    src = "| { [] }"
    assert merge_spaces(render(src)) == "[]"
    src = "| { [1 , ] }"
    assert merge_spaces(render(src)) == "[1]"
    src = "| { [1,2, 3] }"
    assert merge_spaces(render(src)) == "[1, 2, 3]"
    src = "| { [ 1 ,[2], (), (3,)] }"
    assert merge_spaces(render(src)) == "[1, [2], (), (3,)]"

    src = "| {{'set'}}"
    assert merge_spaces(render(src)) == "{'set'}"
    src = "| { { 'set' , } }"
    assert merge_spaces(render(src)) == "{'set'}"
    src = "| { {1, 1 ,1} }"
    assert merge_spaces(render(src)) == "{1}"

    src = "| { {} }"
    assert merge_spaces(render(src)) == "{}"
    src = "| { { } }"
    assert merge_spaces(render(src)) == "{}"
    src = "| { {1:1, 2 : 2 , 3 :3,3:4,} }"
    assert merge_spaces(render(src)) == "{1: 1, 2: 2, 3: 4}"
    src = "| {{ }}"
    assert merge_spaces(render(src)) == "{ }"           # this is NOT a dict! sequences {{ and }} represent { and } characters escaped

    src = "| { 'ala'[1:2:1] }"
    assert merge_spaces(render(src)) == "l"
    src = "| { 'Ala'[3:0:-1] }"
    assert merge_spaces(render(src)) == "al"
    src = "| { 'Ala'[1+2 : 0*0 : -1+5*0] }"
    assert merge_spaces(render(src)) == "al"
    src = "| { {1+2:3-4, -5 : 6*7*0} }"
    assert merge_spaces(render(src)) == "{3: -1, -5: 0}"
    

def test_010_for():
    src = """
        $x = 1
        for i in [1,2,3]:
            $x += 1
        | $x
    """
    assert render(src).strip() == "4"
    src = """
        for i in [1,2,3]:
            p | $i
            | {i+10}
    """
    out = """
        <p>1</p>
        11
        <p>2</p>
        12
        <p>3</p>
        13
    """
    assert render(src).strip() == out.strip()
    src = """
        / pre

        for i in []:
            | $i

        ! post
    """                         # 1-line margin that preceeds the <for> block is preserved even despite the block renders empty
    out = """
        pre


        post
    """
    assert render(src).strip() == out.strip()
    src = """
        for i in [1,2]:
            p:
                $i = i + 5
                | $i in
            | $i out
    """
    out = """
        <p>
            6 in
        </p>
        1 out
        <p>
            7 in
        </p>
        2 out
    """
    assert render(src).strip() == out.strip()
    src = """
        for i in [1,2,3] | $i
    """
    assert render(src).strip() == "123"
    src = """
        for i in [1,2,3] |   $i
    """
    assert render(src).strip() == "1  2  3"

def test_011_calls():
    src = """
        for i in range(3):
            | $i
    """
    out = """
        0
        1
        2
    """
    assert render(src).strip() == out.strip()
    src = """
        for i in range( 1 , 7 , 2 ,):
            | $i
    """
    out = """
        1
        3
        5
    """
    assert render(src).strip() == out.strip()
    src = """
        for pair in enumerate(range(3), start = 10):
            | $pair
    """
    out = """
        (10, 0)
        (11, 1)
        (12, 2)
    """
    assert render(src).strip() == out.strip()
    src = """
        for i, val in enumerate(range(3), start = 10):
            | $val at $i
    """
    out = """
        0 at 10
        1 at 11
        2 at 12
    """
    assert render(src).strip() == out.strip()
    src = """
        $k = 5
        for i, val in enumerate(range(k-2), start = k*2):
            $ i = i + 1
            | $val at $i
        | $i
    """
    out = """
        0 at 11
        1 at 12
        2 at 13
        13
    """
    assert render(src).strip() == out.strip()

    src = "| { {'a':'b'}.get('c', 123) }"
    assert merge_spaces(render(src)) == "123"
    src = "| { { 'a' : 'b' } . get ('c', 123) ' ' 'aaa' }"
    assert merge_spaces(render(src)) == "123 aaa"

def test_012_hypertags():
    src = """
        %H a b c:
            p | $a $b $c
        H 1 c=3 b=2
    """
    assert render(src).strip() == "<p>1 2 3</p>"
    src = """
        %H a b c
            p | $a $b $c
        H 1 c=3 b=2
    """
    assert render(src).strip() == "<p>1 2 3</p>"
    src = """
        %H a b=4 c='5':
            p | $a $b $c
        H 1 b=2
    """
    assert render(src).strip() == "<p>1 2 5</p>"
    src = """
        %H a b=4 c='5' | $a $b  $c
        H 1 b=2
    """
    assert render(src).strip() == "1 2  5"
    src = """
        %H  a  b = 4 c  ='5'|$a$b$c
        H 1 b=2
    """
    assert render(src).strip() == "125"
    src = """
        $b = 10
        %H a b=4 c={b+5} | $a $b $c
        H 1 b={b*2}
    """
    assert render(src).strip() == "1 20 15"

    src = """
        %H x | headline
           text {x} text
              indented line
              
            last line
        H True
    """
    out = """
        headline
        text True text
           indented line

         last line
    """
    assert render(src).strip() == out.strip()
    src = """
        %H @body a=0
            | $a
            @ body
        p
            H 5
                i | kot
    """
    out = """
        <p>
            5
            <i>kot</i>
        </p>
    """
    assert render(src).strip() == out.strip()
    src = """
        %H | xxx
        p
            %H @body a=0
                | $a
            H 5
    """
    out = """
        <p>
            5
        </p>
    """
    assert render(src).strip() == out.strip()
    src = """
        %H | xxx
        %H @body a=0
            | $a
        H 5
    """
    assert render(src).strip() == "5"
    src = """
        %H @body a=0 | $a
        p : H 5
    """
    assert render(src).strip() == "<p>5</p>"
    src = """
        %H @body a=0 @ body
        p : H 5 | kot
    """
    assert render(src).strip() == "<p>kot</p>"

    src = """
        $g = 100
        %G x | xxx {x+g}
        %H @body a=0
            | ala
            @ body
            $g = 200
            %F x y={a*2}
                G {x+y+a+g}
                | inside F
            F 10
        H 5
            | pies
    """
    out = """
        ala
        pies
        xxx 325
        inside F
    """
    assert render(src).strip() == out.strip()
    src = """
        $g = 100
        %g x | xxx {x+g}
        %H @body a=0
            $g = 200
            g {a+g}
        H 5
    """                     # ^ same name ("g") for a hypertag and a variable works fine (separate namespaces for vars and tags)
    out = """
        xxx 305
    """
    assert render(src).strip() == out.strip()
    src = """
        %H @body
            @body[0]
        H
            | first
            | second
    """
    assert render(src).strip() == "first"
    src = """
        %G @body
            @body[0]
            | in G
        %H @body
            G @ body[-1]
        H
            | first
            | last
    """
    out = """
        last
        in G
    """
    assert render(src).strip() == out.strip()
    src = """
        $x = 1
        %H
            | $x
        $x = 2
        H
        $x = 3
        H
    """                     # if a variable is re-assigned in the same block (naming scope), hypertags use the most recent value at the point of expansion
    out = """
        2
        3
    """
    assert render(src).strip() == out.strip()

def test_013_hypertags_err():
    with pytest.raises(Exception, match = 'undefined tag') as ex_info:
        render("""
            p
                %H @body a=0
                    | $a
                    @ body
            H 1
        """)
    
def test_014_none_embedded():
    with pytest.raises(Exception, match = 'embedded in markup text evaluates to None') as ex_info:
        render(""" | {None} """)
    with pytest.raises(Exception, match = 'string-concatenated evaluates to None') as ex_info:
        render(""" | {None None} """)
    
    src = """ | {'a' None? 'b' None? 'c'} """
    assert render(src).strip() == "abc"

def test_015_try():
    src = """ ? | {None} """
    assert render(src) == ""
    src = """
        $ x = ''
        | x $x
        ? | x $x!
    """
    assert render(src).strip() == "x"
    src = """
        $ x = False
        try | x $x!
    """
    assert render(src).strip() == ""
    src = """
        $ x = 0
        try | x $x!
        else| x*2 = {x*2}!
        else| x+1 = {x+1}!
        else! error
    """
    assert render(src).strip() == "x+1 = 1"
    src = """
        $ x = 0
        try
            p | x $x!
        else
            p | x+1 = {x+1}!
    """
    assert render(src).strip() == "<p>x+1 = 1</p>"
    src = """
        $ x = 0
        try :
            p | x $x!
        else
            p | x+1 = {x+1}!
    """
    assert render(src).strip() == "<p>x+1 = 1</p>"
    src = """
        $ x = 0
        try | x $x!
        else:
            try  / x*2 = {x*2}!
            else / x+1 = {x+1}!
    """
    assert render(src).strip() == "x+1 = 1"
    src = """
        $ x = False
        ?
            | x $x!
    """
    assert render(src).strip() == ""

def test_016_special_tags():
    src = """
        div
            p   | title
            .   | contents
                  more lines...
            .
                a | link
                . | xxxxx
    """
    out = """
        <div>
            <p>title</p>
            contents
            more lines...

                <a>link</a>
                xxxxx
        </div>
    """
    assert render(src).strip() == out.strip()
    src = """
        | pre
        for i in range(3)
            .
        | post
    """                         # dot tag (.) always creates a node and renders something; it does NOT mean "pass" (no operation)
    out = """
        pre



        post
    """
    assert render(src).strip() == out.strip()
    src = """
        | pre
        pass
        pass
        for i in [1,2]
            pass
        | post
    """                         # "pass" means "no operation", that is, it renders nothing, not even a newline
    out = """
        pre
        post
    """
    assert render(src).strip() == out.strip()
    
def test_017_comments():
    src = """
        # comment
        -- comment
        ---- comment
        div
            p   | title
            # comment
             more lines
    """                                 # block comments
    out = """
        <div>
            <p>title</p>
        </div>
    """
    assert render(src).strip() == out.strip()
    src = """
        p        -- comment
        p:       #  comment
        .        -- comment
        for i in range(1)    #  comment
            .                -- comment
        for i in range(1):   --  comment
            .
        if True             -- why not?
            | yes
        else:               # no no no
            | no
    """                                 # inline comments
    out = """
        <p></p>
        <p></p>



        yes
    """
    assert render(src).strip() == out.strip()
    src = """
        | a
        # this is a long ...
            multiline ...
          block comment
        | b
        -- this is another long ...
         multiline ...
         block comment
        | c
    """                                 # inline comments
    out = """
        a
        b
        c
    """
    assert render(src).strip() == out.strip()

def test_018_while():
    src = """
        $i = 3
        while i:
            | $i
            $i = i - 1
    """
    out = """
        3
        2
        1
    """
    assert render(src).strip() == out.strip()
    src = """
        $i = 0
        while i < 3
            | $i
            $i = i + 1
    """
    out = """
        0
        1
        2
    """
    assert render(src).strip() == out.strip()
    src = """
        $i = 0
        while False / $i
    """
    assert render(src).strip() == ""
    
def test_019_inplace_assign():
    src = """
        $i   = 7
        $i  += 2
        $i  -= 2
        $i  *= 2
        $i  /= 2
        $i //= 2
        $i  %= 2
        $i   = int(i)
        $i <<= 2
        $i >>= 2
        $i  &= 2
        $i  |= 1
        $i  ^= 123
        $i  ^= 123
        while i < 4
            | $i
            $i += 1
    """
    out = """
        1
        2
        3
    """
    assert render(src).strip() == out.strip()

    src = """
        $x = 1
        div
            $x += 1     -- this <variable> reads "x" from the upper level and assigns a new "x" in a narrower name scope
            | $x
        | $x
    """
    out = """
        <div>
            2
        </div>
        1
    """
    assert render(src).strip() == out.strip()

    
def test_020_expression_in_string():
    src = """
        $size = '10'
        p style={"font-size:" size}
        p style={"font-size:" $size}
        p style=("font-size:" + size)
    """
    out = """
        <p style="font-size:10"></p>
        <p style="font-size:10"></p>
        <p style="font-size:10"></p>
    """
    assert render(src).strip() == out.strip()
    src = """
        $size = '10'
        p style =  'font-size: $size'
        p style =  "font-size: $size px"
        p style =  "font-size:{size}px"
        p style = r'font-size: $size px'
        p style = r"font-size: {size}"
    """
    out = """
        <p style="font-size: 10"></p>
        <p style="font-size: 10 px"></p>
        <p style="font-size:10px"></p>
        <p style="font-size: $size px"></p>
        <p style="font-size: {size}"></p>
    """
    assert render(src).strip() == out.strip()
    src = """
        $size = '10'
        | size {"= $size"}px
    """
    out = """
        size = 10px
    """
    assert render(src).strip() == out.strip()
    src = """
        $size = 10
        | a { "b $size b" } a
        | a { "b { "c {size} c" } b" } a
    """
    out = """
        a b 10 b a
        a b c 10 c b a
    """
    assert render(src).strip() == out.strip()

def test_021_recursion():
    src = """
        p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
            p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                    p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                        p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                            p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                                p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                                    p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                                        p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                                            p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                                                p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                                                    p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                                                        p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p:p
                                                            | kot
    """
    assert 'kot' in render(src)
    
def test_022_builtins():
    src = """
        dedent
            div
                p
                    i
                        | kot
    """
    out = """
        <div>
        <p>
        <i>
        kot
        </i>
        </p>
        </div>
    """
    assert render(src).strip() == out.strip()
    src = r"""
        inline
           | text1
           | {'text2 \n text3' : inline}
    """
    out = """
        text1 text2 text3
    """
    assert render(src).strip() == out.strip()
    src = """
        unique
            | Ala ma kota
            | Ala ma kota
            div
                p
                p
            div
                i |   pies
                i | pies
                |   pies
                | pies
            | Ala ma kota
    """
    out = """
        Ala ma kota
        <div>
        <p></p>
        </div>
        <i>  pies</i>
        <i>pies</i>
        pies
    """
    assert render(src).strip() == out.strip()
    src = """
        for a, b, c in cycle((-1,-2), 'abcdefg', [1,2,3], stop='longest'):
            | $a, $b, $c
    """
    out = """
        -1, a, 1
        -2, b, 2
        -1, c, 3
        -2, d, 1
        -1, e, 2
        -2, f, 3
        -1, g, 1
    """
    assert render(src).strip() == out.strip()
    src = """
        for a, b in cycle('abcdefg', [1,2,3]):
            | $a, $b
    """
    out = """
        a, 1
        b, 2
        c, 3
        d, 1
        e, 2
        f, 3
        g, 1
    """
    assert render(src).strip() == out.strip()
    src = """
        for v, change in changes([1,1,2,2,3,3]):
            | $v, $change
    """
    out = """
        1, True
        1, False
        2, True
        2, False
        3, True
        3, False
    """
    assert render(src).strip() == out.strip()
    src = """
        for v, change in changes([1,1,2,2,3,3], first = False):
            | $v, $change
    """
    out = """
        1, False
        1, False
        2, True
        2, False
        3, True
        3, False
    """
    assert render(src).strip() == out.strip()

def test_023_html():
    src = """
        comment !  $ { } x y z
        comment !
            this is an outline comment | $ {}
        comment
            ! this is an outline comment | $ {}
    """
    out = """
        <!-- $ { } x y z-->
        <!--
        this is an outline comment | $ {}
        -->
        <!--
            this is an outline comment | $ {}
        -->
    """
    assert render(src).strip() == out.strip()
    src = """
        script type="text/javascript"
          comment !
              $(window).resize(sectionHeight);
    """
    out = """
        <script type="text/javascript">
          <!--
          $(window).resize(sectionHeight);
          -->
        </script>
    """
    assert render(src).strip() == out.strip()
    src = r"""
        script !
            var sectionHeight = function() {
              var total    = $(window).height(),
                  $section = $('section').css('height','auto');
            
              if ($section.outerHeight(true) < total) {
                var margin = $section.outerHeight(true) - $section.height();
                $section.height(total - margin - 20);
              } else {
                $section.css('height','auto');
              }
            }
            
            $(window).resize(sectionHeight);
            
            $(function() {
              $("section h1, section h2, section h3").each(function(){
                $("nav ul").append("<li class='tag-" + this.nodeName.toLowerCase() + "'><a href='#" + $(this).text().toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g,'') + "'>" + $(this).text() + "</a></li>");
                $(this).attr("id",$(this).text().toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g,''));
                $("nav ul li:first-child a").parent().addClass("active");
              });
            
              $("nav ul li").on("click", "a", function(event) {
                var position = $($(this).attr("href")).offset().top - 190;
                $("html, body").animate({scrollTop: position}, 400);
                $("nav ul li a").parent().removeClass("active");
                $(this).parent().addClass("active");
                event.preventDefault();
              });
            
              sectionHeight();
            
              $('img').on('load', sectionHeight);
            });
    """
    out = r"""
        <script>
        var sectionHeight = function() {
          var total    = $(window).height(),
              $section = $('section').css('height','auto');

          if ($section.outerHeight(true) < total) {
            var margin = $section.outerHeight(true) - $section.height();
            $section.height(total - margin - 20);
          } else {
            $section.css('height','auto');
          }
        }

        $(window).resize(sectionHeight);

        $(function() {
          $("section h1, section h2, section h3").each(function(){
            $("nav ul").append("<li class='tag-" + this.nodeName.toLowerCase() + "'><a href='#" + $(this).text().toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g,'') + "'>" + $(this).text() + "</a></li>");
            $(this).attr("id",$(this).text().toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g,''));
            $("nav ul li:first-child a").parent().addClass("active");
          });

          $("nav ul li").on("click", "a", function(event) {
            var position = $($(this).attr("href")).offset().top - 190;
            $("html, body").animate({scrollTop: position}, 400);
            $("nav ul li a").parent().removeClass("active");
            $(this).parent().addClass("active");
            event.preventDefault();
          });

          sectionHeight();

          $('img').on('load', sectionHeight);
        });
        </script>
    """
    assert render(src).strip() == out.strip()
    

def test_024_import():
    src = """
        import $x, $y
        | $x, $y
    """
    assert render(src, x = 10, y = 'abc').strip() == "10, abc"
    src = """
        from ~ import $x, $y
        | $x, $y
    """
    assert render(src, x = 10, y = 'abc').strip() == "10, abc"
    src = """
        | $abs(-5)
    """                                         # import of defaults (built-ins)
    assert render(src).strip() == "5"
    src = """
        from builtins import *
        from builtins import $ord
        from ~ import *
        import *
        | $ord(x)
    """
    assert render(src, x = 'A').strip() == "65"
    src = """
        from hypertag.html import *
        from hypertag.html import %p as PARAGRAPH
        PARAGRAPH | kot
    """
    assert render(src).strip() == "<p>kot</p>"

    src = """
        from hypertag.tests.sample1 import $x, $f
        | $x
        | $f(2)
    """
    out = """
        155
        310
    """
    assert render(src).strip() == out.strip()
    src = """
        from hypertag.tests.sample2 import $x
        | $x
    """
    assert render(src).strip() == "155"
    src = """
        from hypertag.tests.sample2 import %H
        H 3
        $x = 10
        H 0
            | abc
    """
    out = """
        158
        465
        155
        abc
        0
    """
    assert render(src).strip() == out.strip()

def test_025_empty_control():
    """
    Empty control blocks (missing body) are considered by Hypertag as syntactically correct.
    This is necessary for detailed error reporting: method HypertagAST._locate_error() relies on the fact
    that truncating an arbitrary number of trailing lines of a script never introduces syntax errors
    unless they already have been present in the preceeding lines.
    """
    src = """
        if False
        elif (True * 5)
        else
        if (3*4):
        if True |
        elif False /
    """
    assert render(src).strip() == ""
    src = """
        for i in [1,2]
        for i in [1,2]:
        for i in [1,2] :
        for i in [1,2] /
        for i in [1,2] |
        for i in [1,2]!
    """
    assert render(src).strip() == ""
    src = """
        while True and False
        while 1 + 2 != 3:
        while False|
    """
    assert render(src).strip() == ""
    src = """
        ?
        ? |
        try
        try:
        try :
        try |
        try
        else
        else :
    """
    assert render(src).strip() == ""

def test_026_attributes():
    src = """
        %T a b c:
            | {a b c}
        T "yes" (-2) True
    """
    out = """
        yes-2True
    """
    assert render(src).strip() == out.strip()

def test_027_pipelines():
    
    src = """
        | { 'Hypertag' : str.upper : list : sorted(reverse=True) }
    """
    assert render(src).strip() == "['Y', 'T', 'R', 'P', 'H', 'G', 'E', 'A']"
    src = """
        | { 'Hypertag':str.upper():sorted }
    """
    assert render(src).strip() == "['A', 'E', 'G', 'H', 'P', 'R', 'T', 'Y']"
    
def test_028_django_filters():
    
    from hypertag.django.filters import slugify
    assert slugify('Hypertag rocks') == 'hypertag-rocks'

    src = """
        from hypertag.django.filters import $slugify
        | { 'Hypertag rocks' : slugify }
    """
    assert render(src).strip() == "hypertag-rocks"
    src = """
        from hypertag.django.filters import *
        | { 'Hypertag rocks' : slugify : upper }
    """
    assert render(src).strip() == "HYPERTAG-ROCKS"
    src = """
        from hypertag.django.filters import *
        | { '123.45' : floatformat(4) }
    """
    assert render(src).strip() == "123.4500"
    src = """
        from hypertag.django.filters import $apnumber, $ordinal
        | "5" spelled out is "{ 5:apnumber }"
        | example ordinals {1:ordinal}, {2:ordinal}, {5:ordinal}
    """
    out = """
        "5" spelled out is "five"
        example ordinals 1st, 2nd, 5th
    """
    assert render(src).strip() == out.strip()
    
def test_029_charset():
    src = """
        div ąłę_źó:1-x = ''
        div 更車-賈滑 = ''
    """
    out = """
        <div ąłę_źó:1-x=""></div>
        <div 更車-賈滑=""></div>
    """
    assert render(src).strip() == out.strip()
    src = r"""
        | {'abc' + '\n\x55\t' + 'def'}
    """
    out = """
        abc
        U	def
    """
    assert render(src).strip() == out.strip()
    

#####################################################################################################################################################

def test_100_varia():
    src = """
        h1 : a href="http://xxx.com": |This is <h1> title
            p  / And <a> paragraph.
        div
            | Ala { 'ęłąśźćóÓŁĄĘŚŻŹĆ' } ęłąśźćóÓŁĄĘŚŻŹĆ
              kot.
            / i pies
        
        div #box .top .grey
        div #box .top .grey-01
        input enabled=True
    """
    out = """
        <h1><a href="http://xxx.com">This is &lt;h1&gt; title
            <p>And <a> paragraph.</p></a></h1>
        <div>
            Ala ęłąśźćóÓŁĄĘŚŻŹĆ ęłąśźćóÓŁĄĘŚŻŹĆ
            kot.
            i pies
        </div>

        <div id="box" class="top grey"></div>
        <div id="box" class="top grey-01"></div>
        <input enabled />
    """
    assert render(src).strip() == out.strip()

def test_101_varia():
    src = """
        % fancy_text @body size='10px':
            | *****
            p style=("color: blue; font-size: " size)
                @body
            | *****

        fancy_text '20px'
            | This text is rendered through a FANCY hypertag!
    """
    out = """
        *****
        <p style="color: blue; font-size: 20px">
            This text is rendered through a FANCY hypertag!
        </p>
        *****
    """
    assert render(src).strip() == out.strip()


#####################################################################################################################################################
#####
#####  MAIN
#####

# print('file:', __file__)

if __name__ == '__main__':
    # unittest.main()
    pytest.main(['-vW ignore::DeprecationWarning', f'--rootdir={os.path.dirname(__file__)}', __file__])
    