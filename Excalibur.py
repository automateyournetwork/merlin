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
from ascii_art import GREETING, LEARN, RUNNING, CLOUD, WRITING, SERIALS
from general_functionalities import ParseShowCommandFunction, ParseLearnFunction
from tinydb import TinyDB, Query
from requests_ntlm import HttpNtlmAuth

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

ios_template_dir = 'templates/cisco/ios'
ios_xe_template_dir = 'templates/cisco/ios_xe'
isr_template_dir = "templates/cisco/isr"
nxos_template_dir = 'templates/cisco/nxos'
cisco_api_template_dir = 'templates/cisco/api'
f5_template_dir = 'templates/f5'

ios_env = Environment(loader=FileSystemLoader(ios_template_dir))
ios_xe_env = Environment(loader=FileSystemLoader(ios_xe_template_dir))
isr_env = Environment(loader=FileSystemLoader(isr_template_dir))
nxos_env = Environment(loader=FileSystemLoader(nxos_template_dir))
cisco_api_env = Environment(loader=FileSystemLoader(cisco_api_template_dir))
f5_env = Environment(loader=FileSystemLoader(f5_template_dir))

# ----------------
# Create Database
# ----------------

if os.path.exists("Camelot/Excalibur/Inventory.json"):
    os.remove("Camelot/Excalibur/Inventory.json")

if os.path.exists("Camelot/Excalibur/Inventory.yaml"):
    os.remove("Camelot/Excalibur/Inventory.yaml")

if os.path.exists("Camelot/Excalibur/Inventory_DB.json"):
    os.remove("Camelot/Excalibur/Inventory_DB.json")       

if os.path.exists("Camelot/Excalibur/Contracts.json"):
    os.remove("Camelot/Excalibur/Contracts.json")

if os.path.exists("Camelot/Excalibur/Contracts.yaml"):
    os.remove("Camelot/Excalibur/Contracts.yaml")

if os.path.exists("Camelot/Excalibur/Contracts_DB.json"):
    os.remove("Camelot/Excalibur/Contracts_DB.json")

inventory_db = TinyDB('Camelot/Excalibur/Inventory_DB.json')
contract_db = TinyDB('Camelot/Excalibur/Contracts_DB.json')

# ----------------
# Load Credentials 
# ----------------

if os.path.exists("testbed/Excalibur_f5_testbed.yaml"):
    with open("testbed/Excalibur_f5_testbed.yaml") as stream:
        f5_testbed = yaml.safe_load(stream)

with open("api_credentials/cisco_serial2info.yaml", 'r') as f:
    cisco_api_credentials = yaml.safe_load(f)

serial_2_info_api_username = cisco_api_credentials['APIs']['serial_2_info']['serial_2_info_api_username']
serial_2_info_api_password = cisco_api_credentials['APIs']['serial_2_info']['serial_2_info_api_password']

oauth_token_raw = requests.post("https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials&client_id=%s&client_secret=%s" % (serial_2_info_api_username,serial_2_info_api_password))
oauth_token_json = oauth_token_raw.json()
oauth_headers = {"Authorization": "%s %s" % (oauth_token_json['token_type'],oauth_token_json['access_token'])}

if os.path.exists("api_credentials/sharepoint.yaml"):
    with open("api_credentials/sharepoint.yaml", 'r') as f:
        sharepoint_api_credentials = yaml.safe_load(f)

        sharepoint_inventory_api_domain = sharepoint_api_credentials['APIs']['inventory']['sharepoint_domain']
        sharepoint_inventory_api_username = sharepoint_api_credentials['APIs']['inventory']['sharepoint_user']
        sharepoint_inventory_api_password = sharepoint_api_credentials['APIs']['inventory']['sharepoint_password']    
        sharepoint_inventory_URL = sharepoint_api_credentials['APIs']['inventory']['sharePointUrl']
        sharepoint_inventory_folder = sharepoint_api_credentials['APIs']['inventory']['folderUrl']
        sharepoint_inventory_sharepoint_filename = sharepoint_api_credentials['APIs']['inventory']['sharePointFileName']
        sharepoint_inventory_upload_filename = sharepoint_api_credentials['APIs']['inventory']['uploadFileName']
        sharepoint_contracts_api_domain = sharepoint_api_credentials['APIs']['inventory']['sharepoint_domain']
        sharepoint_contracts_api_username = sharepoint_api_credentials['APIs']['contracts']['sharepoint_user']
        sharepoint_contracts_api_password = sharepoint_api_credentials['APIs']['contracts']['sharepoint_password']    
        sharepoint_contracts_URL = sharepoint_api_credentials['APIs']['contracts']['sharePointUrl']
        sharepoint_contracts_folder = sharepoint_api_credentials['APIs']['contracts']['folderUrl']
        sharepoint_contracts_sharepoint_filename = sharepoint_api_credentials['APIs']['contracts']['sharePointFileName']
        sharepoint_contracts_upload_filename = sharepoint_api_credentials['APIs']['contracts']['uploadFileName']

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
        # Create File and headers
        # ---------------------------------------
        with open("Camelot/Excalibur/Inventory.csv",'w') as csv:
            csv.seek(0, 0)
            csv.write("Hostname,Slot,Part,Description,Serial Number,Virtual ID,Subslot,Subslot Part,Subslot Description,Subslot Serial Number,SubSlot Virtual ID")
            csv.close()  
        with open("Camelot/Excalibur/Inventory.md",'w') as md:
            md.seek(0, 0)
            md.write("# Inventory")
            md.write("\n")
            md.write("| Hostname | Slot | Part | Description | Serial Number | Virtual ID | Subslot | Subslot Part | Subslot Description | Subslot Serial Number | SubSlot Virtual ID |")
            md.write("\n")
            md.write("| -------- | ---- | ---- | ----------- | ------------- | ---------- | ------- | ------------ | ------------------- | --------------------- | ------------------ |")
            md.close()
        with open("Camelot/Excalibur/Inventory.html",'w') as html:
            html.seek(0, 0)
            html.write("<html><body><h1>Inventory</h1><table style=\"width:100%\">")
            html.write("\n")
            html.write("<tr><th>Hostname</th><th>Slot</th><th>Part</th><th>Description</th><th>Serial Number</th><th>Virtual ID</th><th>Subslot</th><th>Subslot Part</th><th>Subslot Description</th><th>Subslot Serial Number</th><th>Subslot Virtual ID</th></tr>")
            html.close()        

        with open("Camelot/Excalibur/Contracts.csv",'w') as csv:
            csv.seek(0, 0)
            csv.write("Hostname,PID,Service Contract Number,Serial Number,Parent Serial Number,Under Contract,Item Description,Item Type,Warranty Type,Product Line End Date,Warranty End Date,Customer Name,Contract Address,Contract City,Contract State/Province,Contract Country")
            csv.close()                                   

        with open("Camelot/Excalibur/Contracts.md",'w') as md:
            md.seek(0, 0)
            md.write("# Serial 2 Contract Information")
            md.write("\n")
            md.write("| Hostname | PID | Service Contract Number | Serial Number | Parent Serial Number | Under Contract | Item Description | Item Type | Warranty Type | Product Line End Date | Warranty End Date | Customer Name | Contract Address | Contract City | Contract State/Province | Contract Country |")
            md.write("\n")
            md.write("| Hostname | --- | ----------------------- | ------------- | -------------------- | -------------- | ---------------- | --------- | ------------- | --------------------- | ----------------- | ------------- | ---------------- | ------------- | ----------------------- | ---------------- |")
            md.close() 

        with open("Camelot/Excalibur/Contracts.html",'w') as html:
            html.seek(0, 0)
            html.write("<html><body><h1>Serial 2 Contract Infromation</h1><table style=\"width:100%\">")
            html.write("\n")
            html.write("<tr><th>Hostname</th><th>PID</th><th>Service Contract Number</th><th>Serial Number</th><th>Parent Serial Number</th><th>Under Contract</th><th>Item Description</th><th>tem Type</th><th>Warranty Type</th><th>Product Line End Date</th><th>Warranty End Date</th><th>Customer Name</th><th>Contract Address</th><th>Contract City</th><th>Contract State/Province</th><th>Contract Country</th></tr>")                     
            html.close()

        # ---------------------------------------
        # Loop over devices
        # ---------------------------------------
        for device in testbed:
            # ----------------
            # Create a table in the database
            # ----------------
            table = inventory_db.table(device.alias)
            table = contract_db.table(device.alias)

            # ---------------------------------------
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING)))

            # Show Interface Transceiver (NXOS)
            if device.os == "nxos":
                self.parsed_show_interface_transceiver = ParseShowCommandFunction.parse_show_command(steps, device, "show interface transceiver")

            # Show Inventory
            self.parsed_show_inventory = ParseShowCommandFunction.parse_show_command(steps, device, "show inventory")

            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            
            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                ###############################
                # Genie Show Command Section
                ###############################

                # Show Interface Transceiver
                if device.os == "nxos":
                    if self.parsed_show_interface_transceiver is not None:
                        # NXOS
                        sh_interface_transceiver_template = nxos_env.get_template('excalibur_show_interface_transceiver.j2')
                    
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_interface_transceiver, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_interface_transceiver, yml, allow_unicode=True)

                        for filetype in filetype_loop:
                            parsed_interface_transceiver = sh_interface_transceiver_template.render(to_parse_interface=self.parsed_show_interface_transceiver,hostname=device.alias,filetype_loop_jinja2=filetype)

                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_interface_transceiver)
                            
                    # ----------------
                    # Store Inventory in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_inventory)

                # Show Inventory
                if self.parsed_show_inventory is not None:
                    # 3560
                    sh_inventory_2960_template = ios_env.get_template('excalibur_show_inventory_2960.j2')

                    # 3560
                    sh_inventory_3560_template = ios_env.get_template('excalibur_show_inventory_3560.j2')

                    # 3750
                    sh_inventory_3750_template = ios_env.get_template('excalibur_show_inventory_3750.j2')

                    # 6500
                    sh_inventory_6500_template = ios_env.get_template('excalibur_show_inventory_6500.j2')

                    # 3850
                    sh_inventory_3850_template = ios_xe_env.get_template('excalibur_show_inventory_3850.j2')

                    # 4500
                    sh_inventory_4500_template = ios_xe_env.get_template('excalibur_show_inventory_4500.j2')

                    # 9300
                    sh_inventory_9300_template = ios_xe_env.get_template('excalibur_show_inventory_9300.j2')

                    # ISR
                    sh_inventory_isr_template = isr_env.get_template('excalibur_show_inventory_isr.j2')

                    # NXOS
                    sh_inventory_nxos_template = nxos_env.get_template('excalibur_show_inventory_nxos.j2')
                    
                    # 4500
                    if device.platform == "cat4500":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)  

                        for filetype in filetype_loop:
                            parsed_4500_inventory = sh_inventory_4500_template.render(to_parse_inventory=self.parsed_show_inventory['main'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_4500_inventory)                 
                    # 3850
                    elif device.platform == "cat3850":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)    
                             
                        for filetype in filetype_loop:
                            parsed_3850_inventory = sh_inventory_3850_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_3850_inventory)
                        
                    # 9300
                    elif device.platform == "c9300":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_9300_inventory = sh_inventory_9300_template.render(to_parse_inventory=self.parsed_show_inventory['index'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                        
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:    
                                fh.write(parsed_9300_inventory)

                    # ISR
                    elif device.platform == "isr":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_isr_inventory = sh_inventory_isr_template.render(to_parse_inventory=self.parsed_show_inventory,hostname=device.alias,filetype_loop_jinja2=filetype)                    
                        
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:    
                                fh.write(parsed_isr_inventory)

                    # 2960
                    elif device.platform == "cat2960":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_2960_inventory = sh_inventory_2960_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_2960_inventory)

                    # 3560
                    elif device.platform == "cat3560":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_3560_inventory = sh_inventory_3560_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_3560_inventory)

                    # 3750
                    elif device.platform == "cat3750":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_3750_inventory = sh_inventory_3750_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_3750_inventory)

                    # 6500
                    elif device.platform == "cat6500":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_6500_inventory = sh_inventory_6500_template.render(to_parse_inventory=self.parsed_show_inventory['main']['chassis'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_6500_inventory)                        

                    # NXOS
                    elif device.os == "nxos":
                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_nxos_inventory = sh_inventory_nxos_template.render(to_parse_inventory=self.parsed_show_inventory['name'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                        
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_nxos_inventory)                          
                            
                    # ----------------
                    # Store Inventory in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_inventory)

                    # Serial 2 Info Template
                    serial_2_info_template = cisco_api_env.get_template('excalibur_serial_2_info.j2')

                    print(Panel.fit(Text.from_markup(CLOUD)))
                    if device.platform == "cat2960":
                        for slot,value in self.parsed_show_inventory.items():
                            for slot_number,value in value.items():
                                for rp,value in value.items():
                                    for part,value in value.items():
                                        time.sleep(1)
                                        with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                            try:                                      
                                                serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                                serial_2_info_json = serial_2_info_raw.json()
                                                with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                    json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                    fid.write('\n')

                                                with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                    yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                    yml.write('\n')

                                                for filetype in filetype_loop:
                                                    parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                    with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                        fh.write(parsed_output_type)

                                            except Exception as e:
                                                step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                        for slot,value in self.parsed_show_inventory.items():
                            for slot_number,value in value.items():
                                for rp,value in value.items():
                                    for part,value in value.items():
                                        for subslot,value in value['subslot'].items():
                                            for part,value in value.items():
                                                time.sleep(1)
                                                with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                                    try:                                      
                                                        serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                                        serial_2_info_json = serial_2_info_raw.json()
                                                        with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                            json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                            fid.write('\n')

                                                        with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                            yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                            yml.write('\n')
    
                                                        for filetype in filetype_loop:
                                                            parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                            with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                                fh.write(parsed_output_type)

                                                    except Exception as e:
                                                        step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                    if device.platform == "cat3560":
                        for slot,value in self.parsed_show_inventory.items():
                            for slot_number,value in value.items():
                                for rp,value in value.items():
                                    for part,value in value.items():
                                        time.sleep(1)
                                        with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                            try:                                      
                                                serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                                serial_2_info_json = serial_2_info_raw.json()
                                                with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                    json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                    fid.write('\n')

                                                with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                    yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                    yml.write('\n')

                                                for filetype in filetype_loop:
                                                    parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                    with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                        fh.write(parsed_output_type)

                                            except Exception as e:
                                                step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                        for slot,value in self.parsed_show_inventory.items():
                            for slot_number,value in value.items():
                                for rp,value in value.items():
                                    for part,value in value.items():
                                        for subslot,value in value['subslot'].items():
                                            for part,value in value.items():
                                                time.sleep(1)
                                                with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                                    try:                                      
                                                        serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                                        serial_2_info_json = serial_2_info_raw.json()
                                                        with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                            json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                            fid.write('\n')

                                                        with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                            yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                            yml.write('\n')
    
                                                        for filetype in filetype_loop:
                                                            parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                            with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                                fh.write(parsed_output_type)

                                                    except Exception as e:
                                                        step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                    if device.platform == "cat3750":
                        for slot,value in self.parsed_show_inventory.items():
                            for slot_number,value in value.items():
                                for rp,value in value.items():
                                    for part,value in value.items():
                                        time.sleep(1)
                                        with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                            try:                                      
                                                serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                                serial_2_info_json = serial_2_info_raw.json()
                                                with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                    json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                    fid.write('\n')

                                                with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                    yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                    yml.write('\n')

                                                for filetype in filetype_loop:
                                                    parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                    with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                        fh.write(parsed_output_type)

                                            except Exception as e:
                                                step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                        for slot,value in self.parsed_show_inventory.items():
                            for slot_number,value in value.items():
                                for rp,value in value.items():
                                    for part,value in value.items():
                                        for subslot,value in value['subslot'].items():
                                            for part,value in value.items():
                                                time.sleep(1)
                                                with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                                    try:                                      
                                                        serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                                        serial_2_info_json = serial_2_info_raw.json()
                                                        with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                            json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                            fid.write('\n')

                                                        with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                            yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                            yml.write('\n')
    
                                                        for filetype in filetype_loop:
                                                            parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                            with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                                fh.write(parsed_output_type)

                                                    except Exception as e:
                                                        step.failed('There was a problem with the API\n{e}'.format(e=e))   

                    if device.platform == "cat4500":
                        for part,value in self.parsed_show_inventory.items():
                            for pid,value in value.items():
                                for sn,value in value.items():
                                    time.sleep(1)
                                    with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                        try:                                      
                                            serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                            serial_2_info_json = serial_2_info_raw.json()
                                            with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                fid.write('\n')

                                            with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                yml.write('\n')

                                            for filetype in filetype_loop:
                                                parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                    fh.write(parsed_output_type)

                                        except Exception as e:
                                            step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                    if device.platform == "cat6500":
                        for part,value in self.parsed_show_inventory.items():
                            for pid,value in value.items():
                                for sn,value in value.items():
                                    time.sleep(1)
                                    with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                        try:                                      
                                            serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                            serial_2_info_json = serial_2_info_raw.json()
                                            with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                fid.write('\n')

                                            with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                yml.write('\n')

                                            for filetype in filetype_loop:
                                                parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                    fh.write(parsed_output_type)

                                        except Exception as e:
                                            step.failed('There was a problem with the API\n{e}'.format(e=e)) 

                    if device.platform == "isr":
                        for part,value in self.parsed_show_inventory['main'].items():
                            for chassis,value in value.items():
                                time.sleep(1)                          
                                with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                    try:                                      
                                        serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                        serial_2_info_json = serial_2_info_raw.json()
                                        with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                            json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                            fid.write('\n')

                                        with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                            yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                            yml.write('\n')

                                        for filetype in filetype_loop:
                                            parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                            with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                fh.write(parsed_output_type)

                                    except Exception as e:
                                        step.failed('There was a problem with the API\n{e}'.format(e=e)) 

                        for part,value in self.parsed_show_inventory['slot'].items():
                            for slot,value in value.items():                          
                                for part,value in value.items():
                                    time.sleep(1)
                                    with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                        try:                                      
                                            serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['sn'], headers=oauth_headers)
                                            serial_2_info_json = serial_2_info_raw.json()
                                            with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                fid.write('\n')

                                            with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                yml.write('\n')

                                            for filetype in filetype_loop:
                                                parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                    fh.write(parsed_output_type)

                                        except Exception as e:
                                            step.failed('There was a problem with the API\n{e}'.format(e=e)) 

                    if device.platform == "cat3850":
                        for slot,value01 in self.parsed_show_inventory['slot'].items():
                            for pid,value02 in value01.items():
                                for part,value03 in value02.items():
                                    time.sleep(1)
                                    with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                        try:                                      
                                            serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value03['sn'], headers=oauth_headers)
                                            serial_2_info_json = serial_2_info_raw.json()
                                            with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                                json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                                fid.write('\n')

                                            with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                                yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                                yml.write('\n')

                                            for filetype in filetype_loop:
                                                parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                                with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                    fh.write(parsed_output_type)    
                                                                                            
                                        except Exception as e:
                                            step.failed('There was a problem with the API\n{e}'.format(e=e))                                        

                    if device.platform == "nxos":
                        for slot,value in self.parsed_show_inventory.items():
                            for pid,value in value.items():
                                time.sleep(1)                
                                with steps.start('Calling the Cisco Serial 2 Info REST API',continue_=True) as step:
                                    try:    
                                        serial_2_info_raw = requests.get("https://api.cisco.com/sn2info/v2/coverage/summary/serial_numbers/%s" % value['serial_number'], headers=oauth_headers)
                                        serial_2_info_json = serial_2_info_raw.json()
                                        with open("Camelot/Excalibur/Contracts.json", "a") as fid:
                                            json.dump(serial_2_info_json, fid, indent=4, sort_keys=True)
                                            fid.write('\n')

                                        with open("Camelot/Excalibur/Contracts.yaml", "a") as yml:
                                            yaml.dump(serial_2_info_json, yml, allow_unicode=True)
                                            yml.write('\n')

                                        for filetype in filetype_loop:
                                            parsed_output_type = serial_2_info_template.render(to_parse_serial_2_info=serial_2_info_json['serial_numbers'],hostname=device.alias,filetype_loop_jinja2=filetype)

                                            with open("Camelot/Excalibur/Contracts.%s" % filetype, "a") as fh:
                                                fh.write(parsed_output_type)  

                                    except Exception as e:
                                        step.failed('There was a problem with the API\n{e}'.format(e=e))

        # ----------------
        # F5
        # ----------------

        if os.path.exists("testbed/Serial_excalibur_f5_testbed.yaml"):
            for device,value in f5_testbed['devices'].items():
                api_username = f5_testbed["devices"][device]["credentials"]["default"]["username"]
                api_password = f5_testbed["devices"][device]["credentials"]["default"]["password"]
                device_alias = f5_testbed["devices"][device]["alias"]
                f5_token_raw = requests.post("https://%s/mgmt/shared/authn/login" % device, json={"username":"%s" % api_username, "password": "%s" % api_password,"loginprovidername": "tmos"}, verify=False)
                f5_token_json = f5_token_raw.json()
                f5_usable_token = f5_token_json["token"]["token"]

                headers={"X-F5-Auth-Token":f5_usable_token}

            for device in f5_testbed['devices']:
                print(Panel.fit(Text.from_markup(RUNNING)))

                # SFP Serial
                with steps.start('Requesting SFP Serial API Information',continue_=True) as step:
                    try:
                        self.raw_sfp_serial = requests.get("https://%s/mgmt/tm/net/interface" % device_alias, headers=headers, verify=False)
                        print(Panel.fit(Text.from_markup(CLOUD)))

                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                # License
                with steps.start('Requesting License API Information',continue_=True) as step:
                    try:
                        self.raw_license = requests.get("https://%s/mgmt/tm/sys/license" % device_alias, headers=headers, verify=False)
                        print(Panel.fit(Text.from_markup(CLOUD)))

                    except Exception as e:
                        step.failed('There was a problem with the API\n{e}'.format(e=e))

                with steps.start('Store data',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))

                    if self.raw_sfp_serial is not None:
                        self.raw_sfp_serial = self.raw_sfp_serial.json()
                        # F5 SFP
                        sh_inventory_f5_sfp_template = f5_env.get_template('excalibur_sfp_serial_api.j2')

                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.raw_sfp_serial, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.raw_sfp_serial, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_f5_sfp_inventory = sh_inventory_f5_sfp_template.render(to_parse_inventory=self.raw_sfp_serial['items'],hostname=device_alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_f5_sfp_inventory) 

                    if self.raw_license is not None:
                        self.raw_license = self.raw_license.json()
                        # F5 License
                        sh_inventory_f5_license_template = f5_env.get_template('excalibur_license_api.j2')

                        with open("Camelot/Excalibur/Inventory.json", "a") as fid:
                            json.dump(self.raw_license, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Excalibur/Inventory.yaml", "a") as yml:
                            yaml.dump(self.raw_license, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_f5_license_inventory = sh_inventory_f5_license_template.render(to_parse_inventory=self.raw_license['entries'],hostname=device_alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Excalibur/Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_f5_license_inventory) 

        with open("Camelot/Excalibur/Inventory.html", "a") as html:
            html.write("</table></body></html>")
            html.close() 
                            
        if os.path.exists("Camelot/Excalibur/Inventory.md"):
            os.system("markmap --no-open Camelot/Excalibur/Inventory.md --output Camelot/Excalibur/Inventory_mind_map.html")

            fh.close()
            fid.close()
            yml.close()

        with open("Camelot/Excalibur/Contracts.html", "a") as html:
            html.write("</table></body></html>")
            html.close()             

        if os.path.exists("Camelot/Excalibur/Contracts.md"):
            os.system("markmap --no-open Camelot/Excalibur/Contracts.md --output Camelot/Excalibur/Contracts_mind_map.html")

        # SHAREPOINT # 

        if os.path.exists("api_credentials/sharepoint.yaml"):
            with steps.start('Send to Sharepoint',continue_=True) as step:
                # Inventory
                #Sets up the url for requesting a file upload

                inventoryRequestUrl = sharepoint_inventory_URL + '/_api/web/getfolderbyserverrelativeurl(\'' + sharepoint_inventory_folder + '\')/Files/add(url=\'' + sharepoint_inventory_upload_filename + '\',overwrite=true)'

                #Read in the file that we are going to upload

                file = open(sharepoint_inventory_sharepoint_filename, 'rb')

                #Setup the required headers for communicating with SharePoint 

                headers = {'Content-Type': 'application/json; odata=verbose', 'accept': 'application/json;odata=verbose'}

                #Execute a request to get the FormDigestValue. This will be used to authenticate our upload request

                r = requests.post(sharepoint_inventory_URL + "/_api/contextinfo",auth=HttpNtlmAuth('%s\\%s' % (sharepoint_inventory_api_domain,sharepoint_inventory_api_username),'%s' % sharepoint_inventory_api_password), headers=headers, verify=False)
                formDigestValue = r.json()['d']['GetContextWebInformation']['FormDigestValue']

                #Update headers to use the newly acquired FormDigestValue

                headers = {'Content-Type': 'application/json; odata=verbose', 'accept': 'application/json;odata=verbose', 'x-requestdigest' : formDigestValue}

                #Execute the request. If you run into issues, inspect the contents of uploadResult

                uploadResult = requests.post(inventoryRequestUrl,auth=HttpNtlmAuth('%s\\%s' % (sharepoint_inventory_api_domain,sharepoint_inventory_api_username),'%s' % sharepoint_inventory_api_password), headers=headers, verify=False, data=file.read())

                # Inventory
                #Sets up the url for requesting a file upload

                contractRequestUrl = sharepoint_contracts_URL + '/_api/web/getfolderbyserverrelativeurl(\'' + sharepoint_contracts_folder + '\')/Files/add(url=\'' + sharepoint_contracts_upload_filename + '\',overwrite=true)'
                #Read in the file that we are going to upload

                file = open(sharepoint_contracts_sharepoint_filename, 'rb')

                #Setup the required headers for communicating with SharePoint 

                headers = {'Content-Type': 'application/json; odata=verbose', 'accept': 'application/json;odata=verbose'}

                #Execute a request to get the FormDigestValue. This will be used to authenticate our upload request

                r = requests.post(sharepoint_contracts_URL + "/_api/contextinfo",auth=HttpNtlmAuth('%s\\%s' % (sharepoint_inventory_api_domain,sharepoint_inventory_api_username),'%s' % sharepoint_inventory_api_password), headers=headers, verify=False)
                formDigestValue = r.json()['d']['GetContextWebInformation']['FormDigestValue']

                #Update headers to use the newly acquired FormDigestValue

                headers = {'Content-Type': 'application/json; odata=verbose', 'accept': 'application/json;odata=verbose', 'x-requestdigest' : formDigestValue}

                #Execute the request. If you run into issues, inspect the contents of uploadResult

                uploadResult = requests.post(contractRequestUrl,auth=HttpNtlmAuth('%s\\%s' % (sharepoint_inventory_api_domain,sharepoint_inventory_api_username),'%s' % sharepoint_inventory_api_password), headers=headers, verify=False, data=file.read())

        inventory_db.close()
        contract_db.close()
        # Goodbye Banner
        print(Panel.fit(Text.from_markup(SERIALS)))