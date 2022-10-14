from curses.ascii import isalpha
from sys import argv

def main():  
  switch = {
    "-t": truthtable,
    "-e": equivalent,
    "-m": minterms,
    "-M": maxterms,
    "-h": print_help }
  
  if (len(argv)) >= 2:
    switch[argv[1]]()
  else:
    print("(1) Truth Table")
    print("(2) Equivalence")
    print("(3) Minterms")
    print("(4) Maxterms")
    
    print("Please pick an option (1-4):", end=" ")
    
    try:  
      choice = int(input());
    except ValueError:
      print("Invalid choice, exiting...")
      return
    
    switch2 = {
      1: "-t",
      2: "-e",
      3: "-m",
      4: "-M"
    }
    
    if choice in switch2.keys():
      switch[switch2[choice]]()
    else:
      print("invalid choice, exiting...")

def truthtable():
  expression = str()
  operands = dict()
  
  if (len(argv) < 3):
    print("Enter boolean expression: ", end = "")
    expression = input()
  else:
    expression = argv[2]

  for c in expression:
    if isalpha(c):
      if c not in operands:
        operands[c] = 0;
  
  print(f"\nExpression: {expression}", end="\n\n")
  
  max_combo = 1 << len(operands)
  sortedOperands = sorted(operands.keys())
  postfix = infixToPostfix(expression)
  
  for operand in sortedOperands:
    print(operand, end=" ")
  print("| RESULT")
  print("=="*(len(operands)+4))
  
  for i in range(max_combo):    
    for j in range(len(sortedOperands)):
      operands[sortedOperands[len(sortedOperands) - j - 1]] = (i >> j) & 1
    
    for operand in sortedOperands:
      print(operands[operand], end=" ")
    
    print("|", evaluate(operands, postfix))
    
def equivalent():
  exp1 = str();
  exp2 = str();
  
  if (len(argv) <= 2):
    print("\nBoolean expression 1:", end=" ")
    exp1 = input()
    print("Boolean expression 2:", end=" ")
    exp2 = input()
  elif(len(argv) == 3):
    exp1 = argv[2]
    print(f"\nBoolean expression 1: {exp1}")
    print("Boolean expression 2:", end=" ")
    exp2 = input()
  else:
    exp1 = argv[2]
    exp2 = argv[3]
    print(f"\nBoolean expression 1: {exp1}")
    print(f"Boolean expression 2: {exp2}")
  
  print()
  
  expression = exp1 + "=" + exp2
  operands = dict()

  for c in expression:
    if isalpha(c):
      if c not in operands:
        operands[c] = 0;

  max_combo = 1 << len(operands)
  sortedOperands = sorted(operands.keys())
  postfix = infixToPostfix(expression)
  
  for i in range(max_combo):
    for j in range(len(sortedOperands)):
      operands[sortedOperands[len(sortedOperands) - j - 1]] = (i >> j) & 1
      
    if (evaluate(operands, postfix) == 0):
      print(f"[-] Expression {exp1} and {exp2} are not equivalent.")
      return;
  
  print(f"[+] Expression {exp1} and {exp2} are equivalent.")
  
def minterms():
  expression = str()
  operands = dict()
  
  if (len(argv) == 3):
    expression = argv[2]
    print(f"\nExpression: {expression}\n")
  else:
    print("\nExpression:", end=" ")
    expression = input()
  
  for c in expression:
    if isalpha(c):
      if c not in operands:
        operands[c] = 0;
  
  max_combo = 1 << len(operands)
  sortedOperands = sorted(operands.keys())
  postfix = infixToPostfix(expression)
  
  print("Sum:m(", end="")
  
  first = True
  for i in range(max_combo):
    for j in range(len(sortedOperands)):
      operands[sortedOperands[len(sortedOperands) - j - 1]] = (i >> j) & 1
    
    if (evaluate(operands, postfix) == 1):
      if (first):
        print(i, end=(""))
        first = False
      else:
        print(",", i, end="")
  print(")")
      
def maxterms():
  expression = str()
  operands = dict()
  
  if (len(argv) == 3):
    expression = argv[2]
    print(f"\nExpression: {expression}\n")
  else:
    print("\nExpression:", end=" ")
    expression = input()
  
  for c in expression:
    if isalpha(c):
      if c not in operands:
        operands[c] = 0;
  
  max_combo = 1 << len(operands)
  sortedOperands = sorted(operands.keys())
  postfix = infixToPostfix(expression)
  
  first = True
  print("Product:M(", end="")
  
  for i in range(max_combo):
    for j in range(len(sortedOperands)):
      operands[sortedOperands[len(sortedOperands) - j - 1]] = (i >> j) & 1
    
    if (evaluate(operands, postfix) == 0):
      if (first):
        print(i, end=(""))
        first = False
      else:
        print(",", i, end="")
  print(")")
  
def print_help():
  print("Options:")
  print("  -t    generate truth table for an expression")
  print("  -e    check if two expressions are equivalent")
  print("  -m    generate minterms of an expression")
  print("  -M    generate maxterms of an expression")
  print("  -h    show this help text")

def infixToPostfix(expression: str) -> str:
  operators = []
  postfix = str()

  for i in range(len(expression)):
    c = expression[i]
    
    if isalpha(c):
      postfix += c
      if (i > 0 and (isalpha(expression[i - 1]) or expression[i - 1] in ")\'")):
        operators.append('*')
    
    elif c in "+*()'^=":
      if (c == '('):
        operators.append(c)
      
      elif (c == '+'):
        if (len(operators) > 0 and operators[len(operators) - 1] in "+*^="):
          postfix += operators.pop()
        operators.append(c)
      
      elif (c == '*'):
        if (len(operators) > 0 and operators[len(operators) - 1] in "*^="):
          postfix += operators.pop()
        operators.append(c)
        
      elif c in "^=":
        if (len(operators) > 0 and operators[len(operators) - 1] in "^="):
          postfix += operators.pop()
        operators.append(c)
        
      elif (c == '\''):
        postfix += c
      else: # c = ')'
        while(len(operators) > 0 and operators[len(operators) - 1] != '('):
          postfix += operators.pop()
        operators.pop()

  while(len(operators) > 0):
    if (operators[len(operators) - 1] != '('):
      postfix += operators.pop()
    else:
      operators.pop()
    
  return postfix

def evaluate(operands: dict, postfix: str) -> int:  
  values = []
    
  for c in postfix:
    if c in "*+^=":
      b = values.pop()
      a = values.pop()
      
      if (c == '*'):   values.append(a & b)
      elif (c == '+'): values.append(a | b)
      elif (c == '^'): values.append((a ^ b) & 1)
      elif (c == '='): values.append(~(a ^ b) & 1)
    elif (c == '\''):
      values.append(~values.pop() & 1)
    else:
      values.append(operands[c])
      
  return values.pop()

if __name__ == "__main__":
  main()