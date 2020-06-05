registry = {}


class MultiMethod(object):
    """
    Dispatch methods based on type signature
    Use ``dispatch`` to add implementations
    """

    def __init__(self, name):
        self.name = name
        self.funcs = {}
        self.typemap = {}

    def register(self, *types):
        """ register dispatcher with new implementation"""

        def _(func):
            self.add(types, func)
            return func

        return _

    def add(self, signature, func):
        """"" Add new types/method pair to dispatcher"""
        self.funcs[signature] = func

    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args)
        try:
            func = self.typemap[types]
        except KeyError:
            func = self.dispatch(*types)
            self.typemap[types] = func
        return func(*args)

    def dispatch(self, *types):
        """Deterimine appropriate implementation for this type signature"""
        return self.funcs[types]


global_namespace = {}


def dispatch(*types, **kwargs):
    """
    Dispatch function on the types of the inputs
    Supports dispatch on all non-keyword arguments.

    """
    namespace = kwargs.get('namespace', global_namespace)

    def _(func):
        name = func.__name__
        if name not in namespace:
            namespace[name] = MultiMethod(name)
        dispatcher = namespace[name]
        dispatcher.add(types, func)
        return dispatcher

    return _
