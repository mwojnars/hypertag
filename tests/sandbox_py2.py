#-*- coding: utf-8 -*-
"""
Sandbox for testing Hypertag with Python 2.
For now, we stop backporting to Python 2 because Parsimonious apparently does NOT support Python 2
(issues around Unicode handling).
"""

from __future__ import print_function
# from __future__ import unicode_literals

from hypertag.core.ast import HypertagAST


########################################################################################################################################################
#####
#####  MAIN
#####

if __name__ == '__main__':

    from hypertag import HyperHTML
    DEBUG = True
    
    print(u"test: ąłżęśćó ")
    
    text = u"""
        | Ala ma kota
    """
    
    tree = HypertagAST(text, HyperHTML(), stopAfter = "rewrite", verbose = True)
    
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
