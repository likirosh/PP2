#A Class is like an object constructor, or a "blueprint" for creating objects.
#example 1
class MyClass:
  x = 5

#example 2
p1 = MyClass()
print(p1.x)

#example 3
del p1

#example 4
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)

#example 5
class Person:
  pass

'''
class definitions cannot be empty, 
but if you for some reason have a class definition with no content, 
put in the pass statement to avoid getting an error.
'''
class Person()