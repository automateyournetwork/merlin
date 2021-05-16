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

if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json"):
    os.remove("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json")

if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml"):
    os.remove("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml")

if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory_DB.json"):
    os.remove("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory_DB.json")       

CSR_Inventory_DB = TinyDB('Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory_DB.json')

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
        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.csv",'w') as csv:
            csv.seek(0, 0)
            csv.write("Hostname,Slot,Part,Description,Serial Number,Virtual ID,Subslot,Subslot Part,Subslot Description,Subslot Serial Number,SubSlot Virtual ID")
            csv.close()  
        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.md",'w') as md:
            md.seek(0, 0)
            md.write("# Inventory")
            md.write("\n")
            md.write("| Hostname | Slot | Part | Description | Serial Number | Virtual ID | Subslot | Subslot Part | Subslot Description | Subslot Serial Number | SubSlot Virtual ID |")
            md.write("\n")
            md.write("| -------- | ---- | ---- | ----------- | ------------- | ---------- | ------- | ------------ | ------------------- | --------------------- | ------------------ |")
            md.close()
        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.html",'w') as html:
            html.seek(0, 0)
            html.write("<html><body><h1>Inventory</h1><table style=\"width:100%\">")
            html.write("\n")
            html.write("<tr><th>Hostname</th><th>Slot</th><th>Part</th><th>Description</th><th>Serial Number</th><th>Virtual ID</th><th>Subslot</th><th>Subslot Part</th><th>Subslot Description</th><th>Subslot Serial Number</th><th>Subslot Virtual ID</th></tr>")
            html.close()        

        # ---------------------------------------
        # Loop over devices
        # ---------------------------------------
        for device in testbed:
            # ----------------
            # Create a table in the database
            # ----------------
            table = CSR_Inventory_DB.table(device.alias)

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
                    
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_interface_transceiver, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                                
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_interface_transceiver, yml, allow_unicode=True)

                        for filetype in filetype_loop:
                            parsed_interface_transceiver = sh_interface_transceiver_template.render(to_parse_interface=self.parsed_show_interface_transceiver,hostname=device.alias,filetype_loop_jinja2=filetype)

                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:
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
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)  

                        for filetype in filetype_loop:
                            parsed_4500_inventory = sh_inventory_4500_template.render(to_parse_inventory=self.parsed_show_inventory['main'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_4500_inventory)                 
                    # 3850
                    elif device.platform == "cat3850":
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)    
                             
                        for filetype in filetype_loop:
                            parsed_3850_inventory = sh_inventory_3850_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_3850_inventory)
                        
                    # 9300
                    elif device.platform == "c9300":
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_9300_inventory = sh_inventory_9300_template.render(to_parse_inventory=self.parsed_show_inventory['index'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                        
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:    
                                fh.write(parsed_9300_inventory)

                    # ISR
                    elif device.platform == "isr":
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_isr_inventory = sh_inventory_isr_template.render(to_parse_inventory=self.parsed_show_inventory,hostname=device.alias,filetype_loop_jinja2=filetype)                    
                        
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:    
                                fh.write(parsed_isr_inventory)

                    # 2960
                    elif device.platform == "cat2960":
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_2960_inventory = sh_inventory_2960_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_2960_inventory)

                    # 3560
                    elif device.platform == "cat3560":
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_3560_inventory = sh_inventory_3560_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_3560_inventory)

                    # 3750
                    elif device.platform == "cat3750":
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_3750_inventory = sh_inventory_3750_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_3750_inventory)

                    # 6500
                    elif device.platform == "cat6500":
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_6500_inventory = sh_inventory_6500_template.render(to_parse_inventory=self.parsed_show_inventory['main']['chassis'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                            
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_6500_inventory)                        

                    # NXOS
                    elif device.os == "nxos":
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.json", "a") as fid:
                            json.dump(self.parsed_show_inventory, fid, indent=4, sort_keys=True)
                            fid.write('\n')
                            
                        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.yaml", "a") as yml:
                            yaml.dump(self.parsed_show_inventory, yml, allow_unicode=True)                  
                        
                        for filetype in filetype_loop:
                            parsed_nxos_inventory = sh_inventory_nxos_template.render(to_parse_inventory=self.parsed_show_inventory['name'],hostname=device.alias,filetype_loop_jinja2=filetype)                    
                        
                            with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.%s" % filetype, "a") as fh:
                                fh.write(parsed_nxos_inventory)                          
                            
                    # ----------------
                    # Store Inventory in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_inventory)


        with open("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.html", "a") as html:
            html.write("</table></body></html>")
            html.close() 
                            
        if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.md"):
            os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Excalibur/CSR_Inventory.md --output Camelot/Cisco/DevNet_Sandbox/Excalibur/Inventory_mind_map.html")

            fh.close()
            fid.close()
            yml.close()

        # Goodbye Banner
        print(Panel.fit(Text.from_markup(SERIALS)))