n = int(input())
def POwer(n):
    for i in range(n):
        yield 2**i

for num in POwer(n):
    print(num, end=" ")
