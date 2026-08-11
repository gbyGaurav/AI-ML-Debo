# Python Standard Library Cheatsheet
### `random` · `sys` · `os` · `math`

---

## 🎲 `random`
Pseudo-random number generation.

```python
import random
```

| Function | Description | Example |
|---|---|---|
| `random.random()` | Float in `[0.0, 1.0)` | `0.374...` |
| `random.uniform(a, b)` | Float in `[a, b]` | `random.uniform(1, 10)` |
| `random.randint(a, b)` | Int in `[a, b]` (inclusive) | `random.randint(1, 6)` |
| `random.randrange(start, stop, step)` | Int from range, exclusive stop | `random.randrange(0, 10, 2)` |
| `random.choice(seq)` | One random element from sequence | `random.choice(['a','b','c'])` |
| `random.choices(seq, k=n)` | `n` elements, **with** replacement | `random.choices([1,2,3], k=5)` |
| `random.sample(seq, k=n)` | `n` elements, **without** replacement | `random.sample(range(100), 5)` |
| `random.shuffle(list)` | Shuffle a list **in place** | `random.shuffle(my_list)` |
| `random.seed(n)` | Seed the generator (reproducibility) | `random.seed(42)` |
| `random.gauss(mu, sigma)` | Gaussian/normal distribution | `random.gauss(0, 1)` |
| `random.getstate()` / `setstate(s)` | Save/restore RNG internal state | — |

**Common patterns**
```python
random.seed(42)                      # reproducible results
random.choice(['heads', 'tails'])    # coin flip
random.sample(deck, 5)               # deal 5 unique cards
random.shuffle(deck)                 # shuffle in place
```

---

## ⚙️ `sys`
Interpreter- and runtime-level access.

```python
import sys
```

| Function / Attribute | Description | Example |
|---|---|---|
| `sys.argv` | List of command-line arguments | `sys.argv[1]` |
| `sys.exit([code])` | Exit the program | `sys.exit(0)` |
| `sys.version` | Python version string | `'3.12.0 ...'` |
| `sys.version_info` | Version as a tuple | `(3, 12, 0, 'final', 0)` |
| `sys.platform` | OS platform identifier | `'linux'`, `'win32'`, `'darwin'` |
| `sys.path` | Module search path (list, mutable) | `sys.path.append('/my/dir')` |
| `sys.modules` | Dict of loaded modules | `'os' in sys.modules` |
| `sys.stdin` / `stdout` / `stderr` | Standard I/O streams | `sys.stderr.write('err\n')` |
| `sys.getsizeof(obj)` | Size of object in bytes | `sys.getsizeof([1,2,3])` |
| `sys.maxsize` | Max value of a native int (platform) | `9223372036854775807` |
| `sys.setrecursionlimit(n)` | Set max recursion depth | `sys.setrecursionlimit(3000)` |
| `sys.getrecursionlimit()` | Get current recursion limit | — |
| `sys.exc_info()` | Info on the current exception | used inside `except` blocks |

**Common patterns**
```python
if len(sys.argv) < 2:
    print("Usage: script.py <arg>")
    sys.exit(1)

print("Error!", file=sys.stderr)
```

---

## 🗂️ `os`
Operating-system interfaces: files, directories, environment, processes.

```python
import os
```

### Paths & directories
| Function | Description |
|---|---|
| `os.getcwd()` | Get current working directory |
| `os.chdir(path)` | Change current directory |
| `os.listdir(path='.')` | List directory contents |
| `os.mkdir(path)` | Create a single directory |
| `os.makedirs(path)` | Create nested directories |
| `os.rmdir(path)` | Remove an empty directory |
| `os.removedirs(path)` | Remove nested empty directories |
| `os.rename(src, dst)` | Rename/move a file or directory |
| `os.remove(path)` | Delete a file |
| `os.walk(path)` | Recursively yield `(root, dirs, files)` |

### `os.path` submodule
| Function | Description |
|---|---|
| `os.path.join(a, b)` | Join path components |
| `os.path.exists(path)` | Check if path exists |
| `os.path.isfile(path)` | Check if it's a file |
| `os.path.isdir(path)` | Check if it's a directory |
| `os.path.abspath(path)` | Absolute path |
| `os.path.basename(path)` | Final component (filename) |
| `os.path.dirname(path)` | Directory portion |
| `os.path.splitext(path)` | `(root, ext)` tuple |
| `os.path.getsize(path)` | File size in bytes |

### Environment & process
| Function | Description |
|---|---|
| `os.environ` | Dict of environment variables |
| `os.getenv('VAR', default)` | Get env variable safely |
| `os.putenv(k, v)` / `os.environ['k']=v` | Set env variable |
| `os.getpid()` | Current process ID |
| `os.system(cmd)` | Run a shell command |
| `os.name` | OS type: `'posix'`, `'nt'`, etc. |
| `os.sep` | Path separator (`'/'` or `'\\'`) |

**Common patterns**
```python
for root, dirs, files in os.walk('.'):
    for f in files:
        print(os.path.join(root, f))

api_key = os.getenv('API_KEY', 'default_value')
os.makedirs('data/output', exist_ok=True)
```

---

## 📐 `math`
Mathematical functions on floats (see also `cmath` for complex numbers).

```python
import math
```

### Constants
| Constant | Value |
|---|---|
| `math.pi` | `3.14159...` |
| `math.e` | `2.71828...` |
| `math.tau` | `2π` |
| `math.inf` | Infinity |
| `math.nan` | Not-a-number |

### Power, log & roots
| Function | Description |
|---|---|
| `math.sqrt(x)` | Square root |
| `math.pow(x, y)` | `x ** y` as float |
| `math.exp(x)` | `e ** x` |
| `math.log(x, base=e)` | Logarithm |
| `math.log2(x)` / `math.log10(x)` | Log base 2 / base 10 |
| `math.isqrt(n)` | Integer square root |

### Rounding & rendering
| Function | Description |
|---|---|
| `math.ceil(x)` | Round up |
| `math.floor(x)` | Round down |
| `math.trunc(x)` | Truncate toward 0 |
| `math.fabs(x)` | Absolute value (float) |
| `math.copysign(x, y)` | Magnitude of x, sign of y |
| `math.fmod(x, y)` | Floating-point remainder |

### Trigonometry
| Function | Description |
|---|---|
| `math.sin/cos/tan(x)` | Standard trig (radians) |
| `math.asin/acos/atan(x)` | Inverse trig |
| `math.atan2(y, x)` | Angle of point (y, x) |
| `math.degrees(x)` / `math.radians(x)` | Convert between units |
| `math.hypot(x, y)` | `sqrt(x² + y²)` |

### Combinatorics & special
| Function | Description |
|---|---|
| `math.factorial(n)` | `n!` |
| `math.gcd(a, b)` | Greatest common divisor |
| `math.lcm(a, b)` | Least common multiple (3.9+) |
| `math.comb(n, k)` | Combinations `nCk` |
| `math.perm(n, k)` | Permutations `nPk` |
| `math.isclose(a, b)` | Compare floats safely |
| `math.isnan(x)` / `math.isinf(x)` | Check special values |

**Common patterns**
```python
math.isclose(0.1 + 0.2, 0.3)     # True — safe float comparison
math.comb(10, 3)                 # 120 — combinations
distance = math.hypot(dx, dy)    # Euclidean distance
```

---

### Quick reference: import styles
```python
import random, sys, os, math          # standard
from math import sqrt, pi             # import specific names
import os.path as op                  # alias submodule
```