import netmiko

Cisco_Router = {
  'device_type':'cisco_ios',
  'ip':'1.1.10.1',
  'username':'admin',
  'password':'admin12!@#'
}

print("")
commands = [
  'int tunnel 0',
  'tunnel source Gig 1',
  'tunnel destination 1.1.20.1',
  'ip address 10.1.13.1 255.255.255.252',
  'keepalive 10 3',
  'exit',
  'router ospf 1',
  'network 10.1.20.1 0.0.0.0 area 0',
  'network 192.168.1.254 0.0.0.0 area 0',
  'end',
  'wr'
]

net_connect = netmiko.ConnectHandler(**Cisco_Router)
config = net_connect.send_config_set(commands)
config += net_connect.send_command('show run | sec Tunnel')
config += net_connect.send_command('show ip route ospf')
print(config)

net_connect.disconnect()
