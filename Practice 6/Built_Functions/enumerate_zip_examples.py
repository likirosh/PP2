#enumerate
fruits = ["apple", "orange", "banana"]
for i, fruit in enumerate(fruits, start=1)
print(i, fruit)

#zip
names  = ['Alice', 'Bob', 'Charlie']
grades = [95, 87, 92]

for name, grade in zip(names, grades):
    print(f"{name} {score}")


#Type check and conversation
x = 42
name = "Alice"
items = [1, 2, 3]

print(type(x))       
print(type(name))     
print(type(items))    

print(isinstance(x, int))        
print(isinstance(name, str))     
print(isinstance(items, list))

#Conversation
print(int("42"))      
print(int(3.99))      
print(int(True))     
print(int(False))     

print(float("3.14"))   
print(float(42))       
print(float("inf"))   

print(str(42))        
print(str(3.14))     
print(str(True))