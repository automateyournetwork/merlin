# ----------------
# Copyright
# ----------------
# Written by John Capobianco, March 2021
# Copyright (c) 2021 John Capobianco

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
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, LEARN, RUNNING, WRITING, FINISHED
from general_functionalities import ParseShowCommandFunction

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

template_dir = 'templates/cisco/api'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        print(Panel.fit(Text.from_markup(GREETING)))
        testbed.connect()

# ----------------
# Test Case #1
# ----------------
class Collect_Information(aetest.Testcase):
    """Parse all the commands"""

    @aetest.test
    def parse(self, testbed, section, steps):
        """ Testcase Setup section """
        # ---------------------------------------
        # Loop over devices
        # ---------------------------------------
        for device in testbed:
            # ---------------------------------------
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING)))

            # Show Inventory
            self.parsed_show_inventory = ParseShowCommandFunction.parse_show_command(steps, device, "show inventory")

            # Show Version
            self.parsed_show_version = ParseShowCommandFunction.parse_show_command(steps, device, "show version")

            # ---------------------------------------
            # Send Version / Serial Numbers to Cisco APIs 
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed API Data
            # ---------------------------------------         
            
            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                
                # Show version
                if hasattr(self, 'parsed_show_version'):
                    recommended_release_template = env.get_template('recommended_release.j2')
                    psirt_template = env.get_template('psirt.j2')

                    with open("api_credentials/cisco.yaml", 'r') as f:
                        api_credentials = yaml.safe_load(f)

                    recommended_release_api_username = api_credentials['APIs']['recommended_release']['recommended_release_api_username']
                    recommended_release_api_password = api_credentials['APIs']['recommended_release']['recommended_release_api_password']

                    oauth_token_raw = requests.post("https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id=%s&client_secret=%s" % (recommended_release_api_username,recommended_release_api_password))
                    oauth_token_json = oauth_token_raw.json()
                    oauth_headers = {"Authorization": "%s %s" % (oauth_token_json['token_type'],oauth_token_json['access_token'])}

                    print(Panel.fit(Text.from_markup(CLOUD)))
                    for version,value in self.parsed_show_version.items():
                        if device.platform == "cat4500":
                            with steps.start('Calling API',continue_=True) as step:
                                try:
                                    recommended_release_raw = requests.get("https://api.cisco.com/software/suggestion/v2/suggestions/software/productIds/WS-C4500X-32SFP+", headers=oauth_headers)
                                except Exception as e:
                                    step.failed('Could not parse it correctly\n{e}'.format(e=e))                           
                        else:
                            with steps.start('Calling API',continue_=True) as step:
                                try:
                                    recommended_release_raw = requests.get("https://api.cisco.com/software/suggestion/v2/suggestions/software/productIds/%s" % value['chassis'], headers=oauth_headers)
                                except Exception as e:
                                    step.failed('Could not parse it correctly\n{e}'.format(e=e))                           
                        
                        recommended_release_json = recommended_release_raw.json()

                        with open("Camelot/Cisco/APIs/Recommended_Release/%s_recommended_release.json" % device.alias, "w") as fid:
                          json.dump(recommended_release_json, fid, indent=4, sort_keys=True)

                        with open("Camelot/Cisco/APIs/Recommended_Release/%s_recommended_release.yaml" % device.alias, "w") as yml:
                          yaml.dump(recommended_release_json, yml, allow_unicode=True)

                        for filetype in filetype_loop:
                            parsed_output_type = recommended_release_template.render(to_parse_recommended=recommended_release_json['productList'],installed_version=value['system_image'],filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/APIs/Recommended_Release/%s_recommended_release.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/APIs/Recommended_Release/%s_recommended_release.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/APIs/Recommended_Release/%s_recommended_release.md --output Camelot/Cisco/APIs/Recommended_Release/%s_recommended_release_mind_map.html" % (device.alias,device.alias))

                    with open("api_credentials/cisco.yaml", 'r') as f:
                        api_credentials = yaml.safe_load(f)

                    psirt_api_username = api_credentials['APIs']['psirt']['psirt_api_username']
                    psirt_api_password = api_credentials['APIs']['psirt']['psirt_api_password']

                    oauth_token_raw = requests.post("https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id=%s&client_secret=%s" % (psirt_api_username,psirt_api_password))
                    oauth_token_json = oauth_token_raw.json()
                    oauth_headers = {"Authorization": "%s %s" % (oauth_token_json['token_type'],oauth_token_json['access_token'])}

                    print(Panel.fit(Text.from_markup(CLOUD)))
                    for version,value in self.parsed_show_version.items():
                        with steps.start('Calling API',continue_=True) as step:
                            try:
                                psirt_raw = requests.get("https://api.cisco.com/security/advisories/iosxe?version=%s" % value['version'], headers=oauth_headers)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))                           
                        
                        psirt_json = psirt_raw.json()

                        with open("Camelot/Cisco/APIs/PSIRT/%s_PSIRT_report.json" % device.alias, "w") as fid:
                          json.dump(psirt_json, fid, indent=4, sort_keys=True)

                        with open("Camelot/Cisco/APIs/PSIRT/%s_PSIRT_report.yaml" % device.alias, "w") as yml:
                          yaml.dump(psirt_json, yml, allow_unicode=True)

                        for filetype in filetype_loop:
                            parsed_output_type = psirt_template.render(to_parse_psirt=psirt_json['advisories'],filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/APIs/PSIRT/%s_PSIRT_report.%s" % (device.alias,filetype), "w") as fh:
                                fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/APIs/PSIRT/%s_PSIRT_report.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/APIs/PSIRT/%s_PSIRT_report.md --output Camelot/Cisco/APIs/PSIRT/%s_PSIRT_report_mind_map.html" % (device.alias,device.alias))

                # Show Inventory
                if hasattr(self, 'parsed_show_inventory'):
                    serial_2_info_4500_template = env.get_template('serial_2_info.j2')
                    serial_2_info_3850_template = env.get_template('serial_2_info.j2')
                    serial_2_info_9300_template = env.get_template('serial_2_info.j2')

                    with open("api_credentials/cisco.yaml", 'r') as f:
                        api_credentials = yaml.safe_load(f)

                    serial_2_info_api_username = api_credentials['APIs']['serial_2_info']['serial_2_info_api_username']
                    serial_2_info_api_password = api_credentials['APIs']['serial_2_info']['serial_2_info_api_password']

                    oauth_token_raw = requests.post("https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id=%s&client_secret=%s" % (serial_2_info_api_username,serial_2_info_api_password))
                    oauth_token_json = oauth_token_raw.json()
                    oauth_headers = {"Authorization": "%s %s" % (oauth_token_json['token_type'],oauth_token_json['access_token'])}

                    if os.path.exists("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.json.json" % (device.alias)):
                       os.remove("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.json.json" % (device.alias))

                    if os.path.exists("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.yaml" % (device.alias)):
                       os.remove("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.yaml" % (device.alias))

                    for filetype in filetype_loop:
                        if os.path.exists("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.%s" % (device.alias,filetype)):
                            os.remove("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.%s" % (device.alias,filetype))

                    with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.csv" % device.alias,'a') as csv:
                        csv.seek(0, 0)
                        csv.write("PID,Service Contract Number,Serial Number,Parent Serial Number,Under Contract,Item Description,Item Type,Warranty Type,Product Line End Date,Warranty End Date,Customer Name,Contract Address,Contract City,Contract State/Province,Contract Country")
                    csv.close()                                   

                    with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.md" % device.alias,'a') as md:
                        md.seek(0, 0)
                        md.write("# Serial 2 Contract Information")
                        md.write("\n")
                        md.write("| PID | Service Contract Number | Serial Number | Parent Serial Number | Under Contract | Item Description | Item Type | Warranty Type | Product Line End Date | Warranty End Date | Customer Name | Contract Address | Contract City | Contract State/Province | Contract Country |")
                        md.write("\n")
                        md.write("| --- | ----------------------- | ------------- | -------------------- | -------------- | ---------------- | --------- | ------------- | --------------------- | ----------------- | ------------- | ---------------- | ------------- | ----------------------- | ---------------- |")
                    md.close() 

                    with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.html" % device.alias,'a') as html:
                        html.seek(0, 0)
                        html.write("<html><body><h1>Serial 2 Contract Infromation</h1><table style=\"width:100%\">")
                        html.write("\n")
                        html.write("<tr><th>PID</th><th>Service Contract Number</th><th>Serial Number</th><th>Parent Serial Number</th><th>Under Contract</th><th>Item Description</th><th>tem Type</th><th>Warranty Type</th><th>Product Line End Date</th><th>Warranty End Date</th><th>Customer Name</th><th>Contract Address</th><th>Contract City</th><th>Contract State/Province</th><th>Contract Country</th></tr>")                     
                    html.close()

                    print(Panel.fit(Text.from_markup(CLOUD)))
                    if device.platform == "cat4500":
                        for part,value in self.parsed_show_inventory.items():
                            for pid,value in value.items():
                                for sn,value in value.items():
                                    time.sleep(5)
                                    with steps.start('Calling API',continue_=True) as step:
                                        try:                                      
                                            serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                            serial_2_info_json = serial_2_info_raw.json()
                                            with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.json" % device.alias, "a") as fid:
                                                json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                fid.write('\n')

                                            with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.yaml" % device.alias, "a") as yml:
                                                yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                yml.write('\n')

                                            for filetype in filetype_loop:
                                                parsed_output_type = serial_2_info_4500_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],filetype_loop_jinja2=filetype)

                                                with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.%s" % (device.alias,filetype), "a") as fh:
                                                    fh.write(parsed_output_type)

                                        except Exception as e:
                                            step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                    if device.platform == "cat3850":
                        for slot,value01 in self.parsed_show_inventory['slot'].items():
                            for pid,value02 in value01.items():
                                for part,value03 in value02.items():
                                    time.sleep(5)
                                    with steps.start('Calling API',continue_=True) as step:
                                        try:                                      
                                            serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value03['sn'], headers=oauth_headers)
                                            serial_2_info_json = serial_2_info_raw.json()
                                            with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.json" % device.alias, "a") as fid:
                                                json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                fid.write('\n')

                                            with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.yaml" % device.alias, "a") as yml:
                                                yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                yml.write('\n')

                                            for filetype in filetype_loop:
                                                parsed_output_type = serial_2_info_3850_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],filetype_loop_jinja2=filetype)

                                                with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.%s" % (device.alias,filetype), "a") as fh:
                                                    fh.write(parsed_output_type)    
                                                                                            
                                        except Exception as e:
                                            step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                    if device.platform == "cat9300":
                        for slot,value01 in self.parsed_show_inventory['slot'].items():
                            for pid,value02 in value01.items():
                                for part,value03 in value02.items():                 
                                    time.sleep(5)
                                    with steps.start('Calling API',continue_=True) as step:
                                        try:    
                                            serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value03['sn'], headers=oauth_headers)
                                            serial_2_info_json = serial_2_info_raw.json()
                                            with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.json" % device.alias, "a") as fid:
                                                json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                fid.write('\n')

                                            with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.yaml" % device.alias, "a") as yml:
                                                yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                yml.write('\n')

                                            for filetype in filetype_loop:
                                                parsed_output_type = serial_2_info_9300_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],filetype_loop_jinja2=filetype)

                                                with open("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.%s" % (device.alias,filetype), "a") as fh:
                                                    fh.write(parsed_output_type)  

                                        except Exception as e:
                                            step.failed('There was a problem with the APIy\n{e}'.format(e=e))                                        

                        fh.close()
                        fid.close()
                        yml.close()

                    if os.path.exists("Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info.md --output Camelot/Cisco/APIs/Serial_2_Info/%s_serial_2_info_mind_map.html" % (device.alias,device.alias))
                    
        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED)))            