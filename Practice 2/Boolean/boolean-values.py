#example 1
print(10 > 9)
print(10 == 9)
print(10 < 9)

#example 2
a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

##example 3
x = "Hello"
y = 15

print(bool(x))
print(bool(y))

""" 
Almost any value is evaluated to True if it has some sort of content.

Any string is True, except empty strings.

Any number is True, except 0.

Any list, tuple, set, and dictionary are True, except empty ones. 
"""

#example 4
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

"""
In fact, there are not many values that evaluate to False, except empty values, 
such as (), [], {}, "", the number 0, and the value None. 
And of course the value False evaluates to False.
One more value, or object in this case, evaluates to False, 
and that is if you have an object that is made from a 
class with a __len__ function that returns 0 or False
"""
#example 5
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})
