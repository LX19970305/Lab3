from multipledispatch import dispatch
from multipledispatch import Dispatcher


def test_multipledispatch():
    @dispatch(int, int)
    def rev(a, b):
        return a - b

    @dispatch(float, float)
    def rev(a, b):
        return a + b

    @dispatch(object, object)
    def rev(a, b):
        return "%s + %s" % (a, b)

    assert rev(7, 3) == 4
    assert rev(1.3, 1.3) == 2.6
    assert rev(1, 'hello') == '1 + hello'


class A(object): pass


class B(object): pass


class C(A): pass


class D(C): pass


class E(C): pass


def test_inheritance():
    @dispatch(A)
    def f(x):
        return 'a'

    @dispatch(B)
    def f(x):
        return 'b'

    assert f(A()) == 'a'
    assert f(B()) == 'b'
    assert f(C()) == 'a'


def test_register_stacking():
    f = Dispatcher('f')

    @f.register(list)
    @f.register(tuple)
    def rev(x):
        return x[::-1]

    assert rev((1, 2, 3)) == (3, 2, 1)
    assert rev([1, 2, 3]) == [3, 2, 1]


def test_arguments():
    f = Dispatcher('f')

    @f.register(int, int)
    @f.register(int)
    def rev(a, b=10):
        return a - b

    assert rev(10, 3) == 7
    assert rev(5) == -5
    assert rev(b=2, a=1) == -1


def test_addmethod():
    D = Dispatcher('add')

    D.add((int, int), lambda x, y: x + y)
    D.add((float, float), lambda x, y: x + y)

    assert D(1, 2) == 3
    assert D(1.0, 2.0) == 3.0



