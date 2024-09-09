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
#     with open(f'Output/\/{file}', 'r') as data_extract:
#         for line in data_extract:
#             for s in substring:
#                 print(line)
#                 print(s)
#                 # if s in line:
#                 #     print("Good")
#                 # else:
#                 #     print("Not Good", file)
#
# # for f in os.listdir(path):
#     if os.path.isfile(f):
#         my_list.append(f)
#
# print(my_list)
