"*args and **kwargs allow functions to accept a unknown number of arguments."
#example 1
'''
If you do not know how many arguments will be passed into your function, 
add a * before the parameter name.
This way, the function will receive a tuple of arguments and can access the items accordingly
'''
def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus") 

'''
The *args parameter allows a function to accept any number of positional arguments.

Inside the function, args becomes a tuple containing all the passed arguments 
'''
#example 2
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Emil", "Tobias", "Linus")
#example 3
def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")

#example 4
def my_function(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(my_function(1, 2, 3))
print(my_function(10, 20, 30, 40))
print(my_function(5))

#example 5
def my_function(**kid):
  print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")

#example 6
'''
The **kwargs parameter allows a function to accept any number of keyword arguments.

Inside the function, kwargs becomes a dictionary containing all the keyword argument
'''
def my_function(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function(name = "Tobias", age = 30, city = "Bergen")

#example 7
def my_function(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

my_function("emil123", age = 25, city = "Oslo", hobby = "coding")

#example 8
def my_function(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

my_function("User Info", "Emil", "Tobias", age = 25, city = "Oslo")