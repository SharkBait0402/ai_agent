from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

print("Result for current directory")
print(get_file_content("calculator", "main.py"), "\n\n")

print("Result for \'pkg\' directory")
print(get_file_content("calculator", "pkg/calculator.py"), "\n\n")

print("Result for \'/bin\' directory")
print(get_file_content("calculator", "/bin/cat"), "\n\n")

print("Result for \'../\' directory")
print(get_file_content("calculator", "pkg/does_not_exist.py"), "\n\n")
