from hypertag import HyperHTML, Runtime
from hypertag.core.ast import HypertagAST
from hypertag.core.runtime import RootModule


########################################################################################################################################################
#####
#####  MAIN
#####

if __name__ == '__main__':

    DEBUG = True
    ctx = {}
    
    # text = """
    #     $g = 100
    #     %g x | xxx {x+g}
    #     %H @body a=0
    #         @ body
    #         $g = 200
    #         g (g+5)
    #         g a[0] !
    #     H [0,6]?
    #         | pies
    # """
    # text = """
    #     $ x = 0
    #     try | x $x!
    #     else:
    #         try  / x*2 = {x*2}!
    #         else / x+1 = {x+1}!
    # """
    text = """
        DIV
            < try | {True}!
            < try | {False}!
            <? | {True}!
            <? | {False}!
    """
    text = """
        if False:
            $ x = 5
        else:
            $ x = 10
        | {x}
    """
    # text = """
    #     if False
    #         $x = 1
    #         %H | $x
    #     else
    #         $x = 2
    #         %H | {x*2}
    #         $x = 3
    #     $x = 4
    #     H
    # """

    # text = """
    #     for i in [2,1,0]:
    #         if $i
    #             $a = 1
    #         else
    #             $b = 2
    #         | $a
    # """
    text = """
        %H x
            if $x
                $a = 1
            else
                $b = 2
            | $a
        H 1
        H 0
    """
    # TODO: dodać czyszczenie slotów w `state` po wykonaniu bloku, przynajmniej dla xblock_def.expand() ??
    
    text = r"""
        %G x
            p | $x
            i : b | $x
        G 0
        G 1
        div .wide
            p #par1
                b : i | bleble
    """
    text = r"""
    ul .short-list
        li : i | Item
    
    for i in [1,2,3]:
        b class="row$i" | Row no. $i
    
    p id='paragraph1'
        b : i
            | Paragraph

    % hypertag @body x y=0
        | Title $x $y
        @ body
        for node in list(body.walk('postorder')):
            | node class $node.__class__.__name__ tag {node.tag.name if node.tag else 'None'}
    hypertag 1 y=2
        p
            b | Paragraph
        
    """
    text = """
    % tableRow @info name price='UNKNOWN'
        tr
            td | $name
            td | $price
            td
               @ info           # inline form can be used as well:  td @ info
            / $info
            / $info.render()

    tableRow 'Porsche' '200,000'
        img src="porsche.jpg"
        / If you insist on <s>air conditioning</s>, 🤔
    """
    text = """
    %toc @document
        for heading in document['h2']
            $ id = heading.get('id', '')
            li : a href="#{id}" @ heading.body

    %with_toc @document
        | Table of Contents:
        ol
            toc @document

        | The document:
        @document
        
        #
            | Everything except 'h2':
            @document.skip('h2')
    
            | Everything except 'i':
            @document.skip('i')

    with_toc
        h2 #first  | First heading
        p  | text...
        h2 #second | Second heading
        p  | text...
        h2 #third  | Third heading
        p  | text...
        
        p : i | Contents...
    """
    
    # ctx  = {'x': 10, 'y': 11, 's': "A"}
    # text = """
    #     context $x            # variable "x"
    #     context $y as z       -- variable "y" renamed internally to "z"
    #     | {x + z}
    # """
    # text = """
    #     context $s
    #     from builtins import *
    #     from builtins import $ord
    #     #from ~ import *
    #     #import *
    #     | $ord(s)
    # """
    # text = """
    # from hypertag.tests.sample2 import %G
    # %H | hypertag
    # / {%div('kot', id=5)}
    # / G is: {%G()} .
    # / H is: {%H()} .
    #
    # %link @text
    #     a href='#' @text
    #
    # link | Ala
    # link
    #     | kot
    # b / ({%link('pies')})
    #
    # / {%div('plain text').upper()}
    #
    # %t x | {10+x}
    # | { %t(x=5) }
    # """
    # text = """
    # %f x
    #     | this is x: $x
    #     if x > 0:
    #        f (x-1)
    # f 5
    # """
    text = """
        $c = 0
        p
            for x in [1,2,3]:
                | $c
                $c = x
    """
    text = """
        $c = 0
        %H
            for x in [1,2,3]:
                $c = x
                | $c
        H
        | $c
    """
    text = """
        | {"ab cd ef gh" : truncate(7)}
        | {"abcdefgh" : truncate(7)}
        | {"a b cdefgh" : crop(9)}
        | {"a b cdefgh" : crop(9, maxdrop=2)}
        | {"abc def ghi jkl mno pqr" : truncate(9, maxdrop=2)}
    """
    
    root = RootModule(runtime = HyperHTML(), filename = __file__, package = __package__)
    tree = HypertagAST(text, root, verbose = True)
    
    # print()
    # print("===== AST =====")
    # print(tree.ast)
    # print(type(tree.ast))
    # print()
    print("===== After rewriting =====")
    print(tree)
    print()
    
    #
    # print("===== After semantic analysis =====")
    # tree.analyse()
    # # print()
    # # print(tree)
    # print()
    
    print("===== After translation =====")
    dom, _, _ = tree.translate(**ctx)
    print('DOM:')
    print(dom.tree('  '))
    print()

    print("===== After rendering =====")
    print(dom.render(), end = "=====\n")
    # print(tree.A())
    
    # import inspect, importlib
    # print(__file__)
    # module = importlib.import_module('.', 'hypertag.core')  #__package__)
    # print(module.__name__)
    # print(module.__file__)
    # print(module.__package__)
    # print(inspect.getfile(module))
    # print(inspect.getfile(text))
    # from hypertag.django.filters import slugify
    # print(slugify('Hypertag rocks'))
    # __package__ = "hypertag.core"
    # from .runtime import __file__, __name__
    # from hypertag.core.runtime import __file__
    # print(__name__)
    
    
# TODO:
# - czyszczenie slotów w `state` po wykonaniu bloku, przynajmniej dla xblock_def.expand() ??
# - Markdown/Textile/Sass/Scss blocks
# - Runtime & Loader: detection of circular imports
# - Python's "bitwise not" operator (~)
