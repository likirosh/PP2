#example 1
class Computer:
  def __init__(self):
    self.cpu = self.CPU()
    self.ram = self.RAM()

  class CPU:
    def process(self):
      print("Processing data...")

  class RAM:
    def store(self):
      print("Storing data...")

computer = Computer()
computer.cpu.process()
computer.ram.store()

#example 2
class Father:
    def skills(self):
        print("Father: Driving")

class Mother:
    def skills(self):
        print("Mother: Cooking")

class Child(Father, Mother):
    pass

c = Child()
c.skills()

#example 3
class Father:
    def work(self):
        print("Father works as engineer")

class Mother:
    def work(self):
        print("Mother works as teacher")

class Child(Father, Mother):
    def work(self):
        print("Child is a student")

c = Child()
c.work()
