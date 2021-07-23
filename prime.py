import requests
import json
import csv
from datetime import datetime
from requests.auth import HTTPBasicAuth
from config import PI, USER, PASSWORD
import pprint
from netmiko import ConnectHandler
from dnacentersdk import api

base_url = 'https://' + PI + '/webacs/api/v4/data'

url = base_url + '/BulkSanitizedConfigArchives.json'

payload = {}
headers = {
}

response = requests.request('GET', url,auth=HTTPBasicAuth(USER, PASSWORD),verify=False, headers=headers, data = payload)

response = json.loads(response.text)

pprint.pprint(response)

file_id = input("Select file ID to download configuration : ")

base_url = 'https://' + PI + '/webacs/api/v4/op'
url = base_url + '/configArchiveService/extractSanitizedFile.json?fileId=' + file_id

payload = {
}
headers = {
}
response = requests.request('GET', url,auth=HTTPBasicAuth(USER, PASSWORD),verify=False, headers=headers, data = payload)

response = json.loads(response.text)

pprint.pprint(response)