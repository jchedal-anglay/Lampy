import functools
import itertools


def inplace(f):
    def wrapper(self, *args, **kwargs):
        return f(self.copy(), *args, **kwargs)

    return wrapper


class Stream:
    """Lazy sequence, based on generators"""

    def __init__(self, iterator):
        self.iterator = iter(iterator)

    def __iter__(self):
        return self.iterator

    def __next__(self):
        return next(self.iterator)

    def next(self):
        """Yield the first element of the stream"""
        return next(self.iterator)

    @inplace
    def next_(self):
        return self.next()

    def peek(self):
        """Return the first element of the stream, keep original stream intact"""
        try:
            first = self.next()
        except StopIteration:
            return None
        self.iterator = iter(itertools.chain([first], self.iterator))
        return first

    def copy(self):
        """Return a copy of the stream, keep the original stream intact"""
        xs, ys = itertools.tee(self.iterator)
        self.iterator = iter(xs)
        return Stream(ys)

    def is_empty(self):
        """Return True if stream is empty, else otherwise"""
        try:
            first = self.next()
        except StopIteration:
            return True
        self.iterator = iter(itertools.chain([first], self.iterator))
        return False

    def push(self, x):
        """Push x at the beginning of stream"""
        self.iterator = iter(itertools.chain([x], self.iterator))
        return self

    @inplace
    def push_(self, x):
        return self.push(x)

    def drop(self):
        """Discard the first element and return the stream"""
        self.next()
        return self

    @inplace
    def drop_(self):
        return self.drop()

    def consume(self):
        """Force the evaluation of the stream, consume the stream"""
        for _ in self:
            pass

    @inplace
    def consume_(self):
        return self.consume()

    def take(self, n):
        """Return the prefix of length n of the stream"""
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n < 0:
            raise ValueError("n must be positive")
        return Stream(self.next() for _ in range(n))

    @inplace
    def take_(self, n):
        self.take(n)

    def skip(self, n):
        """Return the original stream with the prefix of length n removed"""
        self.take(n)
        return self

    @inplace
    def skip_(self, n):
        self.skip(n)

    def take_while(self, f):
        """Return a newly created stream in which remain only the first few
        elements e in self such that f(x)"""

        def _take_while():
            for e in self:
                if f(e):
                    yield e
                else:
                    break

        self.iterator = iter(_take_while())
        return self

    @inplace
    def take_while_(self, f):
        return self.take_while(f)

    def drop_while(self, f):
        """Return a new stream in which the first few elements such that f(x)
        have been dropped"""
        while True:
            if f(self.peek()):
                self.drop()
            else:
                break
        return self

    @inplace
    def drop_while_(self, f):
        return self.drop_while(f)

    def map(self, f):
        """Return a new stream with f mapped on each element"""
        self.iterator = iter(map(f, self.iterator))
        return self

    @inplace
    def map_(self, f):
        return self.map(f)

    def filter(self, f):
        """Return the stream filtered by f"""
        self.iterator = iter(filter(f, self.iterator))
        return self

    @inplace
    def filter_(self, f):
        return self.filter(f)

    def reduce(self, f, initializer=None):
        """Return the result of f folded on the stream"""
        return functools.reduce(f, self.iterator, initializer)

    @inplace
    def reduce_(self, f, initializer=None):
        return self.reduce(f, initializer=initializer)
