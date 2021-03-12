from hypertag.core.tag import TagFunction



class Registry:
    """A registry of standard tags and variables implemented by a given module."""
    
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
    
    def var(self, obj):
        """Register a given object as a Hypertag variable ($)."""
        assert False
        

