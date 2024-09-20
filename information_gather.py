from device_list import switches, ecos
from netmiko import ConnectHandler, NetmikoTimeoutException
from datetime import datetime
from pathlib import Path
import threading
import time
import os

command_list = ""


def commands(ssh_conn, command_to_run):
    try:
        conn = ConnectHandler(**ssh_conn)
    except NetmikoTimeoutException:
        print(f"Unable to connect to {ssh_conn['host']} please check you data of the switch config manually")
    else:
        conn.enable()
        data = conn.send_command(command_to_run, read_timeout=30)


        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        prompt = conn.find_prompt()
        hostname = prompt[0:-1]
        directory = 'C:/Users\mcaudle\PycharmProjects/Netmiko\Output'
        filename = f'{hostname}_{year}-{month}-{day}.txt'
        folder_name = f'{command_to_run}'.strip()
        path = os.path.join(directory, folder_name)

        if not os.path.exists(path):
            os.makedirs(path)
        with open(f'{path}/{filename}', mode="w") as data_extract:
            data_extract.write(data)
            print(f'{hostname} commands completed successfully')
            print('#' * 30)


done = False

while done is False:
    needed_info = input("What command do you want to run? ")
    start = time.time()

    threads = list()
    for key, values in switches.items():
        connection_dict = values
        th = threading.Thread(target=commands, args=(connection_dict, needed_info))
        threads.append(th)

    for th in threads:
        th.start()

    for th in threads:
        th.join()

    end = time.time()

    print(f'Total execution time:{end - start}')

    more_commands = input("Are there more commands you need to run? Y/N").lower()

    if more_commands == "y":
        done = False

    elif more_commands == "n":
        done = True

    else:
        print("Invalid Entry try again!")
        done = False
