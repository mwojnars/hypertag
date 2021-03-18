import os, sys, importlib
from six.moves import builtins

from hypertag.core.errors import ImportErrorEx, ModuleNotFoundEx
from hypertag.core.grammar import MARK_TAG, MARK_VAR, TAGS
from hypertag.core.ast import HypertagAST
import hypertag.builtins


#####################################################################################################################################################
#####
#####  UTILITIES
#####

# set Python's global recursion limit to at least MIN_RECURSION_LIMIT to avoid RecursionError
# when parsing deeply nested scripts
MIN_RECURSION_LIMIT = 20000
sys.setrecursionlimit(max(sys.getrecursionlimit(), MIN_RECURSION_LIMIT))


def _read_module(module):
    """
    Pull symbols: tags & variables from a module and return as a dict.
    All top-level symbols are treated as variables; tags are pulled from a special dictionary named `__tags__`.
    """
    symbols = {MARK_VAR + name : getattr(module, name) for name in dir(module)}
    tags = symbols.pop(f'{MARK_VAR}__tags__', None)
    if tags:
        if not isinstance(tags, dict): raise ImportErrorEx(f"__tags__ must be a dict in {module}")
        
        # make sure that the tags being imported are assigned to the same names as configured in their Tag.name property
        for name, tag in tags.items():
            if name != tag.name: raise ImportErrorEx(f"tag's internal name ({tag.name}) differs from its public name ({name}) in {module}")
        
        symbols.update({name if name[0] == MARK_TAG else MARK_TAG + name : tag for name, tag in tags.items()})
        
    return symbols


class Module:
    
    def __init__(self, symbols, state = None):
        self.symbols = symbols
        self.state   = state
        

#####################################################################################################################################################
#####
#####  RUNTIME
#####

class Runtime:
    """
    Base class for runtime execution environments of Hypertag scripts. A runtime keeps references to external
    scripts and modules, as well as dynamic *context* of a particular execution.
    Enables import of tags and variables from these external sources to a Hypertag script.
    Sources are identified by "paths". The meaning of a particular path is determined by the Runtime or its subclasses.
    In the future, Runtime may include a *routing* mechanism that maps external names of resources
    to an arbitrarily defined namespace of paths as visible to a script.
    
    Context = virtual module whose contents is initialized when a new script is to be rendered;
              all scripts imported by the initial one use the SAME context (!);
              denoted by "~" import path:  from ~ import $x, %tag
    """
    
    # predefined constants
    PATH_CONTEXT     = '~'          # import path of the global context
    SCRIPT_EXTENSION = 'hy'         # file extension of Hypertag scripts; used during import
    

    # precomputed dict of built-in symbols to avoid recomputation on every __init__()
    BUILTINS = _read_module(builtins)
    BUILTINS.update(_read_module(hypertag.builtins))
    
    # symbols to be imported automatically upon startup; subclasses may define a broader collection
    DEFAULT = BUILTINS
    
    standard_modules = {
        PATH_CONTEXT: {},
    }

    language = None     # target language the documents will be compiled into, defined in subclasses
    #compact  = True    # if True, compactification is performed after analysis: pure (static, constant) nodes are replaced with their pre-computed render() values,
                        # which are returned on all subsequent render() requests; this improves performance when
                        # a document contains many static parts and variables occur rarely
    escape   = None     # escaping function or static method that converts plaintext to target language; typically, when assigned
                        # in a subclass, staticmethod() must be applied as a wrapper to prevent this attr be treated as a regular method:
                        #   escape = staticmethod(custom_function)

    modules  = None     # cached symbols of modules: {canonical_path: module}, where "module" is a dict of symbols and their values
    
    @property
    def context(self): return self.modules[self.PATH_CONTEXT]

    
    def __init__(self, __tags__ = None, **variables):
        """
        :param __tags__: dict of tag names and their Tag instances/classes that shall be made available to the script
                     as a dynamic "context" of execution; names can be prepended with '%', though this is not mandatory
        :param variables: names of external variables that shall be made available to the script
                     as a dynamic "context" of execution
        """
        self.modules = self.standard_modules.copy()
        self.update_context(__tags__, variables)
        
    def update_context(self, tags, variables):
        
        if not (tags or variables): return
        self.modules[self.PATH_CONTEXT] = context = self.modules[self.PATH_CONTEXT].copy()
        context.update(self._create_context(tags, variables))
        
    @staticmethod
    def _create_context(tags, variables):

        context = {}
        if tags:
            # TODO: check if names of tags are non-empty and syntactically correct
            context.update({name if name[0] == MARK_TAG else MARK_TAG + name : link for name, link in tags.items()})
        if variables:
            context.update({MARK_VAR + name : value for name, value in variables.items()})
        return context

    # def import_one(self, symbol, path = None, ast_node = None):
    #     """`symbol` must start with either % or $ to denote whether a tag or a variable should be imported."""
    #
    #     module = self.import_module(path, ast_node)
    #     if symbol not in module: raise ImportErrorEx(f"cannot import '{symbol}' from a given path ({path})", ast_node)
    #     return module[symbol]
    #
    # def import_all(self, path = None, ast_node = None):
    #     """
    #     Import all available symbols (tags and variables) from a given `path`, private symbols excluded.
    #     A private symbol is the one whose name (after %$) starts with "_".
    #     Return a dict of {symbol: object} pairs. Every symbol starts with either % (a tag) or $ (a variable).
    #     """
    #     module = self.import_module(path, ast_node)
    #     return {name: value for name, value in module.items() if name[1] != '_'}

    def import_default(self):
        """
        Import default symbols that shall be available to every script upon startup.
        This typically means all built-in symbols + standard tags/variables specific for a target language.
        """
        return self.DEFAULT
    
        
    def import_module(self, path, ast_node):

        path_canonical = self._canonical(path)
        module = self.modules.get(path_canonical)

        if module is None:
            module = self._load_module(path_canonical, ast_node)
            if not module: raise ModuleNotFoundEx(f"import path not found '{path}', try setting __package__ or __file__ in parsing context", ast_node)
            self.modules[path_canonical] = module
            
        if isinstance(module, Module):
            return module.symbols, module.state
        else:
            return module, None

    def _canonical(self, path):
        """Convert `path` to its canonical form."""
        if path is None: return self.PATH_CONTEXT
        return path
        
    def _load_module(self, path, ast_node):
        """Path must be already converted to a canonical form."""
        
        module = self._load_module_hypertag(path)
        if module: return module

        module = self._load_module_python(path)
        if module: return module
        
        return None
        
    def _load_module_hypertag(self, path):
        """"""
        # from package.script ...     -- "package." prefix must be present to allow file identification
        # from .package.script ...    --
        # from script ...             -- only possible when __file__ of the calling script is defined; "script.hy" is always looked for in the same folder as the calling script
        # from .script
        
        referrer_file    = self.context.get(f'{MARK_VAR}__file__')
        referrer_package = self.context.get(f'{MARK_VAR}__package__')
        
        # package path is present? the package & file can be localized through `importlib`
        if '.' in path:
            package_name, filename = path.rsplit('.', 1)
            package = importlib.import_module(package_name, referrer_package)
            package_name = package.__name__                                 # package_name could have been relative, must be changed to absolute
            package_path = package.__file__
            if package_path.endswith('.py'):
                package_path = os.path.dirname(package_path)                # truncate /__init__.py part of a package file path
            filepath = f'{package_path}/{filename}.{self.SCRIPT_EXTENSION}'
            
        else:
            # no package path? the script must be in the same folder as __file__
            if referrer_file is None: return None
            folder   = os.path.dirname(referrer_file)
            filepath = f"{folder}/{path}"
            package_name = referrer_package
            
        if not os.path.exists(filepath):
            return None
        
        script = open(filepath).read()

        # context (~) has already been initialized by a calling method and will be available to the script below (!)
        dom, symbols, state = self.translate(script, __file__ = filepath, __package__ = package_name)
        return Module(symbols, state)
    
        
    def _load_module_python(self, path):
        """
        Both absolute and relative Python paths are supported. The latter require that "$__package__" variable
        is properly set in the context.
        """
        package = self.context.get(f'{MARK_VAR}__package__')
        try:
            module = importlib.import_module(path, package)
            return Module(_read_module(module))
        except:
            return None

    def translate(self, script, __file__ = None, __package__ = None,  __tags__ = None, **variables):
        
        globals_ = self.import_default()
        globals_[f'{MARK_VAR}__file__']    = __file__
        globals_[f'{MARK_VAR}__package__'] = __package__
        self.update_context(__tags__, variables)
        
        ast = HypertagAST(script, self, globals_)
        return ast.translate()
        
    def render(self, script, __file__ = None, __package__ = None, __tags__ = None, **variables):
        
        dom, symbols, state = self.translate(script, __file__, __package__, __tags__, **variables)
        return dom.render()
        

# class CompoundRuntime(Runtime):
#     """Runtime that combines multiple sub-runtimes, each one having its own XX/ prefix to be added to import paths."""
#
#     loaders = {
#         'HY':   HypertagLoader,
#         'PY':   PythonLoader,
#         'file': FileLoader,
#     }
    
