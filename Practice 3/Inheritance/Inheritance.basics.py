'''
Inheritance allows us to define a class that inherits all the methods and properties from another class.

Parent class is the class being inherited from, also called base class.

Child class is the class that inherits from another class, also called derived class.
'''
#example 1
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()

#example 2
class Student(Person):
  pass

#Use the pass keyword when you do not want to add any other properties or methods to the class.

#example 3
x = Student("Mike", "Olsen")
x.printname()

#example 4
class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.

#example 5
class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)

'''
The __init__() function is called automatically every time the class is being used to create a new object.
The child's __init__() function overrides the inheritance of the parent's __init__() function.