# Python 101

## Built-in functions

* https://docs.python.org/3/library/functions.html

**range**

```python

range(0, 10, 1)  # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

```

**zip**

```python

names = ['Tomas', 'Tom', 'Juney']
years = ['81', '80', '84']

zip(names, years)  # [('Tomas', '81'), ('Tom', '80'), ('Juney', '84')]

```

**map**

```python

numbers = map(str, range(100))

```

**sorted**

```python

sorted(numbers)
sorted(numbers, key=int)

```

## Built-in types

* https://docs.python.org/3/library/stdtypes.html


| Built-in types      |                           |                                          |
|:--------------------|:--------------------------|:-----------------------------------------|
| numeric types       | `int`, `float`, `complex` | `int(1)`, `float(1)`, `complex(1)`       | 
| sequence types      | `list`, `tuple`, `range`  | `[0, 1]`, `(0, 1)`, `range(2)`           | 
| text sequence types | `str`                     | `'hello'`                                | 
| set types           | `set`, `frozenset`        | `set([0, 1, 2])`, `frozenset([0, 1, 2])` | 
| mapping types       | `dict`                    | `dict(zero=0, one=1)`                    |


Containers
==========

* https://docs.python.org/3/tutorial/datastructures.html
* https://docs.python.org/3/library/collections.html
* https://docs.python.org/3/library/collections.abc.html

| type    | example                       | description                                                      | operations                    |
|:--------|:------------------------------|:-----------------------------------------------------------------|:------------------------------|
| `list`  | `[1, 2, 3]`                   | Contains ordered, arbitrary objects                              | iterate, slide, index, modify |
| `tuple` | `(1, 2, 3)`                   | Contains ordered, arbitrary objects, but cannot be changed.      | iterate, index, slice         |
| `set`   | `set([1, 2, 3])`              | Contains unordered, distinct, hashable objects.                  | iterate, modify               |
| `dict`  | `dict(one=1, two=2, three=3)` | Maps unordered, distinct, hashable objects to arbitrary objects. | iterate, modify               |


**list**

```python
    
l = [0, '1', [2], (3, ), dict(four=4)]

```

**tuple**

```python

t = (0, '1', [2], (3, ), dict(four=4))

```

```python

a = 1
b = 2

a, b = b, a

```

**set**

```python

s = set([1, 1, 2, 3, 3, 4])  # set([1, 2, 3, 4])

```

Comprehenions
=============

**list comprehension**

```python

even  = [i for i in range(10) if i % 2 == 0]
odd   = [i for i in range(10) if i % 2]
mixed = [i if i % 2 else None for i in range(10)]

numbers = [str(i) for i  in range(100)]

rows = [range(1, 4) for i in range(3)]
flat = [item for row in rows for item in row]

```

**dict comprehension**

```python

lookup = {name: year for name, year in zip(names, years)}

```

Packages
========

**standard library**

```python

import sys
import os
import math
import random

# and many more

```

```python

from math import sqrt
from math import cos, sin

```

**thrird-party**

```python

import numpy
import scipy

# and many many more

```

```python

import compas
import compas_rhino
import compas_tna

from compas.datastructures import Mesh

```

Exercises
=========

1. Use `range` to create a list of even numbers between 0 and 10.
2. Use `range` to create a list of uneven numbers between 0 and 10.
3. Use `zip` to transpose `rows = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]` into columns.
4. Use `sorted` to sort `tutors = zip(names, years)` by their age.

5. Use `random` to create two lists with each 50 random numbers between 0 and 100.
   Use `set` to find the elements that appear in both lists, and to find the numbers between 0 and 100 that are in neither.
