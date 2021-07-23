import requests
import json
import csv
from datetime import datetime
from requests.auth import HTTPBasicAuth
from config import PI, USER, PASSWORD,USER_DNAC,PASS_DNAC,DNAC
import pprint
from netmiko import ConnectHandler
from dnacentersdk import api

base_url = 'https://' + PI + '/webacs/api/v3/data'

url = base_url + '/Devices.json'

payload = {}
headers = {
}

response = requests.request('GET', url,auth=HTTPBasicAuth(USER, PASSWORD),verify=False, headers=headers, data = payload)

response = json.loads(response.text)
devices_info = []

for device in response['queryResponse']['entityId']:
    url = base_url + '/InventoryDetails/' + device['$'] + '.json'

    response = requests.request('GET', url,auth=HTTPBasicAuth(USER, PASSWORD),verify=False, headers=headers, data = payload)
    response = json.loads(response.text)
    print('----------------------------')
    try:
        device_info = {}
        device_info['name'] = response['queryResponse']['entity'][0]['inventoryDetailsDTO']['summary']['deviceName']
        device_info['ip'] = response['queryResponse']['entity'][0]['inventoryDetailsDTO']['summary']['ipAddress']
        device_info['type'] = response['queryResponse']['entity'][0]['inventoryDetailsDTO']['summary']['deviceType']
        devices_info.append(device_info)

    except KeyError:
        print("No device name")

pprint.pprint(devices_info)

device = input("Select the device IP to retrieve port configuration : ")
ssh_creds = input("Enter ssh credentials username:password : ")

iou1 = {
'device_type': 'cisco_ios',
'ip': device,
'username': ssh_creds.split(':')[0],
'password': ssh_creds.split(':')[1],
}

device = ConnectHandler(**iou1)

output1 = device.send_command("show running-config")
save_file = open("config.txt","w")
save_file.write(output1)
save_file.close()
device.disconnect()
