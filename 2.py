n = int(input())
def Fib(n):
    a = 0
    b = 0
    for _ in range(n):
        yield a, b = b, a+b 

for num in FIb(n):
    print(num, " ")       

