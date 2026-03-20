class Counter:
    def __init__(self, limit, starter):
        self.limit = limit
        self.current = starter

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == self.limit:
            raise StopIteration
        self.current += 1
        return self.current

a = int(input())
b = int(input())


for num in Counter(b, a):
    print(num)