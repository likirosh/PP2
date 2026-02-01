#example 1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

#example 2
for x in "banana":
  print(x)

#example 3
for x in range(6):
  print(x)

#example 4
for x in range(6):
  print(x)
else:
  print("Finally finished!")

#example 5
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)

#example 6 (Pass statement to avoid error with FOR loop with no content )
for x in [0, 1, 2]:
  pass