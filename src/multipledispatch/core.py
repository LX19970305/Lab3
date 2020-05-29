from .dispatcher import Dispatcher

global_namespace = dict()


def dispatch(*types, **kwargs):
    """ Dispatch function on the types of the inputs

    Supports dispatch on all non-keyword arguments.

    Collects implementations based on the function name.  Ignores namespaces.

    If ambiguous type signatures occur a warning is raised when the function is
    defined suggesting the additional method to break the ambiguity.

    """
    namespace = kwargs.get('namespace', global_namespace)

    # on_ambiguity = kwargs.get('on_ambiguity')

    # types = tuple(types)

    def _(func):
        name = func.__name__
        if name not in namespace:
            namespace[name] = Dispatcher(name)
        dispatcher = namespace[name]
        dispatcher.add(types, func)
        return dispatcher

    return _
