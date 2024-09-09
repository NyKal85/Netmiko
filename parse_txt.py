import os


all_files = os.listdir('Output/')

def data_parse(file_path):
    with open(f'Output/\/{file_path}', 'r') as file:
        while line := file.readline():
            if "vlan 25" in line:
                print("delete line")
            else:
                print(line)


for file in all_files:
    data_parse(file)