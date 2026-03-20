with open("example.txt", "w") as f:
    f.write("Dauren was here")

with open("example.txt", "r") as f:
    print(f.read())

with open("example.txt", "a") as f:
    f.write("Dauren bad guy")

with open("example.txt", "r") as f:
    print(f.read())    