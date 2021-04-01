import os, sys, importlib

from hypertag.core.errors import ImportErrorEx, ModuleNotFoundEx
from hypertag.core.grammar import MARK_VAR, MARK_TAG, VAR, TAG, TAGS
from hypertag.core.ast import HypertagAST

PATH_SEP = os.path.sep


#####################################################################################################################################################
#####
#####  UTILITIES
#####

# set Python's global recursion limit to at least MIN_RECURSION_LIMIT to avoid RecursionError
# when parsing deeply nested scripts
MIN_RECURSION_LIMIT = 20000
sys.setrecursionlimit(max(sys.getrecursionlimit(), MIN_RECURSION_LIMIT))


def _join_path(base, path, sep = '.', ext = None):
    """
    Convert a relative import `path` to an absolute one by appending it to an absolute `base` path.
    The `base` can be any type of path: a file path (slash-separated) or an import path (dot-separated) -
    the `sep` argument determines what character is treated as a separator; the same character is inserted
    in the result instead of dots, in the `path` part of the output string. If `ext` is provided,
    it is appended as a file extension of the output path.
    """
    if base is None: return None
    
    orig_base = base
    orig_path = path
    
    assert path[:1] == '.'                  # `path` is a relative import path
    path = path[1:]
    
    if base[-1:] == sep:                    # truncate a trailing separator in the base path
        base = base[:-1]

    while path[:1] == '.':                  # move upwards the package tree if `path` starts with multiple dots
        if sep not in base:
            raise ImportErrorEx("attempted relative import (%s) beyond top-level package or folder (%s)" % (orig_path, orig_base))
        base = base.rsplit(sep, 1)[0]
        path = path[1:]

    fullpath = base + sep + path.replace('.', sep)
    if ext: fullpath += '.' + ext
    
    return fullpath


#####################################################################################################################################################
#####
#####  MODULES
#####

class Module:
    """Wrapper around all types of imported modules (Hypertag's, Python's)."""
    
    runtime  = None     # Runtime that created this module
    location = None     # canonical path of this module, for deduplication and caching; there can be many
                        # non-canonical (e.g., relative) paths pointing to the same module, but only one canonical path
    filename = None     # name of the file if this module was loaded from disk; mapped to __file__ inside a script
    package  = None     # Python package path of this module's package, if available; mapped to __package__ inside a script
    symbols  = None     # cached dict of this module's symbols; each symbol has a leading mark % or $
    
    def __init__(self, **kwattrs):
        for attr, value in kwattrs.items():
            setattr(self, attr, value)
    
    def __getitem__(self, key):
        return self.symbols[key]
        
    def get(self, key, default = None):
        return self.symbols.get(key, default)
        

class PyModule(Module):
    """Wrapper around a regular Python module and its global symbols."""
    
    module = None       # the original Python module
    
    def __init__(self, module):
        """
        Pull symbols (tags & variables) from a Python module and return as a dict.
        All top-level symbols are treated as variables; tags are pulled from a special module-level dictionary `__tags__`.
        """
        self.module   = module
        self.location = getattr(module, '__name__', None)
        self.filename = getattr(module, '__file__', None)
        self.package  = getattr(module, '__package__', None)
        
        self.symbols  = {VAR(name) : getattr(module, name) for name in dir(module)}
        
        # retrieve __tags__
        tags = self.symbols.pop(VAR('__tags__'), None)
        if tags:
            if not isinstance(tags, dict): raise ImportErrorEx("__tags__ must be a dict in %s" % module)
            
            # make sure that the tags being imported are assigned to the same names as configured in their Tag.name property
            for name, tag in tags.items():
                if name != tag.name: raise ImportErrorEx("tag's internal name (%s) differs from its public name (%s) in %s" % (tag.name, name, module))
            
            self.symbols.update({name if name[0] == MARK_TAG else TAG(name) : tag for name, tag in tags.items()})

class HyModule(Module):
    """Wrapper around a Hypertag script to be executed (translated). Stores results of translation."""
    
    script = None       # plain text of the Hypertag script
    dom    = None       # output DOM produced by translation
    state  = None       # internal State at the end of translation; needed when hypertags from this module are to be expanded
    
    def translate(self, builtins, __tags__, **variables):
    
        ast = HypertagAST(self.script, self)
        self.dom, self.symbols, self.state = ast.translate(builtins, __tags__, **variables)
        return self
        
    
class RootModule(HyModule):
    """Wrapper module for a top-level script, to provide a referrer module for other (imported) scripts."""
    

#####################################################################################################################################################
#####
#####  LOADERS
#####

class Loader:
    """
    Finding, loading, and caching modules.
    A loader takes an import path as specified in `import` block of a Hypertag script,
    together with the location of the referrer module; converts the path to its canonical form (subclass-dependent);
    loads the module and returns it as a dict of symbols. Caching of modules can be performed internally.
    Each Loader subclass represents a specific naming convention and an ontology of valid import paths.
    """
    cache = None        # dict of cached modules indexed by their canonical path (module.location);
                        # each Loader subclass is responsible for managing the cache by itself
    
    def __init__(self):
        self.cache = {}
    
    def load(self, path, referrer, runtime):
        """
        Try to load a module given its (non-canonical) path and a referrer module, and return a Module instance.
        If the path is invalid or the module can't be found, None is returned.
        If this method is overriden by subclasses, `self.cache` should be checked to avoid repeated loading
        of the same module every time after a `path` is converted to a canonical `location`; every newly loaded module
        should be put into cache.
        """
        location = self._find(path, referrer)
        if location is None: return None
        if location in self.cache: return self.cache[location]
        
        module = self.cache[location] = self._read(location, runtime)
        return module

    def _find(self, path, referrer):
        """
        Convert a path to its canonical form. The `referrer` is the module where the path occured.
        Return None if the path is invalid for this type of modules.
        """
        return None

    def _read(self, location, runtime):
        """Read a module identified by `location`. Return None if the module is missing."""
        return None
    
    @staticmethod
    def _make_absolute(path, referrer):
        """Utility method for internal purposes: converting a python import path to an absolute path."""
        if path[:1] != '.': return path                 # `path` is absolute, return it unchanged
        return _join_path(referrer.package, path)       # `path` is relative, convert it to an absolute one
        
        
class PyLoader(Loader):
    """
    Loader of regular Python modules. They are identified by absolute package paths (dot-separated, no initial dot),
    which are used as modules' unique locations. When importing a Python module from a Hypertag script using
    a RELATIVE package path, the script's module must have its `package` property set, otherwise it will be impossible
    to infer the referred module's package path.
    """

    def _find(self, path, referrer):
        """Absolute and relative Python paths are supported. The latter require that referrer's package is set."""
        return self._make_absolute(path, referrer)
        
    def _read(self, location, runtime):
        try:
            module = importlib.import_module(location)
            return PyModule(module)
        
        except ModuleNotFoundError:
            return None


class HyLoader(Loader):
    """
    Loader of Hypertag scripts located on disk.
    Import paths have the same structure as in Python: with a dot '.' separating subfolders (packages).
    Location of a module is defined as an absolute file system path to the script file.

    A relative import path (.XYZ) is converted to a file path rooted at the referrer's module folder
    (referrer.filename must be present) to obtain the location.
    
    For absolute paths, different methods are tried to obtain the location. The first one that succeeds
    (i.e., the file exists) is selected:
    
    1. resolve(import_path, referrer) is called to get a location; `resolve` function is an optional argument
       of HyLoader instantiation;
    2. location is being searched for using Python's import mechanism, like if the script was a Python file - this only
       works when the import path contains a package specifier, which points to a valid Python package (with __init__.py);
    3. location is created as a directory path based at the current folder of the process;
    4. location is created as a directory path based at the referrer's folder (like for relative imports).
    
    Import paths CAN refer to folders which are NOT valid Python packages (don't have __init__.py inside).
    HyLoader does not check the existence of __init__.py on directory paths to scripts.
    """
    
    SCRIPT_EXTENSION = 'hy'         # default file extension of Hypertag scripts

    def __init__(self, resolve = None):
        super(HyLoader, self).__init__()
        self.resolve = resolve

    def load(self, path, referrer, runtime):
        
        # whenever possible, python package path (python_path) of the module is inferred, so that its `package` can be set
        location = python_path = None
        ref_root = os.path.dirname(referrer.filename) if referrer.filename else None
        
        # relative import path is always resolved relative to the referrer's folder
        if path[:1] == '.':
            if ref_root:
                location = self._join_path(ref_root, path)
                python_path = self._make_absolute(path, referrer)
                
        # absolute import path can be resolved in several different ways; the first one that returns a valid file path is used
        else:
            # 1. try calling a resolve() function
            if self.resolve:
                location = self.resolve(path, referrer)
                if location in self.cache: return self.cache[location]
                if location and not os.path.exists(location):
                    location = None

            # 2. try the Python's standard import mechanism (importlib); must be applied to the parent package, not the script itself
            if not location and '.' in path:
                package_name, filename = path.rsplit('.', 1)
                pkg = importlib.import_module(package_name)                 # package_name is an absolute path, so referrer is not needed here
                package_path = pkg.__file__
                if package_path.endswith('.py'):
                    package_path = os.path.dirname(package_path)            # truncate /__init__.py part of a package file path
                
                location = package_path + PATH_SEP + filename + '.' + self.SCRIPT_EXTENSION
                python_path = package_path + '.' + filename
                if location and not os.path.exists(location):
                    location = python_path = None
                
            # 3. try using the process' current folder as a root
            if not location:
                location = self._join_path(os.getcwd(), '.' + path)
                if location in self.cache: return self.cache[location]
                if location and not os.path.exists(location):
                    location = None

            # 4. try using the referrer's folder as a root
            if not location and ref_root:
                location = self._join_path(ref_root, '.' + path)
                python_path = self._make_absolute('.' + path, referrer)

        if not location or not os.path.exists(location):
            return None
        
        package = python_path.rsplit('.', 1)[0] if python_path else None
        
        script = open(location).read()
        
        module = self.cache[location] = runtime.translate(script, location, package)
        module.location = location
        module.package = package
        
        return module
        
    
    def _join_path(self, root, path):
        """Convert a python import `path` (with dots) to a file path (with slashes) and append to a root folder's path."""
        
        return _join_path(root, path, PATH_SEP, self.SCRIPT_EXTENSION)
        

#####################################################################################################################################################
#####
#####  RUNTIME
#####

class Runtime:
    """
    Runtime execution environment of Hypertag scripts.
    Defines a set of built-in symbols, a target language, and an escape function.
    Manages modules loading through a collection of predefined loaders.
    Modules are identified by "paths". The meaning of a particular path is determined by its loader.
    """

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

    loaders  = None     # list of Module subclasses whose static load() is called in sequence to find the first one
                        # that is able to locate and load a module by a given path
    
    default_loaders = [HyLoader, PyLoader]      # loaders to be used when no others are passed to __init__
    
    
    def __init__(self, loaders = None):
        self.loaders = loaders or self.default_loaders
        self.loaders = [loader if isinstance(loader, Loader) else loader() for loader in self.loaders]

    def import_builtins(self):
        """
        Import default symbols that shall be available to every script upon startup.
        This typically means all general-purpose symbols + standard tags/variables specific for a target language.
        """
        if self._builtins is None:
            self._builtins = {}
            for path in self.BUILTINS:
                module = self.import_module(path, RootModule(), None)
                self._builtins.update(module.symbols)
                
        return self._builtins
        
    def import_module(self, path, referrer, ast_node):
        """Import symbols that are defined in a module identified by `path`. Return as an instance of Module."""
        
        assert path

        for loader in self.loaders:
            module = loader.load(path, referrer, self)
            if module: return module

        raise ModuleNotFoundEx("import path not found '%s', try setting __package__ or __file__ when calling render()" % path, ast_node)
        
    def translate(self, __script__, __file__ = None, __package__ = None, __tags__ = None, **variables):
        
        builtins = self.import_builtins()
        builtins[VAR('__file__')]    = __file__
        builtins[VAR('__package__')] = __package__
        
        module = HyModule(runtime = self, script = __script__, filename = __file__, package  = __package__)
        module.translate(builtins, __tags__, **variables)
        
        return module
        
    def render(self, __script__, __file__ = None, __package__ = None, __tags__ = None, **variables):
        
        module = self.translate(__script__, __file__, __package__, __tags__, **variables)
        return module.dom.render()
        

