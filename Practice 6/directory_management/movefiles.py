# Copy a single file to another directory
shutil.copy2('project/docs/readme.txt', 'project/tests/readme.txt')

# Move a file to another directory
shutil.move('project/docs/notes.txt', 'project/src/notes.txt')


# Copy an entire directory tree
shutil.copytree('project/src', 'project/src_backup')


# Move an entire directory
shutil.move('project/src_backup', 'project/backup/src')
