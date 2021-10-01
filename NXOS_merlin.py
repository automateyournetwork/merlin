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
from general_functionalities import ParseShowCommandFunction, ParseLearnFunction, ParseConfigFunction, ParseDictFunction
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

template_dir = 'templates/cisco/nxos'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Create Database
# ----------------

if os.path.exists("Camelot/Cisco/NXOS/The_Grail/The_Grail_DB.json"):
    os.remove("Camelot/Cisco/NXOS/The_Grail/The_Grail_DB.json")

db = TinyDB('Camelot/Cisco/NXOS/The_Grail/The_Grail_DB.json')

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        print(Panel.fit(Text.from_markup(GREETING)))
        testbed.connect(learn_hostname=True)

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
            # ----------------
            # Create a table in the database
            # ----------------
            table = db.table(device.alias)

            # ---------------------------------------
            # Genie learn().info for various functions
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN)))

            # ACLs
            self.learned_acl = ParseLearnFunction.parse_learn(steps, device, "acl")

            # ARP
            self.learned_arp = ParseLearnFunction.parse_learn(steps, device, "arp")

            # BGP
            self.learned_bgp = ParseLearnFunction.parse_learn(steps, device, "bgp")            

            # Config
            self.learned_config = ParseConfigFunction.parse_learn(steps, device, "config")

            # HSRP
            self.learned_hsrp = ParseLearnFunction.parse_learn(steps, device, "hsrp")

            # Interface
            self.learned_interface = ParseLearnFunction.parse_learn(steps, device, "interface")

            # OSPF
            self.learned_ospf = ParseLearnFunction.parse_learn(steps, device, "ospf")

            # Platform
            self.learned_platform = ParseDictFunction.parse_learn(steps, device, "platform")   

            # Routing
            self.learned_routing = ParseLearnFunction.parse_learn(steps, device, "routing")

            # VLAN
            self.learned_vlan = ParseLearnFunction.parse_learn(steps, device, "vlan")

            # VRF
            self.learned_vrf = ParseLearnFunction.parse_learn(steps, device, "vrf")   

            # ---------------------------------------
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING)))

            # Show Access-Lists
            self.parsed_show_access_lists = ParseShowCommandFunction.parse_show_command(steps, device, "show access-lists")

            # show BGP Process VRF All
            self.parsed_show_bgp_process_vrf_all = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp process vrf all")

            # Show BGP Sessions
            self.parsed_show_bgp_sessions = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp sessions")

            # Show CDP Neighbors
            if device.platform == 'n9k':
                self.parsed_show_cdp_neighbors = ParseShowCommandFunction.parse_show_command(steps, device, "show cdp neighbors")

            # Show CDP Neighbors Detail           
            self.parsed_show_cdp_neighbors_detail = ParseShowCommandFunction.parse_show_command(steps, device, "show cdp neighbors detail")

            # Show Enviroment
            if device.platform != "n7k":
                self.parsed_show_environment = ParseShowCommandFunction.parse_show_command(steps, device, "show environment")

            # Show Interface
            if device.platform != "n5k":
                self.parsed_show_interface = ParseShowCommandFunction.parse_show_command(steps, device, "show interface")

            # Show Interface Status
            self.parsed_show_interface_status = ParseShowCommandFunction.parse_show_command(steps, device, "show interface status")

            # Show Interface Transceiver
            self.parsed_show_interface_transceiver = ParseShowCommandFunction.parse_show_command(steps, device, "show interface transceiver")

            # Show Inventory
            self.parsed_show_inventory = ParseShowCommandFunction.parse_show_command(steps, device, "show inventory")

            # Show IP Interface Brief
            self.parsed_show_ip_interface_brief = ParseShowCommandFunction.parse_show_command(steps, device, "show ip interface brief vrf all")

            # Show IP OSPF
            self.parsed_show_ip_ospf = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf")

            # Show IP OSPF Interface
            self.parsed_show_ip_ospf_interface = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf interface")

            # Show IP OSPF Neighbor Detail
            self.parsed_show_ip_ospf_neighbor_detail = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf neighbors detail")

            # Show IP Route
            self.parsed_show_ip_route = ParseShowCommandFunction.parse_show_command(steps, device, "show ip route")

            # Show MAC Address-Table
            self.parsed_show_mac_address_table = ParseShowCommandFunction.parse_show_command(steps, device, "show mac address-table")

            # Show Portchannel Summary
            self.parsed_show_port_channel_summary = ParseShowCommandFunction.parse_show_command(steps, device, "show port-channel summary")

            # Show Version
            self.parsed_show_version = ParseShowCommandFunction.parse_show_command(steps, device, "show version")
            
            # Show VLAN
            self.parsed_show_vlan = ParseShowCommandFunction.parse_show_command(steps, device, "show vlan")

            # Show VRF
            self.parsed_show_vrf = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf")

            # Show VRF All detail
            self.parsed_show_vrf_all_detail = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf all detail")

            # show vrf All interface
            self.parsed_show_vrf_all_interface = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf all interface")            
            # ---------------------------------------
            # Create JSON, YAML, CSV, MD, HTML, HTML Mind Map files from the Parsed Data
            # ---------------------------------------         
            
            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                ###############################
                # Genie learn().info section
                ###############################

                # Learned ACL
                if self.learned_acl is not None:
                    learned_acl_template = env.get_template('learned_acl.j2')
                    learned_acl_netjson_json_template = env.get_template('learned_acl_netjson_json.j2')
                    learned_acl_netjson_html_template = env.get_template('learned_acl_netjson_html.j2')
                    directory_names = "Learned_ACL"
                    file_names = "learned_acl" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_acl)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_acl)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_acl_template.render(to_parse_access_list=self.learned_acl['acls'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Learned_ACL/%s_learned_acl.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_ACL/%s_learned_acl.md --output Camelot/Cisco/NXOS/Learned_ACL/%s_learned_acl_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_acl_netjson_json_template.render(to_parse_access_list=self.learned_acl['acls'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_acl_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_ACL/%s_learned_acl_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               
                        fh.close()

                    with open("Camelot/Cisco/NXOS/Learned_ACL/%s_learned_acl_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store ACLs in Device Table in Database
                    # ----------------

                    table.insert(self.learned_acl)

                # Learned ARP
                if self.learned_arp is not None:
                    learned_arp_template = env.get_template('learned_arp.j2')
                    learned_arp_statistics_template = env.get_template('learned_arp_statistics.j2')
                    learned_arp_netjson_json_template = env.get_template('learned_arp_netjson_json.j2')
                    learned_arp_netjson_html_template = env.get_template('learned_arp_netjson_html.j2')
                    learned_arp_statistics_netjson_json_template = env.get_template('learned_arp_statistics_netjson_json.j2')
                    learned_arp_statistics_netjson_html_template = env.get_template('learned_arp_statistics_netjson_html.j2')
                    directory_names = "Learned_ARP"
                    file_names = "learned_arp" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_arp)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_arp)  

                    for filetype in filetype_loop:
                        parsed_output_type = learned_arp_template.render(to_parse_arp=self.learned_arp['interfaces'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_arp_statistics_template.render(to_parse_arp=self.learned_arp['statistics'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp_statistics.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                            fh.close()

                    if os.path.exists("Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp.md --output Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp_statistics.md --output Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp_statistics_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_arp_netjson_json_template.render(to_parse_arp=self.learned_arp['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               
                        fh.close()

                    with open("Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    parsed_output_netjson_json = learned_arp_statistics_netjson_json_template.render(to_parse_arp=self.learned_arp['statistics'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_statistics_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp_statistics_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()

                    with open("Camelot/Cisco/NXOS/Learned_ARP/%s_learned_arp_statistics_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store ARP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_arp)

                # Learned BGP
                if 'instance' in self.learned_bgp:
                    learned_bgp_template = env.get_template('learned_bgp.j2')
                    learned_bgp_netjson_json_template = env.get_template('learned_bgp_netjson_json.j2')
                    learned_bgp_netjson_html_template = env.get_template('learned_bgp_netjson_html.j2')
                    directory_names = "Learned_BGP"
                    file_names = "learned_bgp"

                    self.save_to_json_file(device, directory_names, file_names, self.learned_bgp)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_bgp)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_bgp_template.render(to_parse_bgp=self.learned_bgp['instance'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Learned_BGP/%s_learned_bgp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_BGP/%s_learned_bgp.md --output Camelot/Cisco/NXOS/Learned_BGP/%s_learned_bgp_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_bgp_netjson_json_template.render(to_parse_bgp=self.learned_bgp['instance'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_bgp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_BGP/%s_learned_bgp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Learned_BGP/%s_learned_bgp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store BGP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_bgp)

                # Learned Config
                if self.learned_bgp is not None:
                    directory_names = "Learned_Config"
                    file_names = "learned_config"

                    self.save_to_json_file(device, directory_names, file_names, self.learned_config)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_config)

                    # ----------------
                    # Store Config in Device Table in Database
                    # ----------------

                    table.insert(self.learned_config)

                # Learned HSRP
                if self.learned_hsrp is not None:
                    learned_hsrp_template = env.get_template('learned_hsrp.j2')
                    learned_hsrp_netjson_json_template = env.get_template('learned_hsrp_netjson_json.j2')
                    learned_hsrp_netjson_html_template = env.get_template('learned_hsrp_netjson_html.j2')
                    directory_names = "Learned_HSRP"
                    file_names = "learned_hsrp"

                    self.save_to_json_file(device, directory_names, file_names, self.learned_hsrp)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_hsrp)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_hsrp_template.render(to_parse_hsrp=self.learned_hsrp,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Learned_HSRP/%s_learned_hsrp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_HSRP/%s_learned_hsrp.md --output Camelot/Cisco/NXOS/Learned_HSRP/%s_learned_hsrp_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_hsrp_netjson_json_template.render(to_parse_hsrp=self.learned_hsrp,device_alias = device.alias)
                    parsed_output_netjson_html = learned_hsrp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_HSRP/%s_learned_hsrp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Learned_HSRP/%s_learned_hsrp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store HSRP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_hsrp)

                # Learned Interface
                if device.platform != "n5k":
                    if self.learned_interface is not None:
                        learned_interface_template = env.get_template('learned_interface.j2')
                        learned_interface_netjson_json_template = env.get_template('learned_interface_netjson_json.j2')
                        learned_interface_netjson_html_template = env.get_template('learned_interface_netjson_html.j2')
                        learned_interface_enable_netjson_json_template = env.get_template('learned_interface_enabled_netjson_json.j2')
                        learned_interface_enable_netjson_html_template = env.get_template('learned_interface_enabled_netjson_html.j2')
                        directory_names = "Learned_Interface"
                        file_names = "learned_interface" 

                        self.save_to_json_file(device, directory_names, file_names, self.learned_interface)
                        self.save_to_yaml_file(device, directory_names, file_names, self.learned_interface)

                        for filetype in filetype_loop:
                            parsed_output_type = learned_interface_template.render(to_parse_interface=self.learned_interface,filetype_loop_jinja2=filetype)

                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                        if os.path.exists("Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface.md" % device.alias):
                            os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface.md --output Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface_mind_map.html" % (device.alias,device.alias))

                        parsed_output_netjson_json = learned_interface_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                        parsed_output_netjson_html = learned_interface_netjson_html_template.render(device_alias = device.alias)

                        with open("Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface_netgraph.json" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_json)
                            fh.close()               

                        with open("Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface_netgraph.html" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_html)
                            fh.close()

                        parsed_output_netjson_json = learned_interface_enable_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                        parsed_output_netjson_html = learned_interface_enable_netjson_html_template.render(device_alias = device.alias)

                        with open("Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface_enabled_netgraph.json" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_json)
                            fh.close()               

                        with open("Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface_enabled_netgraph.html" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_html)
                            fh.close()

                        # ----------------
                        # Store Interface in Device Table in Database
                        # ----------------

                        table.insert(self.learned_interface)
                else:
                        learned_interface_template = env.get_template('learned_interface_5k.j2')
                        learned_interface_netjson_json_template = env.get_template('learned_interface_5k_netjson_json.j2')
                        learned_interface_netjson_html_template = env.get_template('learned_interface_5k_netjson_html.j2')                     
                        directory_names = "Learned_Interface"
                        file_names = "learned_interface" 

                        self.save_to_json_file(device, directory_names, file_names, self.learned_interface)
                        self.save_to_yaml_file(device, directory_names, file_names, self.learned_interface)

                        for filetype in filetype_loop:
                            parsed_output_type = learned_interface_template.render(to_parse_interface=self.learned_interface,filetype_loop_jinja2=filetype)

                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                        if os.path.exists("Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface.md" % device.alias):
                            os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface.md --output Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface_mind_map.html" % (device.alias,device.alias))

                        parsed_output_netjson_json = learned_interface_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                        parsed_output_netjson_html = learned_interface_netjson_html_template.render(device_alias = device.alias)

                        with open("Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface_netgraph.json" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_json)
                            fh.close()               

                        with open("Camelot/Cisco/NXOS/Learned_Interface/%s_learned_interface_netgraph.html" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_html)
                            fh.close()

                        # ----------------
                        # Store Interface in Device Table in Database
                        # ----------------

                        table.insert(self.learned_interface)

                # Learned OSPF
                if self.learned_ospf['feature_ospf']:
                    learned_ospf_template = env.get_template('learned_ospf.j2')
                    learned_ospf_netjson_json_template = env.get_template('learned_ospf_netjson_json.j2')
                    learned_ospf_netjson_html_template = env.get_template('learned_ospf_netjson_html.j2')
                    directory_names = "Learned_OSPF"
                    file_names = "learned_ospf" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_ospf)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_ospf)  

                    for filetype in filetype_loop:
                        parsed_output_type = learned_ospf_template.render(to_parse_ospf=self.learned_ospf,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Learned_OSPF/%s_learned_ospf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_OSPF/%s_learned_ospf.md --output Camelot/Cisco/NXOS/Learned_OSPF/%s_learned_ospf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_ospf_netjson_json_template.render(to_parse_ospf=self.learned_ospf,device_alias = device.alias)
                    parsed_output_netjson_html = learned_ospf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_OSPF/%s_learned_ospf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()              

                    with open("Camelot/Cisco/NXOS/Learned_OSPF/%s_learned_ospf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store OSPF in Device Table in Database
                    # ----------------

                    table.insert(self.learned_ospf)

                # Learned Platform
                if self.learned_platform is not None:
                    learned_platform_template = env.get_template('learned_platform.j2')
                    learned_platform_netjson_json_template = env.get_template('learned_platform_netjson_json.j2')
                    learned_platform_netjson_html_template = env.get_template('learned_platform_netjson_html.j2')
                    directory_names = "Learned_Platform"
                    file_names = "learned_platform"

                    self.save_to_json_file(device, directory_names, file_names, self.learned_platform)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_platform)            

                    for filetype in filetype_loop:
                        parsed_output_type = learned_platform_template.render(to_parse_platform=self.learned_platform,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Learned_Platform/%s_learned_platform.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_Platform/%s_learned_platform.md --output Camelot/Cisco/NXOS/Learned_Platform/%s_learned_platform_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_platform_netjson_json_template.render(to_parse_platform=self.learned_platform,device_alias = device.alias)
                    parsed_output_netjson_html = learned_platform_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_Platform/%s_learned_platform_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Learned_Platform/%s_learned_platform_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Platform in Device Table in Database
                    # ----------------

                    table.insert(self.learned_platform)

                # Learned Routing
                if self.learned_routing is not None:
                    learned_routing_template = env.get_template('learned_routing.j2')
                    learned_routing_netjson_json_template = env.get_template('learned_routing_netjson_json.j2')
                    learned_routing_netjson_html_template = env.get_template('learned_routing_netjson_html.j2')
                    directory_names = "Learned_Routing"
                    file_names = "learned_routing" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_routing)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_routing)                

                    for filetype in filetype_loop:
                        parsed_output_type = learned_routing_template.render(to_parse_routing=self.learned_routing['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Learned_Routing/%s_learned_routing.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_Routing/%s_learned_routing.md --output Camelot/Cisco/NXOS/Learned_Routing/%s_learned_routing_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_routing_netjson_json_template.render(to_parse_routing=self.learned_routing['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_routing_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_Routing/%s_learned_routing_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()             

                    with open("Camelot/Cisco/NXOS/Learned_Routing/%s_learned_routing_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store Routing in Device Table in Database
                    # ----------------

                    table.insert(self.learned_routing)

                # Learned VLAN
                if self.learned_vlan is not None:
                    learned_vlan_template = env.get_template('learned_vlan.j2')
                    learned_vlan_netjson_json_template = env.get_template('learned_vlan_netjson_json.j2')
                    learned_vlan_netjson_html_template = env.get_template('learned_vlan_netjson_html.j2')
                    directory_names = "Learned_VLAN"
                    file_names = "learned_vlan" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_vlan)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_vlan)                

                    for filetype in filetype_loop:
                        parsed_output_type = learned_vlan_template.render(to_parse_vlan=self.learned_vlan['vlans'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Learned_VLAN/%s_learned_vlan.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_VLAN/%s_learned_vlan.md --output Camelot/Cisco/NXOS/Learned_VLAN/%s_learned_vlan_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_vlan_netjson_json_template.render(to_parse_vlan=self.learned_vlan['vlans'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_vlan_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_VLAN/%s_learned_vlan_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/NXOS/Learned_VLAN/%s_learned_vlan_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store VLAN in Device Table in Database
                    # ----------------

                    table.insert(self.learned_vlan)

                # Learned VRF
                if self.learned_vrf is not None:
                    learned_vrf_template = env.get_template('learned_vrf.j2')
                    learned_vrf_netjson_json_template = env.get_template('learned_vrf_netjson_json.j2')
                    learned_vrf_netjson_html_template = env.get_template('learned_vrf_netjson_html.j2')
                    directory_names = "Learned_VRF"
                    file_names = "learned_vrf"

                    self.save_to_json_file(device, directory_names, file_names, self.learned_vrf)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_vrf)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_vrf_template.render(to_parse_vrf=self.learned_vrf['vrfs'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype) 
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Learned_VRF/%s_learned_vrf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Learned_VRF/%s_learned_vrf.md --output Camelot/Cisco/NXOS/Learned_VRF/%s_learned_vrf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_vrf_netjson_json_template.render(to_parse_vrf=self.learned_vrf['vrfs'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_vrf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Learned_VRF/%s_learned_vrf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Learned_VRF/%s_learned_vrf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF in Device Table in Database
                    # ----------------

                    table.insert(self.learned_vrf)

                ###############################
                # Genie Show Command Section
                ###############################

                # Show access-lists
                if self.parsed_show_access_lists is not None:
                    sh_access_lists_template = env.get_template('show_access_lists.j2')
                    sh_access_lists_netjson_json_template = env.get_template('show_access_lists_netjson_json.j2')
                    sh_access_lists_netjson_html_template = env.get_template('show_access_lists_netjson_html.j2')
                    directory_names = "Show_Access_Lists"
                    file_names = "show_access_lists"

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_access_lists)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_access_lists)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_access_lists_template.render(to_parse_access_list=self.parsed_show_access_lists,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Show_Access_Lists/%s_show_access_lists.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Access_Lists/%s_show_access_lists.md --output Camelot/Cisco/NXOS/Show_Access_Lists/%s_show_access_lists_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_access_lists_netjson_json_template.render(to_parse_access_list=self.parsed_show_access_lists,device_alias = device.alias)
                    parsed_output_netjson_html = sh_access_lists_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_Access_Lists/%s_show_access_lists_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/NXOS/Show_Access_Lists/%s_show_access_lists_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store ACLs in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_access_lists)

                # Show BGP process vrf all
                if self.parsed_show_bgp_process_vrf_all is not None:
                    sh_bgp_process_vrf_all_template = env.get_template('show_bgp_process_vrf_all.j2')                  
                    sh_bgp_process_vrf_all_netjson_json_template = env.get_template('show_bgp_process_vrf_all_netjson_json.j2')
                    sh_bgp_process_vrf_all_netjson_html_template = env.get_template('show_bgp_process_vrf_all_netjson_html.j2')
                    
                    directory_names = "Show_BGP_Process_VRF_All"
                    file_names = "show_bgp_process_vfr_all"
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_bgp_process_vrf_all)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_bgp_process_vrf_all)
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_bgp_process_vrf_all_template.render(to_parse_bgp=self.parsed_show_bgp_process_vrf_all,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype) 
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.md --output Camelot/Cisco/NXOS/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_bgp_process_vrf_all_netjson_json_template.render(to_parse_bgp=self.parsed_show_bgp_process_vrf_all,device_alias = device.alias)
                    parsed_output_netjson_html = sh_bgp_process_vrf_all_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store BGP Process VRF All in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_bgp_process_vrf_all)

                # Show BGP Sessions
                if self.parsed_show_bgp_sessions is not None:
                    sh_bgp_sessions_template = env.get_template('show_bgp_sessions.j2')                  
                    sh_bgp_sessions_netjson_json_template = env.get_template('show_bgp_sessions_netjson_json.j2')
                    sh_bgp_sessions_netjson_html_template = env.get_template('show_bgp_sessions_netjson_html.j2')
                    directory_names = "Show_BGP_Sessions"
                    file_names = "show_bgp_sessions"

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_bgp_sessions)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_bgp_sessions)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_bgp_sessions_template.render(to_parse_bgp=self.parsed_show_bgp_sessions,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype) 
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Show_BGP_Sessions/%s_show_bgp_sessions.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_BGP_Sessions/%s_show_bgp_sessions.md --output Camelot/Cisco/NXOS/Show_BGP_Sessions/%s_show_bgp_sessions_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_bgp_sessions_netjson_json_template.render(to_parse_bgp=self.parsed_show_bgp_sessions,device_alias = device.alias)
                    parsed_output_netjson_html = sh_bgp_sessions_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_BGP_Sessions/%s_show_bgp_sessions_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_BGP_Sessions/%s_show_bgp_sessions_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store BGP Sessions in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_bgp_sessions)

                # Show CDP Neighbors
                if device.platform == 'n9k':                
                    if self.parsed_show_cdp_neighbors is not None:
                        sh_cdp_neighbors_template = env.get_template('show_cdp_neighbors.j2')
                        sh_cdp_neighbors_netjson_json_template = env.get_template('show_cdp_neighbor_netjson_json.j2')
                        sh_cdp_neighbors_netjson_html_template = env.get_template('show_cdp_neighbor_netjson_html.j2')
                        directory_names = "Show_CDP_Neighbors"
                        file_names = "show_cdp_neighbors"
    
                        self.save_to_json_file(device, directory_names, file_names, self.parsed_show_cdp_neighbors)
                        self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_cdp_neighbors)
    
                        for filetype in filetype_loop:                    
                            parsed_output_type = sh_cdp_neighbors_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors['cdp'],filetype_loop_jinja2=filetype)
    
                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                                           
                        if os.path.exists("Camelot/Cisco/NXOS/Show_CDP_Neighbors/%s_show_cdp_neighbors.md" % device.alias):
                            os.system("markmap --no-open Camelot/Cisco/NXOS/Show_CDP_Neighbors/%s_show_cdp_neighbors.md --output Camelot/Cisco/NXOS/Show_CDP_Neighbors/%s_show_cdp_neighbors_mind_map.html" % (device.alias,device.alias))
    
                        parsed_output_netjson_json = sh_cdp_neighbors_netjson_json_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors['cdp'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                        parsed_output_netjson_html = sh_cdp_neighbors_netjson_html_template.render(device_alias = device.alias)
    
                        with open("Camelot/Cisco/NXOS/Show_CDP_Neighbors/%s_show_cdp_neighbors_netgraph.json" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_json)
                            fh.close()
    
                        with open("Camelot/Cisco/NXOS/Show_CDP_Neighbors/%s_show_cdp_neighbors_netgraph.html" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_html)
                            fh.close()
    
                        # ----------------
                        # Store CDP Neighbors in Device Table in Database
                        # ----------------
    
                        table.insert(self.parsed_show_cdp_neighbors)

                # Show CDP Neighbors Details
                if self.parsed_show_cdp_neighbors_detail is not None:
                    sh_cdp_neighbors_detail_template = env.get_template('show_cdp_neighbors_details.j2')
                    sh_cdp_neighbors_detail_totals_template = env.get_template('show_cdp_neighbors_details_totals.j2')
                    sh_cdp_neighbors_detail_netjson_json_template = env.get_template('show_cdp_neighbor_details_netjson_json.j2')
                    sh_cdp_neighbors_detail_netjson_html_template = env.get_template('show_cdp_neighbor_details_netjson_html.j2')
                    directory_names = "Show_CDP_Neighbors_Details"
                    file_names = "show_cdp_neighbors_detail"
    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_cdp_neighbors_detail)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_cdp_neighbors_detail)
    
                    for filetype in filetype_loop:                    
                        parsed_output_type = sh_cdp_neighbors_detail_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors_detail['index'],filetype_loop_jinja2=filetype)
                        parsed_totals = sh_cdp_neighbors_detail_totals_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors_detail,filetype_loop_jinja2=filetype)
    
                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)               
    
                        with open("Camelot/Cisco/NXOS/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_totals)
    
                    if os.path.exists("Camelot/Cisco/NXOS/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.md --output Camelot/Cisco/NXOS/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_mind_map.html" % (device.alias,device.alias))
    
                    if os.path.exists("Camelot/Cisco/NXOS/Show_CDP_Neighbors/%s_show_cdp_neighbors_detail_totals.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals.md --output Camelot/Cisco/NXOS/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals_mind_map.html" % (device.alias,device.alias))
    
                    parsed_output_netjson_json = sh_cdp_neighbors_detail_netjson_json_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors_detail['index'],filetype_loop_jinja2=filetype,device_ip = device.connections.cli.ip)
                    parsed_output_netjson_html = sh_cdp_neighbors_detail_netjson_html_template.render(device_alias = device.alias)
    
                    with open("Camelot/Cisco/NXOS/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               
    
                    with open("Camelot/Cisco/NXOS/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()
    
                    # ----------------
                    # Store CDP Neighbors Details in Device Table in Database
                    # ----------------
    
                    table.insert(self.parsed_show_cdp_neighbors_detail)

                # Show Environment
                if device.platform != "n7k":
                    if self.parsed_show_environment is not None:
                        sh_environment_template = env.get_template('show_environment_all.j2')
                        sh_environment_netjson_json_template = env.get_template('show_environment_all_netjson_json.j2')
                        sh_environment_netjson_html_template = env.get_template('show_environment_all_netjson_html.j2')  
                        sh_environment_5k_template = env.get_template('show_environment_all_5k.j2')
                        sh_environment_5k_netjson_json_template = env.get_template('show_environment_all_5k_netjson_json.j2')
                        sh_environment_5k_netjson_html_template = env.get_template('show_environment_all_5k_netjson_html.j2')                        
                        directory_names = "Show_Environment"
                        file_names = "show_environment" 

                        self.save_to_json_file(device, directory_names, file_names, self.parsed_show_environment)
                        self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_environment)

                        if device.platform == "n9k":
                            for filetype in filetype_loop:  
                                parsed_output_type = sh_environment_template.render(to_parse_environment=self.parsed_show_environment,filetype_loop_jinja2=filetype)
                      
                                self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                            if os.path.exists("Camelot/Cisco/NXOS/Show_Environment/%s_show_environment.md" % device.alias):
                                os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Environment/%s_show_environment.md --output Camelot/Cisco/NXOS/Show_Environment/%s_show_environment_mind_map.html" % (device.alias,device.alias))

                            parsed_output_netjson_json = sh_environment_netjson_json_template.render(to_parse_environment=self.parsed_show_environment,device_alias = device.alias)
                            parsed_output_netjson_html = sh_environment_netjson_html_template.render(device_alias = device.alias)
    
                            with open("Camelot/Cisco/NXOS/Show_Environment/%s_show_environment_netgraph.json" % device.alias, "w") as fh:
                                fh.write(parsed_output_netjson_json)
                                fh.close()
    
                            with open("Camelot/Cisco/NXOS/Show_Environment/%s_show_environment_netgraph.html" % device.alias, "w") as fh:
                                fh.write(parsed_output_netjson_html)
                                fh.close()

                        if device.platform == "n5k":
                            for filetype in filetype_loop:  
                                parsed_output_type = sh_environment_5k_template.render(to_parse_environment=self.parsed_show_environment,filetype_loop_jinja2=filetype)
                      
                                self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                            if os.path.exists("Camelot/Cisco/NXOS/Show_Environment/%s_show_environment.md" % device.alias):
                                os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Environment/%s_show_environment.md --output Camelot/Cisco/NXOS/Show_Environment/%s_show_environment_mind_map.html" % (device.alias,device.alias))

                            parsed_output_netjson_json = sh_environment_5k_netjson_json_template.render(to_parse_environment=self.parsed_show_environment,device_alias = device.alias)
                            parsed_output_netjson_html = sh_environment_5k_netjson_html_template.render(device_alias = device.alias)
    
                            with open("Camelot/Cisco/NXOS/Show_Environment/%s_show_environment_netgraph.json" % device.alias, "w") as fh:
                                fh.write(parsed_output_netjson_json)
                                fh.close()
    
                            with open("Camelot/Cisco/NXOS/Show_Environment/%s_show_environment_netgraph.html" % device.alias, "w") as fh:
                                fh.write(parsed_output_netjson_html)
                                fh.close()

                        # ----------------
                        # Store Environment in Device Table in Database
                        # ----------------

                        table.insert(self.parsed_show_environment)

                # Show Interface
                if device.platform != "n5k":
                    if self.parsed_show_interface is not None:
                        show_interface_template = env.get_template('show_interface.j2')
                        show_interface_netjson_json_template = env.get_template('show_interface_connected_netjson_json.j2')
                        show_interface_netjson_html_template = env.get_template('show_interface_connected_netjson_html.j2')
                        directory_names = "Show_Interface"
                        file_names = "show_interface"
    
                        self.save_to_json_file(device, directory_names, file_names, self.parsed_show_interface)
                        self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_interface)
    
                        for filetype in filetype_loop:
                            parsed_output_type = show_interface_template.render(to_parse_interface=self.parsed_show_interface,filetype_loop_jinja2=filetype)
    
                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
    
                        if os.path.exists("Camelot/Cisco/NXOS/Show_Interface/%s_show_interface.md" % device.alias):
                            os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Interface/%s_show_interface.md --output Camelot/Cisco/NXOS/Show_Interface/%s_show_interface_mind_map.html" % (device.alias,device.alias))

                        parsed_output_netjson_json = show_interface_netjson_json_template.render(to_parse_interface=self.parsed_show_interface,device_alias = device.alias)
                        parsed_output_netjson_html = show_interface_netjson_html_template.render(device_alias = device.alias)

                        with open("Camelot/Cisco/NXOS/Show_Interface/%s_show_interface_connected_netgraph.json" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_json)               

                        with open("Camelot/Cisco/NXOS/Show_Interface/%s_show_interface_connected_netgraph.html" % device.alias, "w") as fh:
                            fh.write(parsed_output_netjson_html)

                        # ----------------
                        # Store Interfaces in Device Table in Database
                        # ----------------
    
                        table.insert(self.parsed_show_interface)  
      
                # Show Interface Status
                if self.parsed_show_interface_status is not None:
                    show_interface_status_template = env.get_template('show_interface_status.j2')
                    show_interface_status_netjson_json_template = env.get_template('show_interface_status_netjson_json.j2')
                    show_interface_status_netjson_html_template = env.get_template('show_interface_status_netjson_html.j2')
                    show_interface_status_connected_netjson_json_template = env.get_template('show_interface_status_connected_netjson_json.j2')
                    show_interface_status_connected_netjson_html_template = env.get_template('show_interface_status_connected_netjson_html.j2')                    
                    directory_names = "Show_Interface_Status"
                    file_names = "show_interface_status"

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_interface_status)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_interface_status)

                    for filetype in filetype_loop:
                        parsed_output_type = show_interface_status_template.render(to_parse_interface=self.parsed_show_interface_status,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_Interface_Status/%s_show_interface_status.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Interface_Status/%s_show_interface_status.md --output Camelot/Cisco/NXOS/Show_Interface_Status/%s_show_interface_status_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = show_interface_status_netjson_json_template.render(to_parse_interface=self.parsed_show_interface_status,device_alias = device.alias)
                    parsed_output_netjson_html = show_interface_status_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_Interface_Status/%s_show_interface_status_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_Interface_Status/%s_show_interface_status_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    parsed_output_netjson_json = show_interface_status_connected_netjson_json_template.render(to_parse_interface=self.parsed_show_interface_status,device_alias = device.alias)
                    parsed_output_netjson_html = show_interface_status_connected_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_Interface_Status/%s_show_interface_status_connected_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_Interface_Status/%s_show_interface_status_connected_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)                        
                    # ----------------
                    # Store Interfaces in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_interface_status)

                # Show Interface Transceiver
                if self.parsed_show_interface_transceiver is not None:
                    show_interface_transceiver_template = env.get_template('show_interface_transceiver.j2')
                    show_interface_transceiver_connected_netjson_json_template = env.get_template('show_interface_transceiver_connected_netjson_json.j2')
                    show_interface_transceiver_connected_netjson_html_template = env.get_template('show_interface_transceiver_connected_netjson_html.j2')                    
                    directory_names = "Show_Interface_Transceiver"
                    file_names = "show_interface_transceiver"

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_interface_transceiver)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_interface_transceiver)

                    for filetype in filetype_loop:
                        parsed_output_type = show_interface_transceiver_template.render(to_parse_interface=self.parsed_show_interface_transceiver,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_Interface_Transceiver/%s_show_interface_transceiver.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Interface_transceiver/%s_show_interface_transceiver.md --output Camelot/Cisco/NXOS/Show_Interface_Transceiver/%s_show_interface_transceiver_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = show_interface_transceiver_connected_netjson_json_template.render(to_parse_interface=self.parsed_show_interface_transceiver,device_alias = device.alias)
                    parsed_output_netjson_html = show_interface_transceiver_connected_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_Interface_Transceiver/%s_show_interface_transceiver_connected_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_Interface_Transceiver/%s_show_interface_transceiver_connected_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)                        
                    # ----------------
                    # Store Interfaces in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_interface_transceiver)

                # Show Inventory
                if self.parsed_show_inventory is not None:
                    # Nexus 
                    sh_inventory_nexus_template = env.get_template('show_inventory.j2')
                    sh_inventory_netjson_json_template = env.get_template('show_inventory_netjson_json.j2')
                    sh_inventory_netjson_html_template = env.get_template('show_inventory_netjson_html.j2')

                    directory_names = "Show_Inventory"
                    file_names = "show_inventory"

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_inventory)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_inventory)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_inventory_nexus_template.render(to_parse_inventory_name=self.parsed_show_inventory['name'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype) 

                        if os.path.exists("Camelot/Cisco/NXOS/Show_Inventory/%s_show_inventory.md" % device.alias):
                            os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Inventory/%s_show_inventory.md --output Camelot/Cisco/NXOS/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_inventory_netjson_json_template.render(to_parse_inventory_name=self.parsed_show_inventory['name'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_inventory_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_Inventory/%s_show_inventory_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_Inventory/%s_show_inventory_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                # Show ip interface brief
                if self.parsed_show_ip_interface_brief is not None:
                    sh_ip_int_brief_template = env.get_template('show_ip_interface_brief.j2')
                    sh_ip_int_brief_netjson_json_template = env.get_template('show_ip_interface_brief_netjson_json.j2')
                    sh_ip_int_brief_netjson_html_template = env.get_template('show_ip_interface_brief_netjson_html.j2')
                    directory_names = "Show_IP_Interface_Brief"
                    file_names = "show_ip_interface_brief"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_interface_brief)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_interface_brief)               
        
                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_int_brief_template.render(to_parse_interfaces=self.parsed_show_ip_interface_brief['interface'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_IP_Interface_Brief/%s_show_ip_interface_brief.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_Interface_Brief/%s_show_ip_interface_brief.md --output Camelot/Cisco/NXOS/Show_IP_Interface_Brief/%s_show_ip_interface_brief_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_int_brief_netjson_json_template.render(to_parse_interfaces=self.parsed_show_ip_interface_brief['interface'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_int_brief_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_IP_Interface_Brief/%s_show_ip_interface_brief_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/NXOS/Show_IP_Interface_Brief/%s_show_ip_interface_brief_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store IP Int Brief in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_interface_brief)

                # Show IP OSPF
                if self.parsed_show_ip_ospf is not None:
                    sh_ip_ospf_template = env.get_template('show_ip_ospf.j2')
                    sh_ip_ospf_netjson_json_template = env.get_template('show_ip_ospf_netjson_json.j2')
                    sh_ip_ospf_netjson_html_template = env.get_template('show_ip_ospf_netjson_html.j2')                    
                    directory_names = "Show_IP_OSPF"
                    file_names = "show_ip_ospf"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_ospf)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_ospf)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_IP_OSPF/%s_show_ip_ospf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_OSPF/%s_show_ip_ospf.md --output Camelot/Cisco/NXOS/Show_IP_OSPF/%s_show_ip_ospf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_ospf_netjson_json_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_ospf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_IP_OSPF/%s_show_ip_ospf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/NXOS/Show_IP_OSPF/%s_show_ip_ospf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store IP OSPF in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf)

                # Show IP OSPF Interface
                if self.parsed_show_ip_ospf_interface is not None:
                    sh_ip_ospf_interface_template = env.get_template('show_ip_ospf_interface.j2')
                    sh_ip_ospf_interface_netjson_json_template = env.get_template('show_ip_ospf_interface_netjson_json.j2')
                    sh_ip_ospf_interface_netjson_html_template = env.get_template('show_ip_ospf_interface_netjson_html.j2')                    
                    directory_names = "Show_IP_OSPF_Interface"
                    file_names = "show_ip_ospf_interface"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_ospf_interface)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_ospf_interface)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_interface_template.render(to_parse_ip_ospf_interface=self.parsed_show_ip_ospf_interface['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.md --output Camelot/Cisco/NXOS/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_ospf_interface_netjson_json_template.render(to_parse_ip_ospf_interface=self.parsed_show_ip_ospf_interface['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_ospf_interface_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store IP OSPF Interface in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf_interface)

                # Show IP OSPF Neighbor Detail
                if self.parsed_show_ip_ospf_neighbor_detail is not None:
                    sh_ip_ospf_neighbor_detail_template = env.get_template('show_ip_ospf_neighbor_detail.j2')
                    sh_ip_ospf_neighbor_detail_netjson_json_template = env.get_template('show_ip_ospf_neighbor_detail_netjson_json.j2')
                    sh_ip_ospf_neighbor_detail_netjson_html_template = env.get_template('show_ip_ospf_neighbor_detail_netjson_html.j2')
                    directory_names = "Show_IP_OSPF_Neighbor_Detail"
                    file_names = "show_ip_ospf_neighbor_detail"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_ospf_neighbor_detail)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_ospf_neighbor_detail)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_neighbor_detail_template.render(to_parse_ip_ospf_neighbor_detail=self.parsed_show_ip_ospf_neighbor_detail['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.md --output Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_ospf_neighbor_detail_netjson_json_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_ospf_neighbor_detail_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_IP_OSPF/%s_show_ip_ospf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/NXOS/Show_IP_OSPF/%s_show_ip_ospf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store IP OSPF Neighbor Detail in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf_neighbor_detail)

                # Show IP Route
                if self.parsed_show_ip_route is not None:
                    sh_ip_route_template = env.get_template('show_ip_route.j2')
                    sh_ip_route_netjson_json_template = env.get_template('show_ip_route_netjson_json.j2')
                    sh_ip_route_netjson_html_template = env.get_template('show_ip_route_netjson_html.j2')
                    directory_names = "Show_IP_Route"
                    file_names = "show_ip_route"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_route)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_route)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/NXOS/Show_IP_Route/%s_show_ip_route.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_Route/%s_show_ip_route.md --output Camelot/Cisco/NXOS/Show_IP_Route/%s_show_ip_route_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_route_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_route_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_IP_Route/%s_show_ip_route_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()              

                    with open("Camelot/Cisco/NXOS/Show_IP_Route/%s_show_ip_route_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store IP Route in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_route)

                # Show mac address-table
                if self.parsed_show_mac_address_table is not None:
                    sh_mac_address_table_template = env.get_template('show_mac_address_table.j2')
                    sh_mac_address_table_netjson_json_template = env.get_template('show_mac_address_table_netjson_json.j2')
                    sh_mac_address_table_netjson_html_template = env.get_template('show_mac_address_table_netjson_html.j2')
                    directory_names = "Show_MAC_Address_Table"
                    file_names = "show_mac_address_table"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_mac_address_table)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_mac_address_table)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_mac_address_table_template.render(to_parse_mac_address_table=self.parsed_show_mac_address_table['mac_table'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_MAC_Address_Table/%s_show_mac_address_table.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_MAC_Address_Table/%s_show_mac_address_table.md --output Camelot/Cisco/NXOS/Show_MAC_Address_Table/%s_show_mac_address_table_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_mac_address_table_netjson_json_template.render(to_parse_mac_address_table=self.parsed_show_mac_address_table['mac_table'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_mac_address_table_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_MAC_Address_Table/%s_show_mac_address_table_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()              

                    with open("Camelot/Cisco/NXOS/Show_MAC_Address_Table/%s_show_mac_address_table_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store MAC Address Table in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_mac_address_table)

                # Show Port-channel summary
                if self.parsed_show_port_channel_summary is not None:
                    sh_portchannel_summary_template = env.get_template('show_portchannel_summary.j2')
                    sh_portchannel_summary_netjson_json_template = env.get_template('show_portchannel_summary_netjson_json.j2')
                    sh_portchannel_summary_netjson_html_template = env.get_template('show_portchannel_summary_netjson_html.j2')

                    directory_names = "Show_Port_Channel_Summary"
                    file_names = "show_port_channel_summary"
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_port_channel_summary)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_port_channel_summary)

                    for filetype in filetype_loop:                       
                        parsed_output_type = sh_portchannel_summary_template.render(to_parse_etherchannel_summary=self.parsed_show_port_channel_summary['interfaces'],filetype_loop_jinja2=filetype)
                      
                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_Port_Channel_Summary/%s_show_port_channel_summary.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Port_Channel_Summary/%s_show_port_channel_summary.md --output Camelot/Cisco/NXOS/Show_Port_Channel_Summary/%s_show_port_channel_summary_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_portchannel_summary_netjson_json_template.render(to_parse_etherchannel_summary=self.parsed_show_port_channel_summary['interfaces'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_portchannel_summary_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_Port_Channel_Summary/%s_show_port_channel_summary_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_Port_Channel_Summary/%s_show_port_channel_summary_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Port-Channel in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_port_channel_summary)

                # Show version
                if self.parsed_show_version is not None:
                    sh_ver_template = env.get_template('show_version.j2')
                    sh_ver_netjson_json_template = env.get_template('show_version_netjson_json.j2')
                    sh_ver_netjson_html_template = env.get_template('show_version_netjson_html.j2')                    
                    directory_names = "Show_Version"
                    file_names = "show_version"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_version)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_version)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ver_template.render(to_parse_version=self.parsed_show_version['platform'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_Version/%s_show_version.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_Version/%s_show_version.md --output Camelot/Cisco/NXOS/Show_Version/%s_show_version_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ver_netjson_json_template.render(to_parse_version=self.parsed_show_version['platform'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ver_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_Version/%s_show_version_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_Version/%s_show_version_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Version in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_version)

                # Show vlan
                if self.parsed_show_vlan is not None:
                    sh_vlan_template = env.get_template('show_vlan.j2')
                    sh_vlan_netjson_json_template = env.get_template('show_vlan_netjson_json.j2')
                    sh_vlan_netjson_html_template = env.get_template('show_vlan_netjson_html.j2') 
                    directory_names = "Show_VLAN"
                    file_names = "show_vlan"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_vlan)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_vlan)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_vlan_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_VLAN/%s_show_vlan.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_VLAN/%s_show_vlan.md --output Camelot/Cisco/NXOS/Show_VLAN/%s_show_vlan_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_vlan_netjson_json_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vlan_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_VLAN/%s_show_vlan_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_VLAN/%s_show_vlan_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VLAN in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_vlan)

                # Show vrf
                if self.parsed_show_vrf is not None:
                    sh_vrf_template = env.get_template('show_vrf.j2')
                    sh_vrf_netjson_json_template = env.get_template('show_vrf_netjson_json.j2')
                    sh_vrf_netjson_html_template = env.get_template('show_vrf_netjson_html.j2')
                    sh_vrf_detail_template = env.get_template('show_vrf_detail.j2')
                    sh_vrf_detail_netjson_json_template = env.get_template('show_vrf_detail_netjson_json.j2')
                    sh_vrf_detail_netjson_html_template = env.get_template('show_vrf_detail_netjson_html.j2')
                    sh_ip_arp_vrf_template = env.get_template('show_ip_arp_vrf.j2')
                    sh_ip_arp_vrf_statistics_template = env.get_template('show_ip_arp_vrf_statistics.j2')
                    sh_ip_arp_vrf_netjson_json_template = env.get_template('show_ip_arp_vrf_netjson_json.j2')
                    sh_ip_arp_vrf_netjson_html_template = env.get_template('show_ip_arp_vrf_netjson_html.j2')
                    sh_ip_ospf_vrf_template = env.get_template('show_ip_ospf_vrf.j2')
                    sh_ip_ospf_vrf_netjson_json_template = env.get_template('show_ip_ospf_vrf_netjson_json.j2')
                    sh_ip_ospf_vrf_netjson_html_template = env.get_template('show_ip_ospf_vrf_netjson_html.j2')
                    sh_ip_ospf_interface_vrf_template = env.get_template('show_ip_ospf_interface_vrf.j2')
                    sh_ip_ospf_interface_vrf_netjson_json_template = env.get_template('show_ip_ospf_interface_vrf_netjson_json.j2')
                    sh_ip_ospf_interface_vrf_netjson_html_template = env.get_template('show_ip_ospf_interface_vrf_netjson_html.j2')
                    sh_ip_ospf_neighbor_detail_vrf_template = env.get_template('show_ip_ospf_neighbor_detail_vrf.j2')
                    sh_ip_ospf_neighbor_detail_vrf_netjson_json_template = env.get_template('show_ip_ospf_neighbor_detail_vrf_netjson_json.j2')
                    sh_ip_ospf_neighbor_detail_vrf_netjson_html_template = env.get_template('show_ip_ospf_neighbor_detail_vrf_netjson_html.j2')
                    sh_ip_route_template = env.get_template('show_ip_route.j2')
                    sh_ip_route_netjson_json_template = env.get_template('show_ip_route_netjson_json.j2')
                    sh_ip_route_netjson_html_template = env.get_template('show_ip_route_netjson_html.j2')
                    directory_names = "Show_VRF"
                    file_names = "show_vrf"  

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_vrf)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_vrf)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_template.render(to_parse_vrf=self.parsed_show_vrf['vrfs'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/NXOS/Show_VRF/%s_show_vrf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_VRF/%s_show_vrf.md --output Camelot/Cisco/NXOS/Show_VRF/%s_show_vrf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_vrf_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf['vrfs'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_VRF/%s_show_vrf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_VRF/%s_show_vrf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_vrf)

                    # For Each VRF
                    for vrf in self.parsed_show_vrf['vrfs']:

                        # Show IP ARP VRF <VRF> 
                        with steps.start('Parsing ip arp vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_arp_vrf = device.parse("show ip arp vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:

                            with open("Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                json.dump(self.parsed_show_ip_arp_vrf, fid, indent=4, sort_keys=True)
                                fid.close()

                            with open("Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                yaml.dump(self.parsed_show_ip_arp_vrf, yml, allow_unicode=True)
                                yml.close()

                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_arp_vrf_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['interfaces'],filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
                                    fh.close()
        
                            if os.path.exists("Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md --output Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_arp_vrf_statistics_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf,filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_statistics.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
                                    fh.close()
        
                            if os.path.exists("Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_statistics.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrfs_%s_statistics.md --output Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_statistics_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            parsed_output_netjson_json = sh_ip_arp_vrf_netjson_json_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['interfaces'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                            parsed_output_netjson_html = sh_ip_arp_vrf_netjson_html_template.render(device_alias = device.alias)

                            with open("Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)               

                            with open("Camelot/Cisco/NXOS/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)

                            # ----------------
                            # Store IP ARP VRF in Device Table in Database
                            # ----------------

                            table.insert(self.parsed_show_ip_arp_vrf)

                        # Show IP OSPF VRF <VRF> 
                        with steps.start('Parsing ip ospf vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_ospf_vrf = device.parse("show ip ospf vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_VRF/%s_show_ip_ospf_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                json.dump(self.parsed_show_ip_ospf_vrf, fid, indent=4, sort_keys=True)
                                fid.close()

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_VRF/%s_show_ip_ospf_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                yaml.dump(self.parsed_show_ip_ospf_vrf, yml, allow_unicode=True)
                                yml.close()

                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_ospf_vrf_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf_vrf['vrf'],filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/NXOS/Show_IP_OSPF_VRF/%s_show_ip_ospf_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
                                    fh.close()
        
                            if os.path.exists("Camelot/Cisco/NXOS/Show_IP_OSPF_VRF/%s_show_ip_ospf_vrf_%s.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_OSPF_VRF/%s_show_ip_ospf_vrf_%s.md --output Camelot/Cisco/NXOS/Show_IP_OSPF_VRF/%s_show_ip_ospf_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            parsed_output_netjson_json = sh_ip_ospf_vrf_netjson_json_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf_vrf['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                            parsed_output_netjson_html = sh_ip_ospf_vrf_netjson_html_template.render(device_alias = device.alias,vrf = vrf)

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_VRF/%s_show_ip_ospf_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)               

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_VRF/%s_show_ip_ospf_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)

                            # ----------------
                            # Store IP OSPF VRF in Device Table in Database
                            # ----------------

                            table.insert(self.parsed_show_ip_ospf_vrf)

                        # Show IP OSPF Interface VRF <VRF> 
                        with steps.start('Parsing ip ospf interface vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_ospf_interface_vrf = device.parse("show ip ospf interface vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface_VRF/%s_show_ip_ospf_interface_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                json.dump(self.parsed_show_ip_ospf_interface_vrf, fid, indent=4, sort_keys=True)
                                fid.close()

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface_VRF/%s_show_ip_ospf_interface_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                yaml.dump(self.parsed_show_ip_ospf_interface_vrf, yml, allow_unicode=True)
                                yml.close()

                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_ospf_interface_vrf_template.render(to_parse_ip_ospf_interface=self.parsed_show_ip_ospf_interface_vrf['vrf'],filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface_VRF/%s_show_ip_ospf_interface_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
                                    fh.close()
        
                            if os.path.exists("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface_VRF/%s_show_ip_ospf_interface_vrf_%s.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_OSPF_Interface_VRF/%s_show_ip_ospf_interface_vrf_%s.md --output Camelot/Cisco/NXOS/Show_IP_OSPF_Interface_VRF/%s_show_ip_ospf_interface_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            parsed_output_netjson_json = sh_ip_ospf_interface_vrf_netjson_json_template.render(to_parse_ip_ospf_interface=self.parsed_show_ip_ospf_interface_vrf['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                            parsed_output_netjson_html = sh_ip_ospf_interface_vrf_netjson_html_template.render(device_alias = device.alias,vrf = vrf)

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface_VRF/%s_show_ip_ospf_interface_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)               

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Interface_VRF/%s_show_ip_ospf_interface_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)

                            # ----------------
                            # Store IP OSPF VRF in Device Table in Database
                            # ----------------

                            table.insert(self.parsed_show_ip_ospf_interface_vrf)

                        # Show IP OSPF Neighbor VRF <VRF> 
                        with steps.start('Parsing ip ospf neighbor detail vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_ospf_neighbor_detail_vrf = device.parse("show ip ospf neighbor detail vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:
                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail_VRF/%s_show_ip_ospf_neighbor_detail_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                try:
                                    json.dump(self.parsed_show_ip_ospf_neighbor_detail_vrf, fid, indent=4, sort_keys=True)
                                    fid.close()
                                except Exception as e:
                                    step.failed('Could not parse it correctly\n{e}'.format(e=e))

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail_VRF/%s_show_ip_ospf_neighbor_detail_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                yaml.dump(self.parsed_show_ip_ospf_neighbor_detail_vrf, yml, allow_unicode=True)
                                yml.close()

                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_ospf_neighbor_detail_vrf_template.render(to_parse_ip_ospf_neighbor=self.parsed_show_ip_ospf_neighbor_detail_vrf['vrf'],filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail_VRF/%s_show_ip_ospf_neighbor_detail_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
                                    fh.close()
        
                            if os.path.exists("Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail_VRF/%s_show_ip_ospf_neighbor_detail_vrf_%s.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail_VRF/%s_show_ip_ospf_neighbor_detail_vrf_%s.md --output Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail_VRF/%s_show_ip_ospf_neighbor_detail_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            parsed_output_netjson_json = sh_ip_ospf_neighbor_detail_vrf_netjson_json_template.render(to_parse_ip_ospf_neighbor=self.parsed_show_ip_ospf_neighbor_detail_vrf['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                            parsed_output_netjson_html = sh_ip_ospf_neighbor_detail_vrf_netjson_html_template.render(device_alias = device.alias,vrf = vrf)

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail_VRF/%s_show_ip_ospf_neighbor_detail_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)               

                            with open("Camelot/Cisco/NXOS/Show_IP_OSPF_Neighbor_Detail_VRF/%s_show_ip_ospf_neighbor_detail_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)

                            # ----------------
                            # Store IP OSPF VRF in Device Table in Database
                            # ----------------

                            table.insert(self.parsed_show_ip_ospf_neighbor_detail_vrf)

                        # Show IP ROUTE VRF <VRF>
                        with steps.start('Parsing ip route vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_route_vrf = device.parse("show ip route vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:

                            with open("Camelot/Cisco/NXOS/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                json.dump(self.parsed_show_ip_route_vrf, fid, indent=4, sort_keys=True)
                                fid.close()

                            with open("Camelot/Cisco/NXOS/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                yaml.dump(self.parsed_show_ip_route_vrf, yml, allow_unicode=True)
                                yml.close()
                         
                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route_vrf['vrf'],filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/NXOS/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
                                    fh.close()

                            if os.path.exists("Camelot/Cisco/NXOS/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md" % (device.alias,vrf)):
                                    os.system("markmap --no-open Camelot/Cisco/NXOS/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md --output Camelot/Cisco/NXOS/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            parsed_output_netjson_json = sh_ip_route_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_route_vrf['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                            parsed_output_netjson_html = sh_ip_route_netjson_html_template.render(device_alias = device.alias)

                            with open("Camelot/Cisco/NXOS/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)
                                fh.close()              

                            with open("Camelot/Cisco/NXOS/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)
                                fh.close()

                            # ----------------
                            # Store IP Route VRF in Device Table in Database
                            # ----------------

                            table.insert(self.parsed_show_ip_route_vrf)

                        # Show VRF <VRF> Detail 
                        with steps.start('Parsing vrf vrf detail',continue_=True) as step:
                            try:
                                self.parsed_show_vrf_detail = device.parse("show vrf %s detail" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:

                            with open("Camelot/Cisco/NXOS/Show_VRF_Detail/%s_show_vrf_%s_detail.json" % (device.alias,vrf), "w") as fid:
                                json.dump(self.parsed_show_vrf_detail, fid, indent=4, sort_keys=True)
                                fid.close()

                            with open("Camelot/Cisco/NXOS/Show_VRF_Detail/%s_show_vrf_%s_detail.yaml" % (device.alias,vrf), "w") as yml:
                                yaml.dump(self.parsed_show_vrf_detail, yml, allow_unicode=True)
                                yml.close()

                            for filetype in filetype_loop:
                                parsed_output_type = sh_vrf_detail_template.render(to_parse_vrf_detail=self.parsed_show_vrf_detail,filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/NXOS/Show_VRF_Detail/%s_show_vrf_%s_detail.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
                                    fh.close()
        
                            if os.path.exists("Camelot/Cisco/NXOS/Show_VRF_Detail/%s_show_vrf_%s_detail.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Camelot/Cisco/NXOS/Show_VRF_Detail/%s_show_vrf_%s_detail.md --output Camelot/Cisco/NXOS/Show_VRF_Detail/%s_show_vrf_%s_detail_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            parsed_output_netjson_json = sh_vrf_detail_netjson_json_template.render(to_parse_vrf_detail=self.parsed_show_vrf_detail,filetype_loop_jinja2=filetype,device_alias = device.alias)
                            parsed_output_netjson_html = sh_vrf_detail_netjson_html_template.render(device_alias = device.alias,vrf = vrf)

                            with open("Camelot/Cisco/NXOS/Show_VRF_Detail/%s_show_vrf_%s_detail_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)               

                            with open("Camelot/Cisco/NXOS/Show_VRF_Detail/%s_show_vrf_%s_detail_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)

                            # ----------------
                            # Store IP ARP VRF in Device Table in Database
                            # ----------------

                            table.insert(self.parsed_show_vrf_detail)

                # Show vrf all detail
                if self.parsed_show_vrf_all_detail is not None:
                    sh_vrf_all_detail_template = env.get_template('show_vrf_all_detail.j2')
                    sh_vrf_all_detail_netjson_json_template = env.get_template('show_vrf_all_detail_netjson_json.j2')
                    sh_vrf_all_detail_netjson_html_template = env.get_template('show_vrf_all_detail_netjson_html.j2') 
                    directory_names = "Show_VRF_All_Detail"
                    file_names = "show_vrf_all_detail"
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_vrf_all_detail)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_vrf_all_detail)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_all_detail_template.render(to_parse_vrf=self.parsed_show_vrf_all_detail,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype) 

                    if os.path.exists("Camelot/Cisco/NXOS/Show_VRF_All_Detail/%s_show_vrf_all_detail.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_VRF_All_Detail/%s_show_vrf_all_detail.md --output Camelot/Cisco/NXOS/Show_VRF_All_Detail/%s_show_vrf_all_detail_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_vrf_all_detail_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf_all_detail,filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_all_detail_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_VRF_All_Detail/%s_show_vrf_all_detail_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_VRF_All_Detail/%s_show_vrf_all_detail_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF Detail in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vrf_all_detail)

                # Show vrf all interface
                if self.parsed_show_vrf_all_interface is not None:
                    sh_vrf_all_interface_template = env.get_template('show_vrf_all_interface.j2')
                    sh_vrf_all_interface_netjson_json_template = env.get_template('show_vrf_all_interface_netjson_json.j2')
                    sh_vrf_all_interface_netjson_html_template = env.get_template('show_vrf_all_interface_netjson_html.j2') 

                    directory_names = "Show_VRF_All_Interface"
                    file_names = "show_vrf_all_interface"
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_vrf_all_interface)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_vrf_all_interface)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_all_interface_template.render(to_parse_vrf=self.parsed_show_vrf_all_interface,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype) 

                    if os.path.exists("Camelot/Cisco/NXOS/Show_VRF_All_Interface/%s_show_vrf_all_interface.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/NXOS/Show_VRF_All_Interface/%s_show_vrf_all_interface.md --output Camelot/Cisco/NXOS/Show_VRF_All_Interface/%s_show_vrf_all_interface_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_vrf_all_interface_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf_all_interface,filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_all_interface_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/NXOS/Show_VRF_All_Interface/%s_show_vrf_all_interface_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/NXOS/Show_VRF_All_Interface/%s_show_vrf_all_interface_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF Interface in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vrf_all_interface)

        db.close()
        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED)))    

# ----------------
# Save Functions 
# ----------------
    def save_to_json_file(self, device, directory, file_names, content):
        file_path = "Camelot/Cisco/NXOS/{}/{}_{}.json".format(directory, device.alias, file_names)
        with open(file_path, "w") as json_file:
            json.dump(content, json_file, indent=4, sort_keys=True)
            json_file.close()
    
    def save_to_yaml_file(self, device, directory, file_names, content):
        file_path = "Camelot/Cisco/NXOS/{}/{}_{}.yaml".format(directory, device.alias, file_names)
        with open(file_path, "w") as yml_file:
            yaml.dump(content, yml_file, allow_unicode=True)
            yml_file.close()
    
    def save_to_specified_file_type(self, device, directory, file_names, content, file_type):
        file_path = "Camelot/Cisco/NXOS/{}/{}_{}.{}".format(directory, device.alias, file_names, file_type)
        with open(file_path, "w") as opened_file:
            opened_file.write(content)
            opened_file.close()