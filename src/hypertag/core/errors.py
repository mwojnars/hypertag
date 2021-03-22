from hypertag.nifty.parsing import ParserError

########################################################################################################################################################

class HError(ParserError):
    def make_msg(self, msg):
        if not self.pos: return
        
        # convert `line`, `column` to coordinates of the original script from before INDENT/DEDENT encoding
        if self.node and self.column is not None:
            prefix  = self.node.fulltext[:self.pos[0]]
            symbols = self.node.tree.parser.symbols
            indents = prefix.count(symbols['INDENT_S']) + prefix.count(symbols['INDENT_T'])
            dedents = prefix.count(symbols['DEDENT_S']) + prefix.count(symbols['DEDENT_T'])
            indent  = indents - dedents
            column  = indent + self.column
        else:
            column  = None
        
        line = self.line - 1 if self.line else self.line
        
        if self.node and self.node.tree.filename:
            return msg + " in '%s', line %s, column %s (%s)" % (self.node.tree.filename, line, column, self.text)
        else:
            return msg + " at line %s, column %s (%s)" % (line, column, self.text)


# class HBaseException(BaseException):
#     """
#     Base class for exceptions that play internal role during execution of a Hypertag AST.
#     Their occurrence does NOT signal an error, rather they are intended to be caught by Hypertag internal code
#     at a higher level in the tree.
#     """
#
# class HBreak(HBaseException):
#     pass


########################################################################################################################################################

class SyntaxErrorEx(HError, SyntaxError):               pass
class ValueErrorEx(HError, ValueError):                 pass
class TypeErrorEx(HError, TypeError):                   pass
class NameErrorEx(HError, NameError):                   pass
class UnboundLocalEx(HError, UnboundLocalError):        pass
class UndefinedTagEx(HError):                           pass
class NotATagEx(HError):                                pass
class NoneStringEx(HError):                             pass
class ImportErrorEx(HError, ImportError):               pass
class ModuleNotFoundEx(ImportErrorEx):                  pass
class ParseErrorEx(HError):                             pass

class MissingValueEx(HError):
    """
    Empty (false) value was returned by an expression marked with "!" (obligatory) qualifier.
    Typically, this exception is caught at a higher level with a "try" block.
    """
    
class VoidTagEx(HError):
    """Raised when non-empty body is passed to a void tag (i.e., a tag that doesn't accept body)."""
    
