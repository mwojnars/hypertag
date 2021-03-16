from hypertag.core.ast import HypertagAST


########################################################################################################################################################
#####
#####  MAIN
#####

if __name__ == '__main__':

    from hypertag import HyperHTML
    DEBUG = True

    text = """
        h1 : a href="http://xxx.com" : b : | This is <h1> title
            p / And <a> paragraph.
            p | tail text
                  tail text
               tail text
        div
            | Ala
              kot { 'Mru' "czek" 123 } {0}? {456}!
                Ola
            /     i pies
                  Azor

        if False:
            div #box .top .grey
        elif True:
            div #box class="bottom"
        else
            input enabled=True
        """

    # text = """
    #     $k = 5
    #     for i, val in enumerate(range(k-2), start = k*2):
    #         $ i = i + 1
    #         | $val at $i
    #     | $i
    # """
    # text = """
    #     p | Ala
    #     dedent nested=False
    #         div: | kot
    #             i | pies
    # """
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
    ctx  = {'x': 10, 'y': 11}
    text = """
        if True:
            import $x
        else:
            $x = 5
        | $x
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
    for i in [1,2,3]:
        b class="row$i" | Row no. $i
    
    ul
        li class='list-entry'
            | Item
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
    %toc @document
        for heading in document['h2']
            $ id = heading.get('id', '')
            a href = "#{id}" @ heading.body
                
    %with_toc @document
        | Table of Contents:
        toc @document
        
        | The document:
        @document
    
    with_toc
        h2 #first  | First heading
        p  | Contents...
        h2 #second | Second heading
        p  | Contents...
        h2 #third  | Third heading
        p  | Contents...
    """
    
    tree = HypertagAST(text, HyperHTML(**ctx), stopAfter = "rewrite", verbose = True)
    
    # print()
    # print("===== AST =====")
    # print(tree.ast)
    # print(type(tree.ast))
    # print()
    print("===== After rewriting =====")
    print(tree)
    print()
    

    print("===== After semantic analysis =====")
    tree.analyse()
    # print()
    # print(tree)
    print()
    
    print("===== After translation =====")
    dom, _, _ = tree.translate()
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
    
    
# TODO:
# - czyszczenie slotów w `state` po wykonaniu bloku, przynajmniej dla xblock_def.expand() ??
# - selectors @body[...]
# - Python's "bitwise not" operator (~)
