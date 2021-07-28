# Copyright (c) 2021 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.0 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from collections import Counter
from dnacentersdk import api
from config import PI, USER, PASSWORD,USER_DNAC,PASS_DNAC,DNAC

# String that will hold final full configuration of all interfaces
interface_configs = ""
vlan_configs = ""
interfaces_configs = ""
counter1 = 1
old_switch = []
new_switch = []

old_line_cards = []
new_line_cards = []

with open("config.txt") as f:
    lines = f.read().splitlines()
    for num, line in enumerate(lines):
        if line.startswith("interface") and "Vlan" not in line:
            if line[-2] == "/" or line[-3] == "/":
                old_switch.append(line.rsplit("/",1)[0]+'/')
    old_switch = Counter(old_switch)
    for key,value in old_switch.items():
        print("Line card : " + key)
        print("Ports : " + str(value))
        print("---------------------------------")
    
input1 = "1"

while input1 != "0":
    input1 = input("Choose line card to select , press 0 to end selection : ")
    if input1 != "0":
        old_line_cards.append(input1)

# Create a DNACenterAPI connection object
dnac = api.DNACenterAPI(username=USER_DNAC,
                        password=PASS_DNAC,
                        base_url=DNAC,
                        version='2.1.2',
                        verify=False)

# Find all devices that have 'Wireless Controller' in their family
devices = dnac.devices.get_device_list(family='Switches and Hubs')
for device in devices['response']:
    print('hostname :',device['hostname'], 'device ID :',device['id'])
    print('----------------------------------------------------')

new_switch_id = input('Enter device ID for the new stack switch : ')

with open("new_config.txt", "w") as f:
    f.write(dnac.devices.get_device_config_by_id(network_device_id=new_switch_id).response)

with open("new_config.txt") as f:
    lines = f.read().splitlines()
    for num, line in enumerate(lines):
        if line.startswith("interface") and "Vlan" not in line:
            if line[-2] == "/" or line[-3] == "/":
                new_switch.append(line.rsplit("/",1)[0]+'/')
    new_switch = Counter(new_switch)
    for key,value in new_switch.items():
        print("Line card : " + key)
        print("Ports : " + str(value))
        print("---------------------------------")

input2 = "1"
while input2 != "0":
    input2 = input("Choose line card to select , press 0 to end selection : ")
    if input2 != "0":
        new_line_cards.append(input2)
    
print("Line cards selected from old device " + str(old_line_cards))
print("Line cards selected from new device " + str(new_line_cards))

# open config file
new_card_line_counter = 0
with open("config.txt") as f:
    lines = f.read().splitlines()
    for num, line in enumerate(lines):
        if line.rsplit("/",1)[0]+'/' in old_line_cards and "Vlan" not in line:
            counter = 1
            if counter1 < 49:
                line = new_line_cards[new_card_line_counter] + str(counter1)
                counter1 += 1
        
            if counter1 == 49:
                counter1 = 1
                new_card_line_counter += 1

            interfaces_config = ""
            interfaces_config += line + '\n'
            while lines[num+counter].strip() != '!':
                interfaces_config += lines[num+counter] + '\n'
                counter = counter + 1

            interfaces_configs += interfaces_config
            interfaces_config += '\n'

# Save the final configuraiton to a file 
with open("new_config.j2", "w") as f:
    f.write('\n')
    f.write(interfaces_configs)