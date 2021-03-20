from hypertag.nifty.util import isfunction
from hypertag.core.tag import TagFunction


class Registry:
    """A registry of standard tags and variables (e.g., functions, filters) implemented by a given module."""
    
    def __init__(self):
        self.tags = {}
        self.vars = {}
    
    def tag(self, obj):
        """
        Register a given object (Tag subclass, Tag instance, tag function), as a tag by adding to self.tags.
        Tag subclasses are instantiated before adding to self.tags. Functions are wrapped up in TagFunction.
        """
        if isinstance(obj, type):           # instantiate tag classes
            tag  = obj()
            name = tag.name
        elif callable(obj):
            tag  = TagFunction(obj)
            name = obj.__name__
        else:
            tag  = obj
            name = obj.name

        self.tags[name] = tag
        return obj
    
    def var(self, name, obj = None):
        """Register a given object as a Hypertag variable ($)."""
        
        if obj is None:
            # name is not provided, object stored under `name`; must assume the object is a function, so the name can be deduced
            obj  = name
            assert isfunction(obj)
            name = obj.__name__
        
        self.vars[name] = obj
        return obj
        

