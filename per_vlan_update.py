from device_list import switches
from netmiko import ConnectHandler, NetmikoTimeoutException
from datetime import datetime
import threading
import time
import os

# Enter commands in commands_to_run.txt file with one command on each line.
with open('commands_to_run', 'r') as com:
    command_list = com.read().splitlines()

# Starts timer
start = time.time()

# Define your VLAN criteria and commands to apply
VLAN_CRITERIA = input('Which VLAN do you want to find? ')  # Example VLAN number to match
COMMANDS_FOR_VLAN = command_list


# Function to retrieve VLAN port information
def get_vlan_ports(conn):
    output = conn.send_command('show interfaces switchport')
    vlan_ports = []
    all_vlan_ports = []
    interface = ''
    vlan_info = ''
    for line in output.splitlines():
        if 'Name:' in line:
            interface = line[6:]  # Assuming the interface is the first element
        elif VLAN_CRITERIA in line:
            vlan_info = line  # Adjust based on actual format
            vlan_ports.append((interface, vlan_info))
            all_vlan_ports.append((interface, vlan_info))
        else:
            vlan_info = line
            all_vlan_ports.append((interface, vlan_info))
    print(all_vlan_ports)
    return vlan_ports


# Function to apply VLAN-specific commands
def apply_vlan_commands(conn, vlan_ports):
    for interface, vlan_info in vlan_ports:
        print(f"Applying commands to interface {interface} with VLAN info {vlan_info}")
        # Enter configuration mode for the interface
        conn.send_config_set([f'interface {interface}'] + COMMANDS_FOR_VLAN)


def commands(data):
    try:
        conn = ConnectHandler(**data)
    except NetmikoTimeoutException:
        print(f"Unable to connect to {data['host']}. Please check your data or the switch config manually.")
        return
    else:
        conn.enable()

        # Creates hostname for file output
        prompt = conn.find_prompt()
        hostname = prompt[0:-1]

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        filename = f'{hostname}_{year}-{month}-{day}_backup.txt'
        vlan_name = f'{hostname}_{VLAN_CRITERIA}_VLAN'

        # Get VLAN ports and display them
        vlan_data = []
        folder_name = f'{vlan_name}'
        folder_path = f'C:/Users/mcaudle/PycharmProjects/Netmiko/Output/{folder_name}'

        vlan_ports = get_vlan_ports(conn)
        if vlan_ports:
            print(f"Ports in VLAN {VLAN_CRITERIA}:")
            for interface, vlan_info in vlan_ports:
                interface_info = f"Interface: {interface}, VLAN Info: {vlan_info}"
                print(interface_info)
                vlan_data.append(f'{interface} : {vlan_info}')
            save_data = input('Do you want to save this data? (yes/no): ').strip().lower()
            if save_data == 'yes':
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                with open(f"{folder_path}/{hostname}", mode="w") as data_extract:
                    data_extract.write('\n'.join(vlan_data))
                    print(f'Copy of {hostname} vlan {VLAN_CRITERIA} information saved!')
                    print('#' * 30)
            # Prompt user for confirmation
            user_input = input("Do you want to apply changes to the listed ports? (yes/no): ").strip().lower()
            if user_input == 'yes':
                # Apply VLAN-specific commands
                apply_vlan_commands(conn, vlan_ports)
            else:
                print("No changes will be applied.")

        else:
            print(f"No ports found in VLAN {VLAN_CRITERIA}.")

        # Enters config mode and pushes commands to device and saves config
        conn.send_config_set(command_list)
        print("Commands successfully run!")
        conn.save_config()
        if conn.check_config_mode():
            conn.exit_config_mode()

        # Create a copy of the running config and save to output folder
        show_run = conn.send_command('show run', read_timeout=20)

        with open(f"Output/{filename}", mode="w") as data_extract:
            data_extract.write(show_run)
            print(f'Backup of {hostname} completed successfully')
            print('#' * 30)

        print('Closing Connection')
        conn.disconnect()


# Allows for multiple devices to be accessed at once
threads = []
for key, values in switches.items():
    connection_dict = values
    th = threading.Thread(target=commands, args=(connection_dict,))
    threads.append(th)

for th in threads:
    th.start()

for th in threads:
    th.join()

end = time.time()
print(f'Total execution time: {end - start}')
