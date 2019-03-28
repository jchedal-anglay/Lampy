```python
# This contains wrapped version of all builtin functions and some useful functions
from lampy import *

# Declaration
@F
def func(x, y, z):
  pass
  
# Manual wrapping
F(func)

# Composition using +
f = sum + map(succ) + range
print(f(10))  # 55

# Piping using >>
10 >> range >> map(succ) >> sum >> print  # 55

# Pairing using **
f = succ ** pred
print(f(0, 0))  # (1, -1)

# map and filter now try to coerce the returned sequence to their base type
print(map(succ, [1, 2, 3]))  # [2, 3, 4]
print(map(succ, (1, 2, 3)))  # (2, 3, 4)
print(map(succ, {1, 2, 3}))  # {2, 3, 4}
print(*map(succ, 3 >> range))  # generator, 2, 3, 4

# It is also possible to force the returned value to be a generator
print(map(succ, [1, 2, 3], gen=True))  # <generator object map.<locals>.<genexpr> at blablabla>

# map, filter and reduce are now curried functions
f = map(succ)
print(f([1, 2, 3]))  # [2, 3, 4]
# obviously, you can apply all the operators defined above to them
[1, 2, 3] >> f >> print  # [2, 3, 4]

# The builtin functions have been wrapped to support the piping, pairing and compose operators
[1, 2, 3] >> sum >> print  # 6

# The compose function also helps composing functions without using the operator, works even with unwrapped functions
from math import sqrt
print(compose(succ, sqrt)(10))  # 4.16227766016838

# Many other handy functions...
print(identity(5))  # returns its argument: 5
f = const(42)  # will always return 42, curried
10 >> f >> print  # 42

from math import pow
f = flip(pow)
print(f(3, 5), pow(5, 3))  # 125.0 125.0
```
