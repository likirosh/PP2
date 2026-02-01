#example 1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

#example 2
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

#example 3
for i in range(9):
  if i > 3:
    break
  print(i)

#example 4
i = 1
while i < 9:
  print(i)
  if i == 3:
    break
  i += 1