# ----------------
# Python
# ----------------
import os
import sys
import yaml
import time
import json
import shutil
import logging
import requests
import math
import xmltodict
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, LEARN, RUNNING, CLOUD, WRITING, FINISHED
from tinydb import TinyDB, Query

# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# Filetypes 
# ----------------

filetype_loop = ["csv","md","html"]

# ----------------
# Template Directory
# ----------------

template_dir = 'templates/cisco/ise'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Create Database
# ----------------

if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/The_Grail/Grail_DB.json"):
    os.remove("Camelot/Cisco/DevNet_Sandbox/ISE/The_Grail/Grail_DB.json")

db = TinyDB('Camelot/Cisco/DevNet_Sandbox/ISE/The_Grail/Grail_DB.json')

# ----------------
# Load Credentials 
# ----------------

with open("testbed/testbed_DevNet_ISE.yaml") as stream:
    testbed = yaml.safe_load(stream)

# ---------------------------------------
# API Get Token
# ---------------------------------------

for device,value in testbed['devices'].items():
    api_username = testbed["devices"][device]["credentials"]["default"]["username"]
    api_password = testbed["devices"][device]["credentials"]["default"]["password"]
    device_ip = testbed["devices"][device]["connections"]["ip"]

json_headers = { "Content-Type": "application/json", "Accept": "application/json"}
xml_headers = { "Content-Type": "application/xml", "Accept": "application/xml"}

# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
    @aetest.subsection
    def connect_to_devices(self):
        """Connect to all the devices"""
        print(Panel.fit(Text.from_markup(GREETING)))

# ----------------
# Test Case #1 - Go to ISE ERS API
# ----------------
class Collect_Information(aetest.Testcase):
    """Parse all the commands"""

    @aetest.test
    def parse(self, section, steps):
        """ Testcase Setup section """
        for device in testbed['devices']:
            table = db.table(testbed["devices"][device]["alias"])
            print(Panel.fit(Text.from_markup(RUNNING)))

            # Get Network Device Page Count
            with steps.start('Requesting Network Devices API Page Count',continue_=True) as step:
                try:
                    self.raw_page_count = requests.get("https://%s:9060/ers/config/networkdevice?size=100" % device_ip, auth=(api_username, api_password), headers=json_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            pagecount = (self.raw_page_count.json()['SearchResult']['total'])

            # Define Templates 
            network_devices_template = env.get_template('network_devices.j2')
            network_device_details_template = env.get_template('network_device_details.j2')

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Device,Description,ISE ID")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.md",'a') as md:
                md.seek(0, 0)
                md.write("# Network Devices")
                md.write("\n")
                md.write("| Device | Description | ISE ID |")
                md.write("\n")
                md.write("| ------ | ----------- | ------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Network Devices</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Device</th><th>Description</th><th>ISE ID</th></tr>")
                html.close() 

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Device Name,Device IP,Subnet Mask,Description,Profile Name,Network Protocol,Shared Secret,SNMP Link Trap,MAC Trap,Polling Interval,RO Community,Version")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.md",'a') as md:
                md.seek(0, 0)
                md.write("# Network Device Details")
                md.write("\n")
                md.write("| Device Name | Device IP | Subnet Mask | Description | Profile Name | Network Protocol | Shared Secret | SNMP Link Trap | MAC Trap | Polling Interval | RO Community | Version |")
                md.write("\n")
                md.write("| ----------- | --------- | ----------- | ----------- | ------------ | ---------------- | ------------- | -------------- | -------- | ---------------- | ------------ | ------- |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Network Device Details</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Device Name</th><th>Device IP</th><th>Subnet Mask</th><th>Description</th><th>Profile Name</th><th>Network Protocol</th><th>Shared Secret</th><th>SNMP Link Trap</th><th>MAC Trap</th><th>Polling Interval</th><th>RO Community</th><th>Version</th></tr>")                     
                html.close() 

            # Get Parent Network Devices
            for page in range(1,math.ceil(pagecount/100+1)):
                with steps.start('Requesting Master List of Network Devices Information',continue_=True) as step:
                    try:
                        self.raw_network_devices = requests.get("https://%s:9060/ers/config/networkdevice?size=100&page=%i" % (device_ip,page), auth=(api_username, api_password), headers=json_headers, verify=False,)
                        print(Panel.fit(Text.from_markup(CLOUD)))
                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                # ---------------------------------------
                # Generate CSV / MD / HTML / Mind Maps
                # ---------------------------------------

                # Parent Network Device
                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))       

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.json", "a") as fid:
                        json.dump(self.raw_network_devices.json(), fid, indent=4, sort_keys=True)
                        fid.write('\n')
                                
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.yaml", "a") as yml:
                        yaml.dump(self.raw_network_devices.json(), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_network_devices = network_devices_template.render(to_parse_network_devices=self.raw_network_devices.json(),filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.%s" % filetype, "a") as fh:
                            fh.write(parsed_network_devices)
                            fh.close()

                    # ----------------
                    # Store Devices in Device Table in Database
                    # ----------------

                    table.insert(self.raw_network_devices.json())

                # Get Child Network Devices

                for device in self.raw_network_devices.json()['SearchResult']['resources']:
                    with steps.start('Requesting Individual Network Devices Information',continue_=True) as step:
                        try:
                            self.raw_network_device_details = requests.get(device['link']['href'], auth=(api_username, api_password), headers=json_headers, verify=False,)
                            print(Panel.fit(Text.from_markup(CLOUD)))
                        except Exception as e:
                            step.failed('There was a problem with the API\n{e}'.format(e=e))
                
                    with steps.start('Store data',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))       

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.json", "a") as fid:
                            json.dump(self.raw_network_device_details.json(), fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.yaml", "a") as yml:
                            yaml.dump(self.raw_network_device_details.json(), yml, allow_unicode=True)
                    
                        for filetype in filetype_loop:
                            parsed_network_device_details = network_device_details_template.render(to_parse_network_device_details=self.raw_network_device_details.json(),filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.%s" % filetype, "a") as fh:
                                fh.write(parsed_network_device_details)
                                fh.close()

                        # ----------------
                        # Store Devices in Device Table in Database
                        # ----------------

                        table.insert(self.raw_network_device_details.json())

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                            
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_devices_mind_map.html")

            fid.close()
            yml.close()

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                                
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Network_Devices/network_device_details_mind_map.html")
            fid.close()
            yml.close()

            # Get Indentity Page Count
            with steps.start('Requesting Identity Groups API Page Count',continue_=True) as step:
                try:
                    self.raw_page_count = requests.get("https://%s:9060/ers/config/identitygroup?size=100" % device_ip, auth=(api_username, api_password), headers=json_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            pagecount = (self.raw_page_count.json()['SearchResult']['total'])

            # Define Templates 
            identity_groups_template = env.get_template('identity_groups.j2')
            identity_group_details_template = env.get_template('identity_group_details.j2')

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Name,Description,ISE ID")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.md",'a') as md:
                md.seek(0, 0)
                md.write("# Identity Groups")
                md.write("\n")
                md.write("| Name | Description | ISE ID |")
                md.write("\n")
                md.write("| ---- | ----------- | ------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Identity Groups</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Name</th><th>Description</th><th>ISE ID</th></tr>")
                html.close() 

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Name,Description,ISE ID,Parent Group")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.md",'a') as md:
                md.seek(0, 0)
                md.write("# Network Identity Group Details")
                md.write("\n")
                md.write("| Name | Description | ISE ID | Parent Group |")
                md.write("\n")
                md.write("| ---- | ----------- | ------ | ------------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Network Identity Group Details</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Name</th><th>Description</th><th>ISE ID</th><th>Parent Group</th></tr>")
                html.close() 

            # Get Parent Identity Groups
            for page in range(1,math.ceil(pagecount/100+1)):
                with steps.start('Requesting Master List of Identity Groups Information',continue_=True) as step:
                    try:
                        self.raw_identity_groups = requests.get("https://%s:9060/ers/config/identitygroup?size=100&page=%i" % (device_ip,page), auth=(api_username, api_password), headers=json_headers, verify=False,)
                        print(Panel.fit(Text.from_markup(CLOUD)))
                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                # Parent Identity Groups
                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))       

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.json", "a") as fid:
                        json.dump(self.raw_identity_groups.json(), fid, indent=4, sort_keys=True)
                        fid.write('\n')
                                
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.yaml", "a") as yml:
                        yaml.dump(self.raw_identity_groups.json(), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_identity_groups = identity_groups_template.render(to_parse_identity_groups=self.raw_identity_groups.json(),filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.%s" % filetype, "a") as fh:
                            fh.write(parsed_identity_groups)
                            fh.close()

                    # ----------------
                    # Store Identities in Table in Database
                    # ----------------

                    table.insert(self.raw_identity_groups.json())

                # Get Child Identities
                for device in self.raw_identity_groups.json()['SearchResult']['resources']:
                    with steps.start('Requesting Individual Identity Group Information',continue_=True) as step:
                        try:
                            self.raw_network_identity_group_details = requests.get(device['link']['href'], auth=(api_username, api_password), headers=json_headers, verify=False,)
                            print(Panel.fit(Text.from_markup(CLOUD)))
                        except Exception as e:
                            step.failed('There was a problem with the API\n{e}'.format(e=e))
                
                    with steps.start('Store data',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))       

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.json", "a") as fid:
                            json.dump(self.raw_network_identity_group_details.json(), fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.yaml", "a") as yml:
                            yaml.dump(self.raw_network_identity_group_details.json(), yml, allow_unicode=True)
                    
                        for filetype in filetype_loop:
                            parsed_identity_group_details = identity_group_details_template.render(to_parse_identity_group_details=self.raw_network_identity_group_details.json(),filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.%s" % filetype, "a") as fh:
                                fh.write(parsed_identity_group_details)
                                fh.close()

                        # ----------------
                        # Store Identity Details in Table in Database
                        # ----------------

                        table.insert(self.raw_network_identity_group_details.json())

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                            
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_groups_mind_map.html")

            fid.close()
            yml.close()

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                                
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Identity_Groups/identity_group_details_mind_map.html")

            fid.close()
            yml.close()

            # Get EPG Page Count
            with steps.start('Requesting End Point Group API Page Count',continue_=True) as step:
                try:
                    self.raw_page_count = requests.get("https://%s:9060/ers/config/endpointgroup?size=100" % device_ip, auth=(api_username, api_password), headers=json_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            pagecount = (self.raw_page_count.json()['SearchResult']['total'])

            # Define Templates 
            endpoint_groups_template = env.get_template('endpoint_groups.j2')
            endpoint_group_details_template = env.get_template('endpoint_group_details.j2')

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Device,Description,ISE ID")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.md",'a') as md:
                md.seek(0, 0)
                md.write("# Endpoint Groups")
                md.write("\n")
                md.write("| Device | Description | ISE ID |")
                md.write("\n")
                md.write("| ------ | ----------- | ------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Endpoint Groups</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Device</th><th>Description</th><th>ISE ID</th></tr>")
                html.close() 

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Name,Description,ISE ID,System Defined")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.md",'a') as md:
                md.seek(0, 0)
                md.write("# Network Endpoint Group Details")
                md.write("\n")
                md.write("| Name | Description | ISE ID | System Defined |")
                md.write("\n")
                md.write("| ---- | ----------- | ------ | -------------- |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Network Endpoint Group Details</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Name</th><th>Description</th><th>ISE ID</th><th>System Defined</th></tr>")
                html.close() 

            # Get Parent Endpoint Groups
            for page in range(1,math.ceil(pagecount/100+1)):
                with steps.start('Requesting Master List of Endpoint Groups Information',continue_=True) as step:
                    try:
                        self.raw_endpoint_groups = requests.get("https://%s:9060/ers/config/endpointgroup?size=100&page=%i" % (device_ip,page), auth=(api_username, api_password), headers=json_headers, verify=False,)
                        print(Panel.fit(Text.from_markup(CLOUD)))
                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                # ---------------------------------------
                # Generate CSV / MD / HTML / Mind Maps
                # ---------------------------------------

                # Parent Network Device
                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))       

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.json", "a") as fid:
                        json.dump(self.raw_endpoint_groups.json(), fid, indent=4, sort_keys=True)
                        fid.write('\n')
                                
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.yaml", "a") as yml:
                        yaml.dump(self.raw_endpoint_groups.json(), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_endpoint_groups = endpoint_groups_template.render(to_parse_endpoint_groups=self.raw_endpoint_groups.json(),filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.%s" % filetype, "a") as fh:
                            fh.write(parsed_endpoint_groups)
                            fh.close()

                    # ----------------
                    # Store Devices in Device Table in Database
                    # ----------------

                    table.insert(self.raw_endpoint_groups.json())

                # Get Child Identities
                for device in self.raw_endpoint_groups.json()['SearchResult']['resources']:
                    with steps.start('Requesting Individual Endpoint Group Information',continue_=True) as step:
                        try:
                            self.raw_endpoint_group_details = requests.get(device['link']['href'], auth=(api_username, api_password), headers=json_headers, verify=False,)
                            print(Panel.fit(Text.from_markup(CLOUD)))
                        except Exception as e:
                            step.failed('There was a problem with the API\n{e}'.format(e=e))
                
                    with steps.start('Store data',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))       

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.json", "a") as fid:
                            json.dump(self.raw_endpoint_group_details.json(), fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.yaml", "a") as yml:
                            yaml.dump(self.raw_endpoint_group_details.json(), yml, allow_unicode=True)
                    
                        for filetype in filetype_loop:
                            parsed_endpoint_group_details = endpoint_group_details_template.render(to_parse_endpoint_group_details=self.raw_endpoint_group_details.json(),filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.%s" % filetype, "a") as fh:
                                fh.write(parsed_endpoint_group_details)
                                fh.close()

                        # ----------------
                        # Store Endpoint Details in Table in Database
                        # ----------------

                        table.insert(self.raw_endpoint_group_details.json())

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                            
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_groups_mind_map.html")

            fid.close()
            yml.close()

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                                
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Endpoint_Groups/endpoint_group_details_mind_map.html")
            fid.close()
            yml.close()

            # Get dACL Page Count
            with steps.start('Requesting dACL API Page Count',continue_=True) as step:
                try:
                    self.raw_page_count = requests.get("https://%s:9060/ers/config/downloadableacl?size=100" % device_ip, auth=(api_username, api_password), headers=json_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            pagecount = (self.raw_page_count.json()['SearchResult']['total'])

            # Define Templates 
            dACLs_template = env.get_template('dACLs.j2')
            dACL_details_template = env.get_template('dACL_details.j2')

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Device,Description,ISE ID")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.md",'a') as md:
                md.seek(0, 0)
                md.write("# dACLs")
                md.write("\n")
                md.write("| Device | Description | ISE ID |")
                md.write("\n")
                md.write("| ------ | ----------- | ------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>dACLs</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Device</th><th>Description</th><th>ISE ID</th></tr>")
                html.close() 

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("dACL,Description,Type,Rules")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.md",'a') as md:
                md.seek(0, 0)
                md.write("# dACL Details")
                md.write("\n")
                md.write("| dACL | Description | Type | Rules |")
                md.write("\n")
                md.write("| ---- | ----------- | ---- | ----- |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>dACL Details</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>dACL</th><th>Description</th><th>Type</th><th>Rules</tr>")
                html.close() 

            # Get Parent dACLs
            for page in range(1,math.ceil(pagecount/100+1)):
                with steps.start('Requesting Master List of dACL Information',continue_=True) as step:
                    try:
                        self.raw_dACLs = requests.get("https://%s:9060/ers/config/downloadableacl?size=100&page=%i" % (device_ip,page), auth=(api_username, api_password), headers=json_headers, verify=False,)
                        print(Panel.fit(Text.from_markup(CLOUD)))
                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                # ---------------------------------------
                # Generate CSV / MD / HTML / Mind Maps
                # ---------------------------------------

                # Parent dACL
                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))       

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.json", "a") as fid:
                        json.dump(self.raw_dACLs.json(), fid, indent=4, sort_keys=True)
                        fid.write('\n')
                                
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.yaml", "a") as yml:
                        yaml.dump(self.raw_dACLs.json(), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_dACLs = dACLs_template.render(to_parse_dACLs=self.raw_dACLs.json(),filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.%s" % filetype, "a") as fh:
                            fh.write(parsed_dACLs)
                            fh.close()

                    # ----------------
                    # Store Devices in Device Table in Database
                    # ----------------

                    table.insert(self.raw_dACLs.json())

                # Get Child dACLs
                for device in self.raw_dACLs.json()['SearchResult']['resources']:
                    with steps.start('Requesting Individual Network Devices Information',continue_=True) as step:
                        try:
                            self.raw_dACL_details = requests.get(device['link']['href'], auth=(api_username, api_password), headers=json_headers, verify=False,)
                            print(Panel.fit(Text.from_markup(CLOUD)))
                        except Exception as e:
                            step.failed('There was a problem with the API\n{e}'.format(e=e))
                
                    with steps.start('Store data',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))       

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.json", "a") as fid:
                            json.dump(self.raw_dACL_details.json(), fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.yaml", "a") as yml:
                            yaml.dump(self.raw_dACL_details.json(), yml, allow_unicode=True)
                    
                        for filetype in filetype_loop:
                            parsed_dACL_details = dACL_details_template.render(to_parse_dACL_details=self.raw_dACL_details.json(),filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.%s" % filetype, "a") as fh:
                                fh.write(parsed_dACL_details)
                                fh.close()

                        # ----------------
                        # Store Devices in Device Table in Database
                        # ----------------

                        table.insert(self.raw_dACL_details.json())

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                            
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs.md --output Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACLs_mind_map.html")
            fid.close()
            yml.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                                
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/dACLs/dACL_details_mind_map.html")
            fid.close()
            yml.close()

            # Get Authorization Profile Page Count
            with steps.start('Requesting Authorization Profile API Page Count',continue_=True) as step:
                try:
                    self.raw_page_count = requests.get("https://%s:9060/ers/config/authorizationprofile?size=100" % device_ip, auth=(api_username, api_password), headers=json_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            pagecount = (self.raw_page_count.json()['SearchResult']['total'])

            # Define Templates 
            authorization_profiles_template = env.get_template('authorization_profiles.j2')
            authorization_profile_details_template = env.get_template('authorization_profile_details.j2')
                    
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Device,Description,ISE ID")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.md",'a') as md:
                md.seek(0, 0)
                md.write("# Authorization Profiles")
                md.write("\n")
                md.write("| Device | Description | ISE ID |")
                md.write("\n")
                md.write("| ------ | ----------- | ------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Authorization Profiles</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Device</th><th>Description</th><th>ISE ID</th></tr>")
                html.close() 

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Profile,Description,Access Type,Authorization Profile Type,Profile Name,VLAN Name,Voice Domain Permission,Web Authentication")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.md",'a') as md:
                md.seek(0, 0)
                md.write("# Authorization Profile Details")
                md.write("\n")
                md.write("| Profile | Description | Access Type | Authorization Profile Type | Profile Name | VLAN Name | Voice Domain Permission | Web Authentication |")
                md.write("\n")
                md.write("| ------- | ----------- | ----------- | -------------------------- | ------------ | --------- | ----------------------- | ------------------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Authorization Profile Details</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Profile</th><th>Description</th><th>Access Type</th><th>Authorization Profile Type</th><th>Profile Name</th><th>VLAN Name</th><th>Voice Domain Permission</th><th>Web Authentication</th></tr>")
                html.close() 

            # Get Parent Network Devices
            for page in range(1,math.ceil(pagecount/100+1)):
                with steps.start('Requesting Master List of Authorization Profile Information',continue_=True) as step:
                    try:
                        self.raw_authorization_profiles = requests.get("https://%s:9060/ers/config/authorizationprofile?size=100&page=%i" % (device_ip,page), auth=(api_username, api_password), headers=json_headers, verify=False,)
                        print(Panel.fit(Text.from_markup(CLOUD)))
                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                # ---------------------------------------
                # Generate CSV / MD / HTML / Mind Maps
                # ---------------------------------------

                # Parent Network Device
                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))       

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.json", "a") as fid:
                        json.dump(self.raw_authorization_profiles.json(), fid, indent=4, sort_keys=True)
                        fid.write('\n')
                                
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.yaml", "a") as yml:
                        yaml.dump(self.raw_authorization_profiles.json(), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_authorization_profiles = authorization_profiles_template.render(to_parse_authorization_profiles=self.raw_authorization_profiles.json(),filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.%s" % filetype, "a") as fh:
                            fh.write(parsed_authorization_profiles)
                            fh.close()

                    # ----------------
                    # Store Authorization Profiles Table in Database
                    # ----------------

                    table.insert(self.raw_authorization_profiles.json())

                # Get Child Authorization Profiles Devices
                for device in self.raw_authorization_profiles.json()['SearchResult']['resources']:
                    with steps.start('Requesting Individual Authorization Profile Information',continue_=True) as step:
                        try:
                            self.raw_authorization_profile_details = requests.get(device['link']['href'], auth=(api_username, api_password), headers=json_headers, verify=False,)
                            print(Panel.fit(Text.from_markup(CLOUD)))
                        except Exception as e:
                            step.failed('There was a problem with the API\n{e}'.format(e=e))
                
                    with steps.start('Store data',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))       

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.json", "a") as fid:
                            json.dump(self.raw_authorization_profile_details.json(), fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.yaml", "a") as yml:
                            yaml.dump(self.raw_authorization_profile_details.json(), yml, allow_unicode=True)
                    
                        for filetype in filetype_loop:
                            parsed_authorization_profile_details = authorization_profile_details_template.render(to_parse_authorization_profile_details=self.raw_authorization_profile_details.json(),filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.%s" % filetype, "a") as fh:
                                fh.write(parsed_authorization_profile_details)
                                fh.close()

                        # ----------------
                        # Store Devices in Device Table in Database
                        # ----------------

                        table.insert(self.raw_authorization_profile_details.json())

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                            
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profiles_mind_maps.html")

            fid.close()
            yml.close()

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                                
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Authorization_Profiles/authorization_profile_details_mind_map.html")
                
            fid.close()
            yml.close()

            # Get Administrator Page Count
            with steps.start('Requesting Administrators API Page Count',continue_=True) as step:
                try:
                    self.raw_page_count = requests.get("https://%s:9060/ers/config/adminuser?size=100" % device_ip, auth=(api_username, api_password), headers=json_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            pagecount = (self.raw_page_count.json()['SearchResult']['total'])

            # Define Templates 
            administrators_template = env.get_template('administrators.j2')
            administrator_details_template = env.get_template('administrator_details.j2')

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Name,Description,ISE ID")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.md",'a') as md:
                md.seek(0, 0)
                md.write("# Administrators")
                md.write("\n")
                md.write("| Name | Description | ISE ID |")
                md.write("\n")
                md.write("| ---- | ----------- | ------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Administrators</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Name</th><th>Description</th><th>ISE ID</th></tr>")
                html.close() 

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Name,Description,Enabled,Admin Group,Change Password,External User,Inactive Account Never Disable,Include System Alarms in Emails,ISE ID")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.md",'a') as md:
                md.seek(0, 0)
                md.write("# Administrator Details")
                md.write("\n")
                md.write("| Name | Description | Enabled | Admin Group | Change Password | External User | Inactive Account Never Disable | Include System Alarms in Emails | ISE ID |")
                md.write("\n")
                md.write("| ---- | ----------- | ------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Administrator Details</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Name</th><th>Description</th><th>Enabled</th><th>Admin Group</th><th>Change Password</th><th>External User</th><th>Inactive Account Never Disable</th><th>Include System Alarms in Emails</th><th>ISE ID</th></tr>")
                html.close() 

            # Get Parent Administrator
            for page in range(1,math.ceil(pagecount/100+1)):
                with steps.start('Requesting Master List of Administrator Information',continue_=True) as step:
                    try:
                        self.raw_administrators = requests.get("https://%s:9060/ers/config/adminuser?size=100&page=%i" % (device_ip,page), auth=(api_username, api_password), headers=json_headers, verify=False,)
                        print(Panel.fit(Text.from_markup(CLOUD)))
                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                # ---------------------------------------
                # Generate CSV / MD / HTML / Mind Maps
                # ---------------------------------------

                # Parent Administrator
                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))       

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.json", "a") as fid:
                        json.dump(self.raw_administrators.json(), fid, indent=4, sort_keys=True)
                        fid.write('\n')
                                
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.yaml", "a") as yml:
                        yaml.dump(self.raw_administrators.json(), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_administrators = administrators_template.render(to_parse_administrators=self.raw_administrators.json(),filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.%s" % filetype, "a") as fh:
                            fh.write(parsed_administrators)
                            fh.close()

                    # ----------------
                    # Store Administrators in Device Table in Database
                    # ----------------

                    table.insert(self.raw_administrators.json())

                # Get Child Administrator Details

                for device in self.raw_administrators.json()['SearchResult']['resources']:
                    with steps.start('Requesting Individual Administrator Information',continue_=True) as step:
                        try:
                            self.raw_administrator_details = requests.get(device['link']['href'], auth=(api_username, api_password), headers=json_headers, verify=False,)
                            print(Panel.fit(Text.from_markup(CLOUD)))
                        except Exception as e:
                            step.failed('There was a problem with the API\n{e}'.format(e=e))
                
                    with steps.start('Store data',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))       

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.json", "a") as fid:
                            json.dump(self.raw_administrator_details.json(), fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.yaml", "a") as yml:
                            yaml.dump(self.raw_administrator_details.json(), yml, allow_unicode=True)
                    
                        for filetype in filetype_loop:
                            parsed_administrator_details = administrator_details_template.render(to_parse_administrator_details=self.raw_administrator_details.json(),filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.%s" % filetype, "a") as fh:
                                fh.write(parsed_administrator_details)
                                fh.close()

                        # ----------------
                        # Store Admin Details Table in Database
                        # ----------------

                        table.insert(self.raw_administrator_details.json())

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                            
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrators_mind_map.html")

            fid.close()
            yml.close()

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                                
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Administrators/administrator_details_mind_map.html")

            fid.close()
            yml.close()

            # Get Parent Allowed Protocols
            with steps.start('Requesting Master List of Allowed Protocols Information',continue_=True) as step:
                try:
                    self.raw_allowed_protocols = requests.get("https://%s:9060/ers/config/allowedprotocols" % device_ip, auth=(api_username, api_password), headers=json_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))

            # ---------------------------------------
            # Generate CSV / MD / HTML / Mind Maps
            # ---------------------------------------

            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))       
                with open("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocols.json", "a") as fid:
                    json.dump(self.raw_allowed_protocols.json(), fid, indent=4, sort_keys=True)
                    fid.write('\n')
                            
                with open("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocols.yaml", "a") as yml:
                    yaml.dump(self.raw_allowed_protocols.json(), yml, allow_unicode=True)

                for filetype in filetype_loop:
                    parsed_allowed_protocols = allowed_protocols_template.render(to_parse_allowed_protocols=self.raw_allowed_protocols.json(),filetype_loop_jinja2=filetype)
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocols.%s" % filetype, "a") as fh:
                        fh.write(parsed_allowed_protocols)
                        fh.close()

                # ----------------
                # Store allowed_protocols in Device Table in Database
                # ----------------
                table.insert(self.raw_allowed_protocols.json())

            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocols.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocols.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocols_mind_map.html")

            fid.close()
            yml.close()

            # Get Child Allowed Protocols
            for device in self.raw_allowed_protocols.json()['SearchResult']['resources']:
                with steps.start('Requesting Individual Allowed Protocols Information',continue_=True) as step:
                    try:
                        self.raw_allowed_protocol_details = requests.get(device['link']['href'], auth=(api_username, api_password), headers=json_headers, verify=False,)
                        print(Panel.fit(Text.from_markup(CLOUD)))
                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))
            
                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING))) 

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocol_details.json", "a") as fid:
                        json.dump(self.raw_allowed_protocol_details.json(), fid, indent=4, sort_keys=True)
                        fid.write('\n')
                            
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocol_details.yaml", "a") as yml:
                        yaml.dump(self.raw_allowed_protocol_details.json(), yml, allow_unicode=True)
                
                    for filetype in filetype_loop:
                        parsed_allowed_protocol_details = allowed_protocol_details_template.render(to_parse_allowed_protocol_details=self.raw_allowed_protocol_details.json(),filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocol_details.%s" % filetype, "a") as fh:
                            fh.write(parsed_allowed_protocol_details)
                            fh.close()

                    # ----------------
                    # Store Devices in Device Table in Database
                    # ----------------

                    table.insert(self.raw_allowed_protocol_details.json())

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocol_details.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                                
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocol_details.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocol_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Allowed_Protocols/allowed_protocol_details_mind_map.html")
                
            fid.close()
            yml.close()

            # Get Endpoint Page Count
            with steps.start('Requesting Endpoint API Page Count',continue_=True) as step:
                try:
                    self.raw_page_count = requests.get("https://%s:9060/ers/config/endpoint?size=100" % device_ip, auth=(api_username, api_password), headers=json_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            pagecount = (self.raw_page_count.json()['SearchResult']['total'])

            # Define Templates 
            endpoints_template = env.get_template('endpoints.j2')
            endpoint_details_template = env.get_template('endpoint_details.j2')

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Name,ISE ID")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.md",'a') as md:
                md.seek(0, 0)
                md.write("# Endpoints")
                md.write("\n")
                md.write("| Name | ISE ID |")
                md.write("\n")
                md.write("| ---- | ------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Endpoints</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Name</th><th>ISE ID</th></tr>")
                html.close() 

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Name,MAC Address,Group ID,ISE ID,Identity Store,Identity Store ID,Portal User,Profile ID,Static Group,Static Profile")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.md",'a') as md:
                md.seek(0, 0)
                md.write("# Endpoint Details")
                md.write("\n")
                md.write("| Name | MAC Address | Group ID | ISE ID | Identity Store | Identity Store ID | Portal User | Profile ID | Static Group | Static Profile |")
                md.write("\n")
                md.write("| ---  | ----------- | -------- | ------ | -------------- | ----------------- | ----------- | ---------- | ------------ | -------------- |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>Endpoint Details</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Name</th><th>MAC Address</th><th>Group ID</th><th>ISE ID</th><th>Identity Store</th><th>Identity Store ID</th><th>Portal User</th><th>Profile ID</th><th>Static Group</th><th>Static Profile</th></tr>")
                html.close()

            # Get Parent Endpoints
            for page in range(1,math.ceil(pagecount/100+1)):
                with steps.start('Requesting Master List of Endpoints Information',continue_=True) as step:
                    try:
                        self.raw_endpoint_details = requests.get("https://%s:9060/ers/config/endpoint?size=100&page=%i" % (device_ip,page), auth=(api_username, api_password), headers=json_headers, verify=False,)
                        print(Panel.fit(Text.from_markup(CLOUD)))
                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                # ---------------------------------------
                # Generate CSV / MD / HTML / Mind Maps
                # ---------------------------------------

                # Parent Endpoints
                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))       

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.json", "a") as fid:
                        json.dump(self.raw_endpoint_details.json(), fid, indent=4, sort_keys=True)
                        fid.write('\n')
                                
                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.yaml", "a") as yml:
                        yaml.dump(self.raw_endpoint_details.json(), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_endpoint_details = endpoints_template.render(to_parse_endpoint_details=self.raw_endpoint_details.json(),filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.%s" % filetype, "a") as fh:
                            fh.write(parsed_endpoint_details)
                            fh.close()

                    # ----------------
                    # Store Devices in Device Table in Database
                    # ----------------

                    table.insert(self.raw_endpoint_details.json())

                # Get Child Network Devices

                for device in self.raw_endpoints.json()['SearchResult']['resources']:
                    with steps.start('Requesting Individual Endpoint Information',continue_=True) as step:
                        try:
                            self.raw_endpoint_details = requests.get(device['link']['href'], auth=(api_username, api_password), headers=json_headers, verify=False,)
                            print(Panel.fit(Text.from_markup(CLOUD)))
                        except Exception as e:
                            step.failed('There was a problem with the API\n{e}'.format(e=e))
                
                    with steps.start('Store data',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))       

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.json", "a") as fid:
                            json.dump(self.raw_endpoint_details.json(), fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.yaml", "a") as yml:
                            yaml.dump(self.raw_endpoint_details.json(), yml, allow_unicode=True)
                    
                        for filetype in filetype_loop:
                            parsed_endpoint_details = endpoint_details_template.render(to_parse_endpoint_details=self.raw_endpoint_details.json(),filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.%s" % filetype, "a") as fh:
                                fh.write(parsed_endpoint_details)
                                fh.close()

                        # ----------------
                        # Store Devices in Device Table in Database
                        # ----------------

                        table.insert(self.raw_endpoint_details.json())

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                            
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoints_mind_map.html")

            fid.close()
            yml.close()

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.html", "a") as html:
                html.write("</table></body></html>")
                html.close() 
                                
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Endpoints/endpoint_details_mind_map.html")
            fid.close()
            yml.close()


            # Get Active Session Totals
            with steps.start('Requesting Active Session Totals Count',continue_=True) as step:
                try:
                    self.raw_active_session_totals = requests.get("https://%s/admin/API/mnt/Session/ActiveCount" % device_ip, auth=(api_username, api_password), headers=xml_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                if self.raw_active_session_totals is not None:
                    active_session_totals_template = env.get_template('active_session_totals.j2')

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_totals.json", "w") as fid:
                        json.dump(xmltodict.parse(self.raw_active_session_totals.content), fid, indent=4, sort_keys=True)

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_totals.yaml", "w") as yml:
                        yaml.dump(xmltodict.parse(self.raw_active_session_totals.content), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_active_session_totals = active_session_totals_template.render(to_parse_active_session_totals=xmltodict.parse(self.raw_active_session_totals.content),filetype_loop_jinja2=filetype)
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_totals.%s" % filetype, "w") as fh:
                            fh.write(parsed_active_session_totals)                   

                    # ----------------
                    # Store Active Total Sessions in Device Table in Database
                    # ----------------
                    table.insert(xmltodict.parse(self.raw_active_session_totals.content))
            
            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_totals.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_totals.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_totals_mind_map.html")

            # Get Active Session Details
            with steps.start('Requesting Active Session Details Count',continue_=True) as step:
                try:
                    self.raw_active_session_details = requests.get("https://%s/admin/API/mnt/Session/ActiveList" % device_ip, auth=(api_username, api_password), headers=xml_headers, verify=False,)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))
            
            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                if self.raw_active_session_details is not None:
                    active_session_details_template = env.get_template('active_session_details.j2')

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_details.json", "w") as fid:
                        json.dump(xmltodict.parse(self.raw_active_session_details.content), fid, indent=4, sort_keys=True)

                    with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_details.yaml", "w") as yml:
                        yaml.dump(xmltodict.parse(self.raw_active_session_details.content), yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_active_session_details = active_session_details_template.render(to_parse_active_session_details=xmltodict.parse(self.raw_active_session_details.content),filetype_loop_jinja2=filetype)
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_details.%s" % filetype, "w") as fh:
                            fh.write(parsed_active_session_details)                 

                    # ----------------
                    # Store Active Total Sessions in Device Table in Database
                    # ----------------
                    table.insert(xmltodict.parse(self.raw_active_session_details.content))

            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_totals.md"):
                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/active_session_details_totals_mind_map.html")

            # Define Templates 
            MAC_session_details_template = env.get_template('mac_session_details.j2')
                 
            # Get Active Session Details
            active_list = xmltodict.parse(self.raw_active_session_details.content)

            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.csv",'a') as csv:
                csv.seek(0, 0)
                csv.write("Timestamp,Authentication ID,Authentication Method,Authentication Protocol,User Name,IP Address,MAC Address,Switch Name,Switch IP,Switch Port,ISE Server,Audit Session ID,Policy,Execution Steps,Input Packets,Output Packets,Device Type,Identity Group,Location,Posture Status,Selected Profile,Service Type,VLAN,Message Code")
                csv.close()  
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.md",'a') as md:
                md.seek(0, 0)
                md.write("# MAC Session Details")
                md.write("\n")
                md.write("| Timestamp | Authentication ID | Authentication Method | Authentication Protocol | User Name | IP Address | MAC Address | Switch Name | Switch IP | Switch Port | ISE Server | Audit Session ID | Policy | Execution Steps | Input Packets | Output Packets | Device Type | Identity Group | Location | Posture Status | Selected Profile | Service Type | VLAN | Message Code |")
                md.write("\n")
                md.write("| --------  | ----------------- | --------------------- | ----------------------- | --------- | ---------- | ----------- | ----------- | --------- | ----------- | ---------- | ---------------- | ------ | --------------- | ------------- | -------------- | ----------- | -------------- | -------- | -------------- | ---------------- | ------------ | ---- | ------------ |")
                md.close()
            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.html",'a') as html:
                html.seek(0, 0)
                html.write("<html><body><h1>MAC Session Details</h1><table style=\"width:100%\">")
                html.write("\n")
                html.write("<tr><th>Timestamp</th><th>Authentication ID</th><th>Authentication Method</th><th>Authentication Protocol</th><th>User Name</th><th>IP Address</th><th>MAC Address</th><th>Switch Name</th><th>Switch IP</th><th>Switch Port</th><th>ISE Server</th><th>Audit Session ID</th><th>Policy</th><th>Execution Steps</th><th>Input Packets</th><th>Output Packets</th><th>Device Type</th><th>Identity Group</th><th>Location</th><th>Posture Status</th><th>Selected Profile</th><th>Service Type</th><th>VLAN</th><th>Message Code</th></tr>")
                html.close() 

            if hasattr(active_list, 'activeSession'):
                for active_session in active_list['activeList']['activeSession']:
                    with steps.start('Requesting MAC Session Information',continue_=True) as step:
                        try:
                            self.raw_mac_session_details = requests.get("https://%s/admin/API/mnt/Session/MACAddress/%s" % (device_ip,active_session['calling_station_id']), auth=(api_username, api_password), headers=xml_headers, verify=False,)
                            print(Panel.fit(Text.from_markup(CLOUD)))
                        except Exception as e:
                            step.failed('There was a problem with the API\n{e}'.format(e=e))

                    # MAC Details
                    with steps.start('Store data',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))       

                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.json", "a") as fid:
                            json.dump(xmltodict.parse(self.raw_mac_session_details.content), fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.yaml", "a") as yml:
                            yaml.dump(xmltodict.parse(self.raw_mac_session_details.content), yml, allow_unicode=True)

                        for filetype in filetype_loop:
                            parsed_MAC_session_details = MAC_session_details_template.render(to_parse_MAC_session_details=xmltodict.parse(self.raw_mac_session_details.content),filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.%s" % filetype, "a") as fh:
                                fh.write(parsed_MAC_session_details)
                                fh.close()

                        # ----------------
                        # Store Devices in Device Table in Database
                        # ----------------

                        table.insert(xmltodict.parse(self.raw_mac_session_details.content))

                with open("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.html", "a") as html:
                    html.write("</table></body></html>")
                    html.close() 
                                    
                if os.path.exists("Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.md"):
                    os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details.md --output Camelot/Cisco/DevNet_Sandbox/ISE/Active_Sessions/MAC_session_details_mind_map.html")

                fid.close()
                yml.close()

        # ---------------------------------------
        # You Made It 
        # ---------------------------------------
        db.close()
        print(Panel.fit(Text.from_markup(FINISHED)))