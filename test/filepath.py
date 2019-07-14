import os

dirname = os.path.dirname(__file__)
sub_dir = os.path.join(dirname, "subfolder1")
sub_file_path = os.path.join(sub_dir, "subfile1.txt")

file_object = open(sub_file_path, 'r')

contents = file_object.readline()

file_object.close()

print("File contents are: " + contents)