#example 1
class Animal:
    def sound(self):
        print("Animal makes a sound")

class Cow(Animal):
    def sound(self):   # overriding
        print("Cow moos")

c = Cow()
c.sound()


#example 2
class Vehicle:
    def move(self):
        print("Vehicle is moving")

class Car(Vehicle):
    def move(self):   # overridden method
        print("Car is driving")

c = Car()
c.move()

#example 3
class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    def greet(self):
        super().greet()   # calls parent method
        print("I am a student")

s = Student()
s.greet()
