import shutil
import os
os.makedirs('project/src/utils', exist_ok=True)
os.makedirs('project/src/models', exist_ok=True)
os.makedirs('project/tests', exist_ok=True)

entries = os.listdir('project')
print("Contents of project/:", entries)

#Find files by extension
for path in ['project/src/main.py', 'project/src/utils/helper.py',
             'project/docs/readme.txt', 'project/docs/notes.txt',
             'project/tests/test_main.py']:
    with open(path, 'w') as f:
        f.write("sample content")

def find_by_extension(root_dir, extension):
    matches = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extension):
                matches.append(os.path.join(root, file))
    return matches

py_files  = find_by_extension('project', '.py')
txt_files = find_by_extension('project', '.txt')

print("Python files:", py_files)
print("Text files:  ", txt_files)