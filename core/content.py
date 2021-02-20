
#####################################################################################################################################################

class Element:
    """
    Element of a target document. There are 2 types of elements:
    - snippets - short inline strings intended for HORIZONTAL concatenation; no styling (paddings/margin) included
    - blocks - multiline strings intended for VERTICAL concatenation; may include styling:
               horizontal indentation and/or vertical leading/trailing margin (empty lines)
    Blocks, unlike snippets, may include nested blocks and be labelled with section names.
    """

#####################################################################################################################################################

class Block(Element):
    """
    Block of markup text to be rendered into a target document.
    May only be concatenated vertically with other blocks; it is disallowed to prepend/append to existing lines of a block.
    A block may be indented/dedented and its surrounding vertical space can be altered;
    other modifications (to the actual text inside block) are disallowed.
    Internally, a Block is represented as a list of sub-Blocks (ChainBlock), or a plain string (StringBlock).
    Indentation is stored separately and appended upon rendering.
    When nested blocks are being rendered, their indentations sum up.
    A block is ALWAYS rendered with a trailing '\n'. A block may render to None,
    in such case it is removed from the target document.
    """
    indent = None           # indentation of the entire block, to be prepended upon rendering
    section = None          # name of section this block belongs to; None means main section
    
    def render(self, base_indent = ''):
        raise NotImplementedError
    
class ChainBlock(Block):
    
    blocks = None           # list of sub-blocks as Block instances
    
    def render(self, base_indent = ''):
        indent = base_indent + self.indent
        blocks = [block.render(indent) for block in self.blocks]            # render sub-blocks
        blocks = [block for block in blocks if block is not None]           # drop blocks that render to None
        assert all(block and block[-1] == '\n' for block in blocks)
        return ''.join(blocks)
    
class TextBlock(Block):

    text = None
    
    def render(self, base_indent = ''):
        return
    
    
class SpaceBlock(Block):
    """1+ empty vertical lines."""
    
    height = None           # no. of empty lines to render
    
    def __init__(self, height):
        assert height >= 1
        self.height = height
        
    def render(self, base_indent = ''):
        return '\n' * self.height                   # empty lines do NOT have indentation

class EmptyBlock(Block):
    """Empty block to be ignored during rendering of the document."""
    
    def render(self, base_indent = ''):
        return None
    
class Inline(Element):
    """
    Inline element. Contrary to a Block, an Inline:
    - has no indentation
    - has no trailing newline \n
    - has no nested elements ??
    - has no label nor nested sections
    """
    

#####################################################################################################################################################

class Section:
    
    label = None        # string label of this section; empty string '' denotes the main section
    text  = None        # rendered contents of this section body; can be an empty string ''
    

# class Feed / Stream / Sequence
class Content:
    """
    List of labelled sections produced by a child node of the AST of a document.
    The first section is the main one, labelled by ''.
    The main section is always present and is unique (although its value can be an empty string).
    Other sections may not be unique (same label may occur multiple times).
    """
    sections = None     # list of Sections
    
    def __init__(self, main = '', **sections):
        pass
