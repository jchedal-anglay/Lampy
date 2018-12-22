class Function:
    def __init__(self, fn):
        self.fn = fn

    def __rrshift__(self, other):
        """Function piping: x >> f -> f(x)."""
        return self(other)

    def __add__(self, other):
        """Function composition: (f + g + h)(x) -> f(g(h(x)))."""
        return Function(lambda *args, **kwargs: self(other(*args, **kwargs)))

    def __pow__(self, other):
        """Function pairing: (f ** g)(1, 2) -> (f(1), g(2))."""
        return Function(lambda x1, x2: (self(x1), other(x2)))

    def __call__(self, *args, **kwargs):
        """Evaluates the wrapped function."""
        return self.fn(*args, **kwargs)


@Function
def identity(x):
    return x


@Function
def map(fn, xs=None, gen=False):
    if xs is None:
        return Function(lambda xs: map(fn, xs, gen))
    seq = (fn(x) for x in xs)
    try:
        return type(xs)(seq) if not gen else seq
    except:
        return seq


@Function
def filter(fn, xs=None):
    if xs is None:
        return Function(lambda xs: filter(fn, xs))
    seq = (x for x in xs if fn(x))
    try:
        return type(xs)(seq)
    except:
        return seq

@Function
def reduce(fn, xs=None, initializer=None):
    if xs is None:
        return Function(lambda xs: reduce(fn, xs, initializer))
    it = iter(xs)
    acc = next(it) if initializer is None else initializer
    for element in it:
        acc = fn(acc, element)
    return acc


@Function
def flip(fn):
    return Function(lambda x1, x2: fn(x2, x1))


@Function
def add(x, y=None):
    if y is None:
        return Function(lambda y: add(x, y))
    return x + y


@Function
def sub(x, y=None):
    if y is None:
        return Function(lambda y: sub(x, y))
    return x - y


@Function
def mul(x, y=None):
    if y is None:
        return Function(lambda y: mul(x, y))
    return x * y


@Function
def div(x, y=None):
    if y is None:
        return Function(lambda y: div(x, y))
    return x / y


@Function
def mod(x, y=None):
    if y is None:
        return Function(lambda y: mod(x, y))
    return x % y


# Wrapped builtins
abs = Function(abs)
all = Function(all)
any = Function(any)
ascii = Function(ascii)
bin = Function(bin)
bool = Function(bool)
bytearray = Function(bytearray)
bytes = Function(bytes)
callable = Function(callable)
chr = Function(chr)
classmethod = Function(classmethod)
compile = Function(compile)
complex = Function(complex)
delattr = Function(delattr)
dict = Function(dict)
dir = Function(dir)
divmod = Function(divmod)
enumerate = Function(enumerate)
eval = Function(eval)
float = Function(float)
format = Function(format)
frozenset = Function(frozenset)
getattr = Function(getattr)
globals = Function(globals)
hasattr = Function(hasattr)
hash = Function(hash)
help = Function(help)
hex = Function(hex)
id = Function(id)
input = Function(input)
int = Function(int)
isinstance = Function(isinstance)
issubclass = Function(issubclass)
iter = Function(iter)
len = Function(len)
list = Function(list)
locals = Function(locals)
max = Function(max)
memoryview = Function(memoryview)
min = Function(min)
next = Function(next)
object = Function(object)
oct = Function(oct)
open = Function(open)
ord = Function(ord)
pow = Function(pow)
print = Function(print)
property = Function(property)
range = Function(range)
repr = Function(repr)
reversed = Function(reversed)
round = Function(round)
set = Function(set)
setattr = Function(setattr)
slice = Function(slice)
sorted = Function(sorted)
staticmethod = Function(staticmethod)
str = Function(str)
sum = Function(sum)
tuple = Function(tuple)
type = Function(type)
vars = Function(vars)
zip = Function(zip)
