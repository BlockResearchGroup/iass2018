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

==================== ======================================== ============================================
Built-in types                                                      
==================== ======================================== ============================================
numeric types        :obj:`int`, :obj:`float`, :obj:`complex` ``int(1)``, ``float(1)``, ``complex(1)``       
sequence types       :obj:`list`, :obj:`tuple`, :obj:`range`  ``[0, 1]``, ``(0, 1)``, ``range(2)``           
text sequence types  :obj:`str`                               ``'hello'``                                
set types            :obj:`set`, :obj:`frozenset`             ``set([0, 1, 2])``, ``frozenset([0, 1, 2])`` 
mapping types        :obj:`dict`                              ``dict(zero=0, one=1)``                    
==================== ======================================== ============================================


Containers
==========

* https://docs.python.org/3/tutorial/datastructures.html
* https://docs.python.org/3/library/collections.html
* https://docs.python.org/3/library/collections.abc.html

============ ================================ ================================================================== ===============================
type         example                          description                                                        operations                    
============ ================================ ================================================================== ===============================
:obj:`list`   ``[1, 2, 3]``                   Contains ordered, arbitrary objects                                iterate, slide, index, modify 
:obj:`tuple`  ``(1, 2, 3)``                   Contains ordered, arbitrary objects, but cannot be changed.        iterate, index, slice         
:obj:`set`    ``set([1, 2, 3])``              Contains unordered, distinct, hashable objects.                    iterate, modify               
:obj:`dict`   ``dict(one=1, two=2, three=3)`` Maps unordered, distinct, hashable objects to arbitrary objects.   iterate, modify               
============ ================================ ================================================================== ===============================


**list**

.. code-block:: python
    
    l = [0, '1', [2], (3, ), dict(four=4)]

**tuple**

.. code-block:: python

    t = (0, '1', [2], (3, ), dict(four=4))

.. code-block:: python

    a = 1
    b = 2

    a, b = b, a

**set**

.. code-block:: python

    s = set([1, 1, 2, 3, 3, 4])  # set([1, 2, 3, 4])


Comprehenions
=============

**list comprehension**

**dict comprehension**


Standard packages
=================

* link to the standard library

.. code-block:: python

    import sys
    import os
    import math
    import json
    import ast
    import random
    import ctypes
    import copy

    # and many more

.. code-block:: python

    from math import sqrt
    from math import cos, sin


Third-party packages
====================

.. code-block:: python

    import numpy
    import scipy
    import pandas
    import matplotlib
    import networkx
    import sympy
    import PySide
    import PyOpenGL
    import PyCuda


Exercises
=========

*Interactive notebook with solutions is available in the IASS 2018 repo*

1. Use ``range`` to create a list of even numbers between 0 and 10.
2. Use ``range`` to create a list of uneven numbers between 0 and 10.
3. Use ``zip`` to transpose ``rows = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]`` into columns.
4. Use ``sorted`` to sort ``tutors = zip(names, years)`` by their age.

5. Use ``random`` to create two lists with each 50 random numbers between 0 and 100.
   Use ``set`` to find the elements that appear in both lists, and to find the numbers between 0 and 100 that are in neither.
