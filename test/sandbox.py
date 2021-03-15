from hypertag.core.ast import HypertagAST


########################################################################################################################################################
#####
#####  MAIN
#####

if __name__ == '__main__':
    
    from hypertag.core.run_html import HyperHTML
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
    
    text = """
    from builtins import $list as LIST
    
    | $LIST((1,2,3))
    
    %JS @code
        script type="text/javascript"
          / <!--
          ....
              @code
          / -->
    
    | abc
    |
      abc
    
    | ---
    div |
      Line 1
      Line 2
    div
      | Line 1
      | Line 2
      
    JS
      | ala ma kota
    
    #javascript !
    JS !
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
    text = r"""
    from builtins import $sorted, $list as LIST
    | $sorted(LIST((3,2,1)))
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
    
    print("===== After rendering =====")
    print(tree.render(), end = "=====\n")
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
# - builtin tags
