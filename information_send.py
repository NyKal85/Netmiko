from device_list import switches, ecos
from netmiko import ConnectHandler, NetmikoTimeoutException
from datetime import datetime
import threading
import time

# enter commands in commands_to_run.txt file with one command on each line.
with open('commands_to_run', 'r') as com:
    command_list = com.read().splitlines()

# give you time in seconds it took to complete at the end of the program
start = time.time()


def commands(data):
    # attempts to connect to device and enter privilege exec mode. If unable to connect it will print the error below.
    try:
        conn = ConnectHandler(**data)
    except NetmikoTimeoutException:
        print(f"Unable to connect to {data['host']} please check you data of the switch config manually")
    else:
        conn.enable()

        # Enters config mode and pushes commands to device and saves config
        conn.send_config_set()
        conn.send_config_set(command_list, read_timeout=20)
        print("Commands successfully run!")
        conn.save_config()
        if conn.check_config_mode():
            conn.exit_config_mode()

        # Create copy of running config and saves to output folder
        show_run = conn.send_command('show run', read_timeout=20)
        prompt = conn.find_prompt()
        hostname = prompt[0:-1]

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        filename = f'{hostname}_{year}-{month}-{day}_backup.txt'
        with open(f"Output/{filename}", mode="w") as data_extract:
            data_extract.write(show_run)
            print(f'Backup of {hostname} completed successfully')
            print('#' * 30)

        print('Closing Connection')
        conn.disconnect()


# allows for multiple devices to be accessed at once.
threads = list()
for key, values in switches.items():
    connection_dict = values
    th = threading.Thread(target=commands, args=(connection_dict,))
    threads.append(th)

for th in threads:
    th.start()

for th in threads:
    th.join()

end = time.time()
print(f'Total execution time:{end - start}')
