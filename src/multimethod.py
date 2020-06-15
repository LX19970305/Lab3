class MultiMethod(object):
    """
    Dispatch methods based on type signature
    Use ``dispatch`` to add implementations
    """

    def __init__(self, name):
        """
        creates a MultiMethod object with a given name and an empty typemap.

        :param name: used for diagnostics
        """
        self.name = name
        self.funcs = {}
        self.typemap = {}

    def register(self, *types, **kwargs):
        """ register dispatcher with new implementation"""

        def _(func):
            self.add(types, func, **kwargs)
            return func

        return _

    def add(self, signature, func):
        """"" Add new types/method pair to dispatcher"""
        self.funcs[signature] = func
        self.ordering = ordering(self.funcs)

    def __call__(self, *args, **kwargs):
        """
        Make the MultiMethod object itself callable.
        It looks up the actual function to be called in the type map based on the parameter type passed in.
        """
        types = tuple(arg.__class__ for arg in args)
        try:
            func = self.typemap[types]
        except KeyError:
            func = self.dispatch(*types)
            self.typemap[types] = func
        return func(*args, **kwargs)

    def dispatch(self, *types):
        """Deterimine appropriate implementation for this type signature"""
        if types in self.funcs:
            return self.funcs[types]
        return next(self.dispatch_iter(*types))

    def dispatch_iter(self, *types):
        n = len(types)
        for signature in self.ordering:
            if len(signature) == n and all(map(issubclass, types, signature)):
                result = self.funcs[signature]
                yield result


def ordering(sign):
    """
    A sane ordering of signatures to check, first to lastTopoological sort of edges
    """
    sign = list(map(tuple, sign))
    edges = [(a, b) for a in sign for b in sign if edge(a, b)]
    edges = group(lambda x: x[0], edges)
    for s in sign:
        if s not in edges:
            edges[s] = []
    edges = dict((k, [b for a, b in v]) for k, v in edges.items())
    return topoSort(edges)


def edge(a, b, tie_breaker=hash):
    if (tie_breaker(a) > tie_breaker(b)):
        return True
    return False


def topoSort(edges):
    """
    inputs:
        edges - a dict of the form {a: {b, c}} where b and c depend on a
    outputs:
        L - an ordered list of nodes that satisfy the dependencies of edges
    """
    inputedges = dictionaryReverse(edges)
    inputedges = dict((k, set(val)) for k, val in inputedges.items())
    S = set((v for v in edges if v not in inputedges))
    orderList = []

    while (S):
        node = S.pop()
        orderList.append(node)
        for i in edges.get(node):
            inputedges[i].remove(node)
            if not inputedges[i]:
                S.add(i)
    return orderList


def dictionaryReverse(d):
    """
    Reverses direction of dependence dict
    """
    result = {}
    for key in d:
        for val in d[key]:
            result[val] = result.get(val, tuple()) + (key,)
    return result


def group(fun, edges):
    """
    Group a collection by a key function
    """

    d = {}
    for item in edges:
        key = fun(item)
        if key not in d:
            d[key] = list()
        d[key].append(item)
    return d


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