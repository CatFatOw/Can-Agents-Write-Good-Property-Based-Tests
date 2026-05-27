SYSTEM_PROMPT = "You are a world class Python programmer."

PROPERTIES_PROMPT = """
Please review the following API documentation for {function_name}.
--------------------------- API Documentation ---------------------------
{api_documentation}
-------------------------------------------------------------------------
Extract a list of maximum five properties that you would use for property-based testing. Specifically, give properties on the output of the function, which may or may not depend on the input arguments.
Output in the following format:
1.
2.
3.
4.
5.
Do not write any tests. Only write this list of five properties in natural language.
"""

MUTANTS_PROMPT = """
Please review the following API documentation for {function_name}.
--------------------------- API Documentation ---------------------------
{api_documentation}
-------------------------------------------------------------------------
Here is a property of the {function_name} that we would like to test in a property-based test.
{prop}
Write five different buggy versions of {function_name} that have the same function signature. If the function signature includes
parameters with <no value> as a default value, replace the <no value> with None. Each function should call {function_name}
and modify the output to violate this property for all inputs. Strictly follow the output format below.
```python
def buggy_1(...):
  <buggy 2 code>
def buggy_2(...):
  <buggy 2 code>
(...)
```
"""

PBT_PROPERTIES_PROMPT = """
Now, write a Python property-based test suite using the library Hypothesis testing the properties you described. Strictly follow the output format described below when writing each test.
In your generation strategy, be aware of very large inputs and overflows.
--------------------------- Output Format ---------------------------
```python
from hypothesis import given, strategies as st
import {module_name}

@given(st.data())
def test_{function_name}_property():
    (...)
# End program
```
"""

OUTPUT_FORMAT_TEMPLATE = """
--------------------------- Example Output ---------------------------
```python
from hypothesis import given, strategies as st

@given(st.data())
def test_draw_sequentially(data):
    x = data.draw(integers())
    y = data.draw(integers(min_value=x))
    assert x < y
# End program
```
"""

PBT_PROMPT_TEMPLATE = """
Please review the following API documentation for {function_name}.
--------------------------- API Documentation ---------------------------
{api_documentation}
-------------------------------------------------------------------------
Use the Python library hypothesis to write a
single property test that generates random values for input parameter of {function_name}. First, explain a strategy to make your
your function generate a wide variety of inputs and edge cases. Then, explain which properties to check in the test based on the API documentation. Finally, output
one property test using your generation strategy and properties. Strictly follow the output format presented below.
--------------------------- Output Format ---------------------------
```python
from hypothesis import given, strategies as st

# Summary: Summary of the generation strategy
@given(st.data())
def test_{function_name}():
    (...)
# End program
```
"""
