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

import yaml
from prettyprinter import pprint
import collections
from collections import abc
from DNACenter import DNACenter
from jinja2 import Template
import time
import os
from config import PI, USER, PASSWORD,USER_DNAC,PASS_DNAC,DNAC

#TODO: Setting deploy to False will only create the template in DNAC
# Setting deploy to True will deploy the template to devices specified under the NETWORK variable
deploy = False

#TODO: ENTER THE IP ADDRESS(S) OF DEVICES TO TARGET WITH TEMPLATE DEPLOYMENT
NETWORK = [""]
#TODO: ENTER DNAC USERNAME
USERNAME = USER_DNAC
#TODO: ENTER DNAC PASSWORD
PASSWORD = PASS_DNAC
#ENTER DNAC BASE URL
BASE_URL = DNAC

#TODO: Enter the DNAC template project name 
TEMPLATE_PROJECT_NAME = "GVE_DevNet_Jorge"

#TODO: Enter Device Family
"""
Examples of device familes:

Routers
Switches and Hubs
Wireless Sensor
Unified AP	
"""
TEMPLATE_DEVICE_FAMILY = "Switches and Hubs"


#Points to the jinja template file
JINJA_TEMPLATE = 'new_config.j2'
#Points to the YAML config file
YAML_TEMPLATE = 'new_config.yaml'





#TODO: Enter DNAC template name
DNAC_TEMPLATE_NAME = "TEMPLATE_FROM_SCRIPT"

def yaml_to_templates(temp, template_name):
		for template in session.get_template_projects(project_name = TEMPLATE_PROJECT_NAME):
			if template['name'] == template_name:
				session.delete_template(template['id'])

		template_id = None
		session.create_template(template_name, temp, project_name=TEMPLATE_PROJECT_NAME, device_family=TEMPLATE_DEVICE_FAMILY)
		print(template_name)
		for template in session.get_template_projects(project_name = TEMPLATE_PROJECT_NAME):
			if template['name'] == template_name:
				template_id = template['id']
				session.commit_template(template['id'])

		if deploy == True:
			session.deploy_template(template_id)




def yaml_to_dict(yaml_file):
	with open(yaml_file, 'rb') as f:
		document = yaml.load(f, Loader=yaml.FullLoader)

		pprint(document)

		return document


def load_jinja(jinja_template, yaml_data):
	with open (jinja_template) as f:
		 template = Template(''.join(f.readlines()))

	return template.render(yaml_data)



if __name__ == "__main__":

	session = DNACenter(username = USERNAME, password = PASSWORD, base_url=BASE_URL,device_ip_addresses=NETWORK)
	template = load_jinja(JINJA_TEMPLATE,yaml_to_dict(YAML_TEMPLATE))
	yaml_to_templates(template, DNAC_TEMPLATE_NAME)





