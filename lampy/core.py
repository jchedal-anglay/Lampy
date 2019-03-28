import builtins
import functools
import operator

from . import stream


class F:
    def __init__(self, fn):
        self.fn = fn
        self.__name__ = fn.__name__
        self.__doc__ = fn.__doc__

    def __rrshift__(self, other):
        """Function piping: x >> f -> f(x)."""
        return self(other)

    def __rshift__(self, other):
        """Function piping: x >> f -> f(x)."""
        return other(self)

    def __add__(self, other):
        """Function composition: (f + g + h)(x) -> f(g(h(x)))."""
        f = lambda *args, **kwargs: self(other(*args, **kwargs))
        return F(f)

    def __call__(self, *args, **kwargs):
        """Evaluates the wrapped function."""
        return self.fn(*args, **kwargs)


@F
def identity(x):
    """Return its argument"""
    return x


@F
def const(x, *args, **kwargs):
    """Return its first parameter, curried"""
    if not args and not kwargs:
        return F(lambda *args, **kwargs: const(x, *args, **kwargs))
    return x


@F
def succ(x):
    """Return x + 1"""
    return x + 1


@F
def pred(x):
    """Return x - 1"""
    return x - 1


@F
def map(fn, xs=None, gen=False):
    """Map a function to an iterable, curried
    if gen is True, it will try to coerce the returned generator into the input's type"""
    if xs is None:
        f = lambda xs: map(fn, xs, gen)
        f.__name__ = map.__name__
        f.__doc__ = map.__doc__
        return F(f)
    seq = builtins.map(fn, xs)
    try:
        return type(xs)(seq) if not gen else seq
    except:
        return stream.Stream(seq)


@F
def filter(fn, xs=None, gen=False):
    """Filter an iterable based on a function , curried
    if gen is False, it will try to coerce the returned generator into the input's type"""
    if xs is None:
        f = lambda xs: filter(fn, xs)
        f.__name__ = filter.__name__
        f.__doc__ = filter.__doc__
        return F(f)
    seq = builtins.filter(fn, xs)
    try:
        return type(xs)(seq) if not gen else seq
    except:
        return stream.Stream(seq)


@F
def reduce(fn, xs=None, initializer=None):
    """Fold a function on an iterable, curried"""
    if xs is None:
        f = lambda xs: reduce(fn, xs, initializer)
        f.__name__ = reduce.__name__
        f.__doc__ = reduce.__doc__
        return F(f)
    return functools.reduce(fn, xs, initializer)


@F
def flip(fn):
    """Swap the argument order of a function taking two parameters"""
    f = lambda x1, x2: fn(x2, x1)
    f.__name__ = flip.__name__
    f.__doc__ = flip.__doc__
    return F(f)


@F
def apply(fn, xs=None):
    """Apply fn to xs after unpacking it, curried"""
    if xs is None:
        f = lambda xs: fn(*xs)
        f.__name__ = apply.__name__
        f.__doc__ = apply.__doc__
        return F(f)
    return fn(xs)


@F
def compose(*args):
    """Compose n functions together"""
    return reduce(operator.add, args, identity)


@F
def curry2(fn):
    """Make a curried version of a function"""

    @F
    def wrapper(x, y=None):
        if y is None:
            return F(lambda y: fn(x, y))
        return fn(x, y)

    return wrapper


add = curry2(operator.add)
sub = curry2(operator.sub)
mul = curry2(operator.mul)
floordiv = curry2(operator.floordiv)
div = curry2(operator.truediv)
mod = curry2(operator.mod)
