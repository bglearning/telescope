# Telescope

Simple tool to look at your stars!

Currently, it only shows the language counts of the starred repos.

## Dependencies

- Python3
- The [requests](http://docs.python-requests.org/en/master/) library.
  
Install via pip for Python3:

```
pip install requests
```

## Usage

```
python3 telescope.py <username>
```

Example:
```
python3 telescope.py codingOtaku
```

Output:
```
Total starred repos: 107
Python       : 26
Java         : 13
JavaScript   : 10
HTML         : 5
Jupyter Notebook : 4
CSS          : 3
Ruby         : 3
C++          : 2
TeX          : 2
C            : 1
Groovy       : 1
Shell        : 1
Assembly     : 1
```

## TODO

- Use the [GraphQL API v4](https://developer.github.com/v4/) instead of the v3 `REST` API.
- ...
