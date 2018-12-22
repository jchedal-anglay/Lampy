class F:
    def __init__(self, fn):
        self.fn = fn
        self.__name__ = fn.__name__
        self.__doc__ = fn.__doc__

    def __rrshift__(self, other):
        """Function piping: x >> f -> f(x)."""
        return self(other)

    def __add__(self, other):
        """Function composition: (f + g + h)(x) -> f(g(h(x)))."""
        f = lambda *args, **kwargs: self(other(*args, **kwargs))
        f.__name__ = 'compose<{}><{}>'.format(self.__name__, other.__name__)
        f.__doc__ = 'Composed function.'
        return F(f)

    def __pow__(self, other):
        """Function pairing: (f ** g)(1, 2) -> (f(1), g(2))."""
        f = lambda x1, x2: (self(x1), other(x2))
        f.__name__ = 'pair<{}><{}>'.format(self.__name__, other.__name__)
        f.__doc__ = 'Paired function.'
        return F(f)

    def __call__(self, *args, **kwargs):
        """Evaluates the wrapped function."""
        return self.fn(*args, **kwargs)


@F
def identity(x):
    return x

@F
def const(x, *args, **kwargs):
    if not args and not kwargs:
        return F(lambda *args, **kwargs: const(x, *args, **kwargs))
    return x

@F
def succ(x):
    return x + 1

@F
def pred(x):
    return x - 1


@F
def map(fn, xs=None, gen=False):
    if xs is None:
        f = lambda xs: map(fn, xs, gen)
        f.__name__ = 'map'
        f.__doc__ = 'Curried version of map.'
        return F(f)
    seq = (fn(x) for x in xs)
    try:
        return type(xs)(seq) if not gen else seq
    except:
        return seq

@F
def filter(fn, xs=None, gen=False):
    if xs is None:
        f = lambda xs: filter(fn, xs)
        f.__name__ = 'filter'
        f.__doc__ = 'Curried version of filter.'
        return F(f)
    seq = (x for x in xs if fn(x))
    try:
        return type(xs)(seq) if not gen else seq
    except:
        return seq

@F
def reduce(fn, xs=None, initializer=None):
    if xs is None:
        f = lambda xs: reduce(fn, xs, initializer)
        f.__name__ = 'reduce'
        f.__doc__ = 'Curried version of reduce.'
        return F(f)
    it = iter(xs)
    acc = next(it) if initializer is None else initializer
    for element in it:
        acc = fn(acc, element)
    return acc

@F
def flip(fn):
    f = lambda x1, x2: fn(x2, x1)
    f.__name__ = 'flip<{}>'.format(fn.__name__)
    f.__doc__ = fn.__doc__
    return F(f)

@F
def apply(fn, xs=None):
    if xs is None:
        f = lambda xs: fn(*xs)
        f.__name__ = 'apply<{}>'.format(fn.__name__)
        f.__doc__ = fn.__doc__
        return F(f)
    return fn(xs)

@F
def compose(*args):
    return reduce(add, args, identity)

@F
def eq(x, y=None):
    if y is None:
        return F(lambda y: eq(x, y))
    return x == y

@F
def add(x, y=None):
    if y is None:
        return F(lambda y: add(x, y))
    return x + y

@F
def sub(x, y=None):
    if y is None:
        return F(lambda y: sub(x, y))
    return x - y

@F
def mul(x, y=None):
    if y is None:
        return F(lambda y: mul(x, y))
    return x * y

@F
def div(x, y=None):
    if y is None:
        return F(lambda y: div(x, y))
    return x / y

@F
def truediv(x, y=None):
    if y is None:
        return F(lambda y: truediv(x, y))
    return x // y

@F
def mod(x, y=None):
    if y is None:
        return F(lambda y: mod(x, y))
    return x % y


# Wrapped builtins
abs = F(abs)
all = F(all)
any = F(any)
ascii = F(ascii)
bin = F(bin)
bool = F(bool)
bytearray = F(bytearray)
bytes = F(bytes)
callable = F(callable)
chr = F(chr)
classmethod = F(classmethod)
compile = F(compile)
complex = F(complex)
delattr = F(delattr)
dict = F(dict)
dir = F(dir)
divmod = F(divmod)
enumerate = F(enumerate)
eval = F(eval)
float = F(float)
format = F(format)
frozenset = F(frozenset)
getattr = F(getattr)
globals = F(globals)
hasattr = F(hasattr)
hash = F(hash)
hex = F(hex)
id = F(id)
input = F(input)
int = F(int)
isinstance = F(isinstance)
issubclass = F(issubclass)
iter = F(iter)
len = F(len)
list = F(list)
locals = F(locals)
max = F(max)
memoryview = F(memoryview)
min = F(min)
next = F(next)
object = F(object)
oct = F(oct)
open = F(open)
ord = F(ord)
pow = F(pow)
print = F(print)
property = F(property)
range = F(range)
repr = F(repr)
reversed = F(reversed)
round = F(round)
set = F(set)
setattr = F(setattr)
slice = F(slice)
sorted = F(sorted)
staticmethod = F(staticmethod)
str = F(str)
sum = F(sum)
tuple = F(tuple)
type = F(type)
vars = F(vars)
zip = F(zip)
