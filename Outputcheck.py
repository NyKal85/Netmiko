import os

substring = [

]

all_files = os.listdir('Output/')


def search_str(file_path, word):
    with open(f'Output/\/{file_path}', 'r') as file:
        content = file.read()
        if word in content:
            print('string in file')
        else:
            print(file_path, "String no in file")

for file in all_files:
    for line in substring:
        search_str(file, line)

