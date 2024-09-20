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
VLAN_CRITERIA = ""  # Example VLAN number to match
COMMANDS_FOR_VLAN = command_list


# Function to retrieve VLAN port information
def get_vlan_ports(conn):
    VLAN_CRITERIA = input('Which VLAN do you want to find? ')
    output = conn.send_command('show interfaces switchport', read_timeout=30)
    vlan_ports = []
    all_vlan_ports = []
    interface = ''
    prompt = conn.find_prompt()
    hostname = prompt[0:-1]

    for line in output.splitlines():
        if 'Name:' in line:
            interface = line[6:]  # If name in line print everything after 'Name: '
        elif VLAN_CRITERIA in line and 'Access Mode' in line:
            vlan_info = line  # Adjust based on actual format
            vlan_ports.append((interface, vlan_info))
            all_vlan_ports.append((interface, vlan_info))
        elif "VLAN":
            vlan_info = line
            all_vlan_ports.append((interface, vlan_info))
    with open(f"Output/{hostname}.txt", mode="w") as data_extract:
        new_data = ', '.join([str(t) for t in all_vlan_ports])
        data_extract.write(new_data)
        print(f'Copy of {hostname} vlan data!')
        print('#' * 30)
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

        vlan_name = f'{hostname}_{VLAN_CRITERIA}_VLAN'

        # Get VLAN ports and display them
        vlan_data = []
        folder_name = f'{vlan_name}'
        folder_path = f'C:/Users/mcaudle/PycharmProjects/Netmiko/Output/{folder_name}'

        vlan_ports = get_vlan_ports(conn)
        if vlan_ports:
            interface_list = []
            print(f"Ports in VLAN {VLAN_CRITERIA}:")
            for interface, vlan_info in vlan_ports:
                interface_info = f"Interface: {interface}, VLAN Info: {vlan_info}"
                print(interface_info)
                interface_list.append(interface)
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
                default_port = input("Do you want to set port to default configuration? (yes/no): ").strip().lower()
                if default_port == 'yes':
                    for interface in interface_list:
                        conn.send_config_set([f'default interface {interface}'])
                        print(f'Setting {interface} to default')
                    apply_vlan_commands(conn, vlan_ports)
                else:
                    # Apply VLAN-specific commands
                    apply_vlan_commands(conn, vlan_ports)
            else:
                print("No changes will be applied.")
        else:
            print(f"No ports found in VLAN {VLAN_CRITERIA}.")

        # Enters config mode and pushes commands to device and saves config
        conn.send_config_set(command_list)
        print("Commands successfully run!")
        print("Saving Configuration")
        conn.save_config()
        if conn.check_config_mode():
            conn.exit_config_mode()

        # Create a copy of the running config and save to output folder
        # show_run = conn.send_command('show run', read_timeout=20)
        #
        # with open(f"Output/{filename}", mode="w") as data_extract:
        #     data_extract.write(show_run)
        #     print(f'Backup of {hostname} completed successfully')
        #     print('#' * 30)

        print('Closing Connection')
        conn.disconnect()


# Allows for multiple devices to be accessed at once
threads = []
for key, values in switches.items():
    connection_dict = values
    commands(connection_dict)
#     th = threading.Thread(target=commands, args=(connection_dict,))
#     threads.append(th)
#
# for th in threads:
#     th.start()
#
# for th in threads:
#     th.join()
#
# end = time.time()
# print(f'Total execution time: {end - start}')
