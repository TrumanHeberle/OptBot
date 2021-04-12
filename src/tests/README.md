# Unit testing
**This directory should only contain code for performing unit testing on specific functions, classes, or modules.**


In order to run tests correctly, each file containing tests should define test
functions such that the function name begins with "test". Each test function
should utilize python assert statements to assess code. Multiple assertions can
be made per function. For example:


```python
def test_1():
    x = 10
    assert x==10
    y = 10
    assert x==y
```


Run tests by executing the python file "tests.py" in the "src" directory.
