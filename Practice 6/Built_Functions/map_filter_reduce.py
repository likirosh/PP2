#map
numbers=list(map(int, input().split()))
squarred=list(map(lambda x: x*2, numbers))

#filter
numbers = [-1,-4,-3,-5,1,2,6,7,10]
oddnum = list(filter(lambda x: x%2 != 0, numbers))
pos=list(filter(lambda x: x > 0, numbers))

#reduce
from functools import reduce
numbers = [1,2,3,4,5]
total = reduce(lambda acc, x: acc+x, numbers)
print(total)

#all in one
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

result = reduce(
    lambda acc, x: acc + x,         
    filter(lambda x: x % 2 == 0,     
    map(lambda x: x ** 2, numbers))  
)

print(result)