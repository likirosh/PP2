import shutil
import os
shutil.copy2('example.txt', 'backup.txt')

with open('backup.txt', 'r') as f:
    content = f.read()
    print("File contents:")
    print(content)

os.remove('backup.txt')