#example 1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

#example 2
for i in range(9):
  if i == 3:
    continue
  print(i)

#example 3
i = 0
while i < 9:
  i += 1
  if i == 3:
    continue
  print(i)