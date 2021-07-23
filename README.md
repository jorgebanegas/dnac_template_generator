**Jinja_template_creator**

script that reads a config file then creates a jinja template based on the information from the config file

Contacts:

* Jorge Banegas ( jbanegas@cisco.com )


**Source Installation**

Create and enter virtual environment

```bash
virtualenv env
source env/bin/activate
```

Install project dependencies

```bash
pip install -r requirements.txt
```
Include the credentials of your DNAC/Prime instance inside the config.py file

```python
PI=""
USER=""
PASSWORD=""

USER_DNAC=""
PASS_DNAC=""
DNAC=""
```

Be sure to include config file inside the project folder and name it config.txt

Run python ssh script, if you want to install the config file from prime (will need ssh credentials)

```bash
python ssh.py
```

Run python main script to create the new jinja template

```bash
python main.py
```

Run python converter script to submit the jinja template onto your dnac instance

Be sure to include an existing DNAC project name

```python
#TODO: Enter the DNAC template project name 
TEMPLATE_PROJECT_NAME = "GVE_DevNet_Jorge"
```

```bash
python converter.py
```
