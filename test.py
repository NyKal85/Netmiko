VLAN_CRITERIA = '10'


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
        else:
            all_vlan_ports.append((interface, vlan_info))
    return vlan_ports, all_vlan_ports
