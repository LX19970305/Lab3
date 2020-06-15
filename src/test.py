from multimethod import dispatch
from multimethod import MultiMethod


def test_arguments():
    f = MultiMethod('f')

    @f.register(int, int)
    @f.register(int)
    def foo(a, b=10):
        return a - b

    assert foo(10, 3) == 7
    assert foo(5) == -5
    assert foo(b=2, a=1) == -1
    assert foo(a=1, b=2) == -1


def test_multipledispatch():
    @dispatch(int, int)
    def foo(a, b):
        return a - b

    @dispatch(float, float)
    def foo(a, b):
        return a + b

    assert foo(7, 3) == 4
    assert foo(1.3, 1.3) == 2.6


def test_addmethod():
    D = MultiMethod('add')

    D.add((int, int), lambda x, y: x + y)
    D.add((float, float), lambda x, y: x + y)

    assert D(1, 2) == 3
    assert D(1.0, 2.0) == 3.0


class A(object):
    pass


class B(A):
    pass


class C(A):
    pass


def test_inheritance():
    @dispatch(A)
    def foo(x):
        return 'AA'

    @dispatch(C)
    def foo(x):
        return 'CC'

    assert foo(A()) == 'AA'
    assert foo(B()) == 'AA'
    assert foo(C()) == 'CC'
