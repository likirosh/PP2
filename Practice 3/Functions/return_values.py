#example 1
'''
Functions can send data back to the code that called them using the return statement.

When a function reaches a return statement, it stops executing and sends the result back
'''

def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

#example 2
def get_greeting():
  return "Hello from a function"

print(get_greeting())
"If a function doesn't have a return statement, it returns None by default."

#example 3
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)