import os, sys, importlib
from six.moves import builtins

from hypertag.core.errors import ImportErrorEx, ModuleNotFoundEx
from hypertag.core.grammar import MARK_VAR, MARK_TAG, VAR, TAG, TAGS
from hypertag.core.ast import HypertagAST
import hypertag.builtins

PATH_SEP = os.path.sep


#####################################################################################################################################################
#####
#####  UTILITIES
#####

# set Python's global recursion limit to at least MIN_RECURSION_LIMIT to avoid RecursionError
# when parsing deeply nested scripts
MIN_RECURSION_LIMIT = 20000
sys.setrecursionlimit(max(sys.getrecursionlimit(), MIN_RECURSION_LIMIT))


# def _read_module(module):
#     """
#     Pull symbols: tags & variables from a Python module and return as a dict.
#     All top-level symbols are treated as variables; tags are pulled from a special dictionary named `__tags__`.
#     """
#     symbols = {VAR(name) : getattr(module, name) for name in dir(module)}
#     tags = symbols.pop(VAR('__tags__'), None)
#     if tags:
#         if not isinstance(tags, dict): raise ImportErrorEx("__tags__ must be a dict in %s" % module)
#
#         # make sure that the tags being imported are assigned to the same names as configured in their Tag.name property
#         for name, tag in tags.items():
#             if name != tag.name: raise ImportErrorEx("tag's internal name (%s) differs from its public name (%s) in %s" % (tag.name, name, module))
#
#         symbols.update({name if name[0] == MARK_TAG else TAG(name) : tag for name, tag in tags.items()})
#
#     return symbols


#####################################################################################################################################################
#####
#####  MODULES
#####

class Module:
    """Base class for wrappers around all types of imported modules (Hypertag's, Python's)."""
    
    location = None     # canonical identifier (path) of this module, for deduplication and retrieval; there can be many
                        # non-canonical (e.g., relative) paths pointing to a given module, but only 1 canonical path
    symbols  = None     # cached dict of this module's symbols; each symbol has a leading mark % or $
    state    = None     # internal State at the end of translation of a Hypertag module; required for evaluation of imported hypertags
    
    def __getitem__(self, key):
        return self.symbols[key]
        
    def get(self, key, default = None):
        return self.symbols.get(key, default)
        
    def normalize(self, path):
        """Convert a path to its canonical form assuming that `self` is the referrer module where the path occured."""
        return path
    
        
# class Context(Module):
#     """Special type of module to hold dynamic context of script translation."""
#
#     def __init__(self, tags, variables):
#
#         self.symbols = symbols = {}
#
#         if tags:
#             # TODO: check if names of tags are non-empty and syntactically correct
#             symbols.update({name if name[0] in (MARK_TAG, MARK_VAR) else TAG(name) : link for name, link in tags.items()})
#         if variables:
#             symbols.update({VAR(name) : value for name, value in variables.items()})
    
    
class HyModule(Module):
    """"""
    
    def __init__(self, symbols, state):
        self.symbols = symbols
        self.state   = state
        
    
class PyModule(Module):
    """Wrapper around a regular Python module and its global symbols."""
    
    module = None       # the original Python module
    
    def __init__(self, module):
        """
        Pull symbols (tags & variables) from a Python module and return as a dict.
        All top-level symbols are treated as variables; tags are pulled from a special module-level dictionary `__tags__`.
        """
        self.module   = module
        self.location = module.__name__
        self.symbols  = {VAR(name) : getattr(module, name) for name in dir(module)}
        
        # retrieve __tags__
        tags = self.symbols.pop(VAR('__tags__'), None)
        if tags:
            if not isinstance(tags, dict): raise ImportErrorEx("__tags__ must be a dict in %s" % module)
            
            # make sure that the tags being imported are assigned to the same names as configured in their Tag.name property
            for name, tag in tags.items():
                if name != tag.name: raise ImportErrorEx("tag's internal name (%s) differs from its public name (%s) in %s" % (tag.name, name, module))
            
            self.symbols.update({name if name[0] == MARK_TAG else TAG(name) : tag for name, tag in tags.items()})
    
    def normalize(self, path):
        
        if path[:1] != '.': return path
        
        # `path` is relative, convert it to absolute
        return self._joinpath(self.module.__package__, path)
        
    @staticmethod
    def _joinpath(base, path):
        """Convert a relative package `path` to an absolute one by appending it to an absolute `base` path."""
        
        orig_base = base
        orig_path = path
        
        assert path[:1] == '.'
        path = path[1:]
        
        while path[0] == '.':           # move upwards the package tree if `path` starts with multiple dots
            if '.' not in base:
                raise ImportErrorEx("attempted relative import (%s) beyond top-level package (%s)" % (orig_path, orig_base))
            base = base.rsplit('.', 1)[0]
            path = path[1:]

        return base + '.' + path
        

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
    
    # PATH_CONTEXT     = '~'          # import path of the global context
    
    # predefined constants
    SCRIPT_EXTENSION = 'hy'         # file extension of Hypertag scripts; used during import

    # list of modules to be imported automatically into a script upon startup of translation (built-in symbols)
    BUILTINS = ['builtins', 'hypertag.builtins']
    
    # cached dict of built-in symbols, to avoid recalculation for every new AST
    _builtins = None

    language = None     # target language the documents will be compiled into, defined in subclasses
    #compact  = True    # if True, compactification is performed after analysis: pure (static, constant) nodes are replaced with their pre-computed render() values,
                        # which are returned on all subsequent render() requests; this improves performance when
                        # a document contains many static parts and variables occur rarely
    escape   = None     # escaping function or static method that converts plaintext to target language; typically, when assigned
                        # in a subclass, staticmethod() must be applied as a wrapper to prevent this attr be treated as a regular method:
                        #   escape = staticmethod(custom_function)

    modules  = None     # cached modules as a dict {canonical_path: module}
    
    # @property
    # def context(self):
    #     return self.modules.get(self.PATH_CONTEXT, {})

    
    def __init__(self):
        self.modules = {}

    def import_builtins(self):
        """
        Import default symbols that shall be available to every script upon startup.
        This typically means all general-purpose symbols + standard tags/variables specific for a target language.
        """
        if self._builtins is None:
            self._builtins = {}
            for path in self.BUILTINS:
                module = self.import_module(path, None)
                self._builtins.update(module.symbols)
                
        return self._builtins
        
    def import_module(self, path, ast_node):
        """Import symbols defined in a module identified by `path`. Return as an instance of Module."""
        
        assert path
        # path = self._canonical(path)
        module = self.modules.get(path)

        if module is None:
            module = self._load_module(path, ast_node)
            if not module: raise ModuleNotFoundEx("import path not found '%s', try setting __package__ or __file__ in parsing context" % path, ast_node)
            self.modules[path] = module
            
        return module

    # def _canonical(self, path):
    #     """Convert `path` to its canonical form."""
    #     if path is None: return self.PATH_CONTEXT
    #     return path
        
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
        
        referrer_file    = None  #self.context.get(VAR('__file__'))
        referrer_package = None  #self.context.get(VAR('__package__'))
        
        # package path is present? the package & file can be localized through `importlib`
        if '.' in path and (referrer_package or path[0] != '.'):
            #if path[0] == '.' and not referrer_package: return None
            package_name, filename = path.rsplit('.', 1)
            package = importlib.import_module(package_name, referrer_package)
            package_name = package.__name__                                 # package_name could have been relative, must be changed to absolute
            package_path = package.__file__
            if package_path.endswith('.py'):
                package_path = os.path.dirname(package_path)                # truncate /__init__.py part of a package file path
            filepath = '%s%s%s.%s' % (package_path, PATH_SEP, filename, self.SCRIPT_EXTENSION)
            
        else:
            # no package path? the script must be in the same folder as __file__
            if referrer_file is None: return None
            if path[0] == '.': path = path[1:]
            path = path.replace('.', PATH_SEP)
            folder   = os.path.dirname(referrer_file)
            filepath = folder + PATH_SEP + path
            package_name = referrer_package
            
        if not os.path.exists(filepath):
            return None
        
        script = open(filepath).read()
        
        # context (~) has already been initialized by a calling method and will be available to the script below (!)
        dom, symbols, state = self.translate(script, __file__ = filepath, __package__ = package_name)
        symbols[VAR('__file__')]    = filepath
        symbols[VAR('__package__')] = package_name

        return HyModule(symbols, state)
    
        
    def _load_module_python(self, path):
        """
        Both absolute and relative Python paths are supported. The latter require that "$__package__" variable
        is properly set in the context.
        """
        package = None  #self.context.get(VAR('__package__'))
        try:
            module = importlib.import_module(path, package)
            return PyModule(module)
        except:
            return None

    @staticmethod
    def make_context(tags, variables):
        """
        Combine two dicts of symbols into one. If a symbol lacks a leading mark ($,%), the mark is imputed
        as $ (for `variables`), or % (for `tags`).
        """
        symbols = {}

        if tags:
            # TODO: check if names of tags are non-empty and syntactically correct
            symbols.update({name if name[0] in (MARK_TAG, MARK_VAR) else TAG(name) : value for name, value in tags.items()})
        if variables:
            symbols.update({name if name[0] in (MARK_TAG, MARK_VAR) else VAR(name) : value for name, value in variables.items()})
        
        return symbols

    def translate(self, script, __file__ = None, __package__ = None,  __tags__ = None, **variables):
        
        builtins = self.import_builtins()
        builtins[VAR('__file__')]    = __file__
        builtins[VAR('__package__')] = __package__
        context = self.make_context(__tags__, variables)

        ast = HypertagAST(script, self, filename = __file__)
        return ast.translate(builtins, context)
        
        # if self.PATH_CONTEXT in self.modules:
        #     if __tags__ or variables: raise ImportErrorEx("dynamic context was already created and cannot be modified")
        #     context_created = False
        # else:
        #     self.modules[self.PATH_CONTEXT] = Context(__tags__, variables)
        #     context_created = True
        #
        # context = self.modules[self.PATH_CONTEXT].symbols
        # ast = HypertagAST(script, self, filename = __file__)
        #
        # try:
        #     return ast.translate(builtins, context)
        # finally:
        #     if context_created: del self.modules[self.PATH_CONTEXT]
            
        
    def render(self, script, __file__ = None, __package__ = None, __tags__ = None, **variables):
        
        dom, symbols, state = self.translate(script, __file__, __package__, __tags__, **variables)
        return dom.render()
        

#####################################################################################################################################################
#####
#####  LOADERS
#####

class Loader:
    """
    Base class for module loaders. A loader takes an import path as specified in `import` block of a Hypertag script,
    together with the location of the referrer module; converts the path to its canonical form (subclass-dependent);
    loads the module and returns it as a dict of symbols. Caching of modules can be performed internally.
    """

class StandardLoader:
    """A loader of Python and Hypertag modules that searches the disk in a way analogous to what Python does."""

# class CompoundLoader(Loader):
#     """Runtime that combines multiple sub-runtimes, each one having its own XX/ prefix to be added to import paths."""
#
#     loaders = {
#         'HY':   HypertagLoader,
#         'PY':   PythonLoader,
#         'file': FileLoader,
#     }
    
