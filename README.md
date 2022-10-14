# Boolean Algebra Script
This simple Python script can perform operations like generating minterms, generating maxterms, generating ruth tables, and checking expressions for equivalence on a boolean expression with up to 52 possible operands (26 lower-case and 26 upper-case letters).

## Operations

Symbol | Operation
--|--
\* | AND
\+ | OR
^ | XOR
= | equivalence operator aka XNOR
( | opening parenthesis for grouping operations
) | closing parenthesis for grouping operations

Additionally two operands or groups that are adjacent will be evaluated to be an AND operation like this:

Expression: | Evaluated as:
--|--
ab         | a*b
(a+b)c     | (a+b)*c
(a+b)(c+d) | (a+b)*(c+d)

## Running
In your terminal of choice, navigate to the directory `boolean-algebra.py` is in and run:
```bash
# option, expression-1, and expression-2 are optional parameters
python boolean-algebra.py ?[option] ?[expression-1] ??[expression-2]
```
- If no option is specified, the script will print out menu options instead.
- If an option is specified but no expressions are given, the script will prompt you for boolean expression(s).

## Options
```bash
-t   # generate truth table for a boolean expression.
-e   # check if two boolean expressions are equivalent
-m   # generate shorthand minterm expansion
-M   # generate shorthand maxterm expansion
-h   # print helper text
```
**Example: generate truth table for expression `A+B^C`**
```
$ python boolean-algebra.py -t "A+B^C"

