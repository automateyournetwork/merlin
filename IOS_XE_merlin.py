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

template_dir = 'templates/cisco/ios_xe'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Create Database
# ----------------

if os.path.exists("Camelot/Cisco/IOS_XE/The_Grail/Grail_DB.json"):
    os.remove("Camelot/Cisco/IOS_XE/The_Grail/Grail_DB.json") 

db = TinyDB('Camelot/Cisco/IOS_XE/The_Grail/Grail_DB.json')

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

            # Dot1X
            self.learned_dot1x = ParseLearnFunction.parse_learn(steps, device, "dot1x")

            # Interface
            self.learned_interface = ParseLearnFunction.parse_learn(steps, device, "interface")

            # LLDP
            self.learned_lldp = ParseLearnFunction.parse_learn(steps, device, "lldp")

            # NTP
            self.learned_ntp = ParseLearnFunction.parse_learn(steps, device, "ntp")

            # OSPF
            self.learned_ospf = ParseLearnFunction.parse_learn(steps, device, "ospf")

            # Routing
            self.learned_routing = ParseLearnFunction.parse_learn(steps, device, "routing")

            # STP
            self.learned_stp = ParseLearnFunction.parse_learn(steps, device, "stp")

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

            # Show Access-Sessions
            self.parsed_show_access_session = ParseShowCommandFunction.parse_show_command(steps, device, "show access-session")

            # Show Authentication Sessions
            self.parsed_show_authentication_sessions = ParseShowCommandFunction.parse_show_command(steps, device, "show authentication sessions")

            # Show CDP Neighbors
            self.parsed_show_cdp_neighbors = ParseShowCommandFunction.parse_show_command(steps, device, "show cdp neighbors")

            # Show CDP Neighbors Detail           
            self.parsed_show_cdp_neighbors_detail = ParseShowCommandFunction.parse_show_command(steps, device, "show cdp neighbors detail")

            # Show Enviroment
            self.parsed_show_environment = ParseShowCommandFunction.parse_show_command(steps, device, "show environment all")

            # Show Etherchannel Summary
            self.parsed_show_etherchannel_summary = ParseShowCommandFunction.parse_show_command(steps, device, "show etherchannel summary")

            # Show Interfaces
            self.parsed_show_int = ParseShowCommandFunction.parse_show_command(steps, device, "show interfaces")

            # Show Interfaces Status
            self.parsed_show_int_status = ParseShowCommandFunction.parse_show_command(steps, device, "show interfaces status")

            # Show Interfaces Trunk
            self.parsed_show_interfaces_trunk = ParseShowCommandFunction.parse_show_command(steps, device, "show interfaces trunk")

            # Show Inventory
            self.parsed_show_inventory = ParseShowCommandFunction.parse_show_command(steps, device, "show inventory")

            # Show IP ARP
            self.parsed_show_ip_arp = ParseShowCommandFunction.parse_show_command(steps, device, "show ip arp")

            # Show IP Interface Brief
            self.parsed_show_ip_int_brief = ParseShowCommandFunction.parse_show_command(steps, device, "show ip interface brief")

            # Show IP OSPF
            self.parsed_show_ip_ospf = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf")

            # Show IP OSPF Dabase
            self.parsed_show_ip_ospf_database = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf database")

            # Show IP OSPF Interface
            self.parsed_show_ip_ospf_interface = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf interface")

            # Show IP OSPF Neighbor
            self.parsed_show_ip_ospf_neighbor = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf neighbor")

            # Show IP OSPF Neighbor Detail
            self.parsed_show_ip_ospf_neighbor_detail = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf neighbor detail")

            # Show IP Route
            self.parsed_show_ip_route = ParseShowCommandFunction.parse_show_command(steps, device, "show ip route")

            # Show ISSU State Detail
            ## Only VSS Systems support ISSU Such as a 4500; test if device.platform == 4500
            if device.platform == "cat4500":
                self.parsed_show_issu_state = ParseShowCommandFunction.parse_show_command(steps, device, "show issu state detail")

            # Show MAC Address-Table
            self.parsed_show_mac_address_table = ParseShowCommandFunction.parse_show_command(steps, device, "show mac address-table")

            # Show NTP Associations
            self.parsed_show_ntp_associations = ParseShowCommandFunction.parse_show_command(steps, device, "show ntp associations")

            # Show Power Inline
            self.parsed_show_power_inline = ParseShowCommandFunction.parse_show_command(steps, device, "show power inline")

            # Show Version
            self.parsed_show_version = ParseShowCommandFunction.parse_show_command(steps, device, "show version")

            # Show VLAN
            self.parsed_show_vlan = ParseShowCommandFunction.parse_show_command(steps, device, "show vlan")

            # Show VRF
            self.parsed_show_vrf = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf")
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
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_ACL/%s_learned_acl.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_ACL/%s_learned_acl.md --output Camelot/Cisco/IOS_XE/Learned_ACL/%s_learned_acl_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_acl_netjson_json_template.render(to_parse_access_list=self.learned_acl['acls'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_acl_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_ACL/%s_learned_acl_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               
                        fh.close()

                    with open("Camelot/Cisco/IOS_XE/Learned_ACL/%s_learned_acl_netgraph.html" % device.alias, "w") as fh:
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

                        with open("Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                            fh.close()

                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.md --output Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics.md --output Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_arp_netjson_json_template.render(to_parse_arp=self.learned_arp['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               
                        fh.close()

                    with open("Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    parsed_output_netjson_json = learned_arp_statistics_netjson_json_template.render(to_parse_arp=self.learned_arp['statistics'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_statistics_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()

                    with open("Camelot/Cisco/IOS_XE/Learned_ARP/%s_learned_arp_statistics_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store ARP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_arp)

                # Learned Dot1X
                if self.learned_dot1x is not None:
                    learned_dot1x_template = env.get_template('learned_dot1x.j2')
                    learned_dot1x_netjson_json_template = env.get_template('learned_dot1x_netjson_json.j2')
                    learned_dot1x_netjson_html_template = env.get_template('learned_dot1x_netjson_html.j2')
                    learned_dot1x_sessions_template = env.get_template('learned_dot1x_sessions.j2')
                    learned_dot1x_sessions_netjson_json_template = env.get_template('learned_dot1x_sessions_netjson_json.j2')
                    learned_dot1x_sessions_netjson_html_template = env.get_template('learned_dot1x_sessions_netjson_html.j2')
                    directory_names = "Learned_Dot1X"
                    file_names = "learned_dot1x" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_dot1x)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_dot1x)              

                    for filetype in filetype_loop:
                        parsed_output_type = learned_dot1x_template.render(to_parse_dot1x=self.learned_dot1x,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x.md --output Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_dot1x_netjson_json_template.render(to_parse_dot1x=self.learned_dot1x,device_alias = device.alias)
                    parsed_output_netjson_html = learned_dot1x_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()             

                    with open("Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    for filetype in filetype_loop:
                        parsed_output_type = learned_dot1x_sessions_template.render(to_parse_dot1x=self.learned_dot1x,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_sessions.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close()
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_sessions.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_sessions.md --output Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_sessions_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_dot1x_sessions_netjson_json_template.render(to_parse_dot1x=self.learned_dot1x,device_alias = device.alias)
                    parsed_output_netjson_html = learned_dot1x_sessions_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_sessions_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()

                    with open("Camelot/Cisco/IOS_XE/Learned_Dot1X/%s_learned_dot1x_sessions_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store dot1X in Device Table in Database
                    # ----------------

                    table.insert(self.learned_dot1x)

                # Learned Interface
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

                        with open("Camelot/Cisco/IOS_XE/Learned_Interface/%s_learned_interface.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close()
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_Interface/%s_learned_interface.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_Interface/%s_learned_interface.md --output Camelot/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_interface_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                    parsed_output_netjson_html = learned_interface_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    parsed_output_netjson_json = learned_interface_enable_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                    parsed_output_netjson_html = learned_interface_enable_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_enabled_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Learned_Interface/%s_learned_interface_enabled_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store Interface in Device Table in Database
                    # ----------------

                    table.insert(self.learned_interface)

                # Learned LLDP
                if self.learned_lldp is not None:
                    learned_lldp_template = env.get_template('learned_lldp.j2')
                    learned_lldp_netjson_json_template = env.get_template('learned_lldp_netjson_json.j2')
                    learned_lldp_netjson_html_template = env.get_template('learned_lldp_netjson_html.j2')
                    learned_lldp_interfaces_template = env.get_template('learned_lldp_interfaces.j2')
                    learned_lldp_interfaces_netjson_json_template = env.get_template('learned_lldp_interfaces_netjson_json.j2')
                    learned_lldp_interfaces_netjson_html_template = env.get_template('learned_lldp_interfaces_netjson_html.j2')
                    directory_names = "Learned_LLDP"
                    file_names = "learned_lldp" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_lldp)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_lldp)               

                    for filetype in filetype_loop:
                        parsed_output_type = learned_lldp_template.render(to_parse_lldp=self.learned_lldp,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp.md --output Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_lldp_netjson_json_template.render(to_parse_lldp=self.learned_lldp,device_alias = device.alias)
                    parsed_output_netjson_html = learned_lldp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    for filetype in filetype_loop:
                        parsed_output_type = learned_lldp_interfaces_template.render(to_parse_lldp=self.learned_lldp['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_interfaces.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close() 
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_interfaces.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_interfaces.md --output Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_interfaces_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_lldp_interfaces_netjson_json_template.render(to_parse_lldp=self.learned_lldp['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_lldp_interfaces_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_interfaces_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Learned_LLDP/%s_learned_lldp_interfaces_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store LLDP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_lldp)

                # Learned NTP
                if self.learned_ntp is not None:
                    learned_ntp_template = env.get_template('learned_ntp.j2')
                    learned_ntp_netjson_json_template = env.get_template('learned_ntp_netjson_json.j2')
                    learned_ntp_netjson_html_template = env.get_template('learned_ntp_netjson_html.j2')
                    learned_ntp_associations_template = env.get_template('learned_ntp_associations.j2')
                    learned_ntp_associations_netjson_json_template = env.get_template('learned_ntp_associations_netjson_json.j2')
                    learned_ntp_associations_netjson_html_template = env.get_template('learned_ntp_associations_netjson_html.j2')
                    learned_ntp_unicast_template = env.get_template('learned_ntp_unicast.j2')
                    learned_ntp_unicast_netjson_json_template = env.get_template('learned_ntp_unicast_netjson_json.j2')
                    learned_ntp_unicast_netjson_html_template = env.get_template('learned_ntp_unicast_netjson_html.j2')
                    directory_names = "Learned_NTP"
                    file_names = "learned_ntp" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_ntp)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_ntp)               

                    for filetype in filetype_loop:
                        parsed_output_type = learned_ntp_template.render(to_parse_ntp=self.learned_ntp['clock_state'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp.md --output Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_ntp_netjson_json_template.render(to_parse_ntp=self.learned_ntp['clock_state'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_ntp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()              

                    with open("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    for filetype in filetype_loop:
                        parsed_output_type = learned_ntp_associations_template.render(to_parse_ntp=self.learned_ntp['vrf'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_associations.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close()
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_associations.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_associations.md --output Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_associations_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_ntp_associations_netjson_json_template.render(to_parse_ntp=self.learned_ntp['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_ntp_associations_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_associations_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()

                    with open("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_associations_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    for filetype in filetype_loop:
                        parsed_output_type = learned_ntp_unicast_template.render(to_parse_ntp=self.learned_ntp['vrf'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_unicast.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close() 
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_unicast.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_unicast.md --output Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_unicast_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_ntp_unicast_netjson_json_template.render(to_parse_ntp=self.learned_ntp['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_ntp_unicast_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_unicast_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()              

                    with open("Camelot/Cisco/IOS_XE/Learned_NTP/%s_learned_ntp_unicast_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store NTP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_ntp)

                # Learned OSPF
                if self.learned_ospf is not None:
                    learned_ospf_template = env.get_template('learned_ospf.j2')
                    learned_ospf_netjson_json_template = env.get_template('learned_ospf_netjson_json.j2')
                    learned_ospf_netjson_html_template = env.get_template('learned_ospf_netjson_html.j2')
                    directory_names = "Learned_OSPF"
                    file_names = "learned_ospf" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_ospf)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_ospf)  

                    for filetype in filetype_loop:
                        parsed_output_type = learned_ospf_template.render(to_parse_ospf=self.learned_ospf['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_OSPF/%s_learned_ospf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_OSPF/%s_learned_ospf.md --output Camelot/Cisco/IOS_XE/Learned_OSPF/%s_learned_ospf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_ospf_netjson_json_template.render(to_parse_ospf=self.learned_ospf['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_ospf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_OSPF/%s_learned_ospf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()              

                    with open("Camelot/Cisco/IOS_XE/Learned_OSPF/%s_learned_ospf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store OSPF in Device Table in Database
                    # ----------------

                    table.insert(self.learned_ospf)

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
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_Routing/%s_learned_routing.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_Routing/%s_learned_routing.md --output Camelot/Cisco/IOS_XE/Learned_Routing/%s_learned_routing_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_routing_netjson_json_template.render(to_parse_routing=self.learned_routing['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_routing_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_Routing/%s_learned_routing_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()             

                    with open("Camelot/Cisco/IOS_XE/Learned_Routing/%s_learned_routing_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store Routing in Device Table in Database
                    # ----------------

                    table.insert(self.learned_routing)

                # Learned STP
                if self.learned_stp is not None:
                    learned_stp_template = env.get_template('learned_stp.j2')
                    learned_stp_netjson_json_template = env.get_template('learned_stp_netjson_json.j2')
                    learned_stp_netjson_html_template = env.get_template('learned_stp_netjson_html.j2')
                    learned_stp_rpvst_template = env.get_template('learned_stp_rpvst.j2')
                    learned_stp_rpvst_netjson_json_template = env.get_template('learned_stp_rpvst_netjson_json.j2')
                    learned_stp_rpvst_netjson_html_template = env.get_template('learned_stp_rpvst_netjson_html.j2')
                    directory_names = "Learned_STP"
                    file_names = "learned_stp" 

                    self.save_to_json_file(device, directory_names, file_names, self.learned_stp)
                    self.save_to_yaml_file(device, directory_names, file_names, self.learned_stp)               

                    for filetype in filetype_loop:
                        parsed_output_type = learned_stp_template.render(to_parse_stp=self.learned_stp['global'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype) 
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp.md --output Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_stp_netjson_json_template.render(to_parse_stp=self.learned_stp['global'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_stp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    for filetype in filetype_loop:
                        parsed_output_type = learned_stp_rpvst_template.render(to_parse_stp=self.learned_stp['rapid_pvst'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_rpvst.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)
                            fh.close() 
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_rpvst.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_rpvst.md --output Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_rpvst_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_stp_rpvst_netjson_json_template.render(to_parse_stp=self.learned_stp['rapid_pvst'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_stp_rpvst_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_rpvst_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Learned_STP/%s_learned_stp_rpvst_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store STP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_stp)

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
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_VLAN/%s_learned_vlan.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_VLAN/%s_learned_vlan.md --output Camelot/Cisco/IOS_XE/Learned_VLAN/%s_learned_vlan_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_vlan_netjson_json_template.render(to_parse_vlan=self.learned_vlan['vlans'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_vlan_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_VLAN/%s_learned_vlan_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Learned_VLAN/%s_learned_vlan_netgraph.html" % device.alias, "w") as fh:
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
                    directory = "Learned_VRF"
                    file_name = "learned_vrf"

                    self.save_to_json_file(device, directory, file_name, self.learned_vrf)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_vrf)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_vrf_template.render(to_parse_vrf=self.learned_vrf['vrfs'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/IOS_XE/Learned_VRF/%s_learned_vrf.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Learned_VRF/%s_learned_vrf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Learned_VRF/%s_learned_vrf.md --output Camelot/Cisco/IOS_XE/Learned_VRF/%s_learned_vrf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_vrf_netjson_json_template.render(to_parse_vrf=self.learned_vrf['vrfs'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_vrf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_VRF/%s_learned_vrf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/IOS_XE/Learned_VRF/%s_learned_vrf_netgraph.html" % device.alias, "w") as fh:
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
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists.md --output Camelot/Cisco/IOS_XE/Show_Access_Lists/%s_show_access_lists_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_access_lists_netjson_json_template.render(to_parse_access_list=self.parsed_show_access_lists,device_alias = device.alias)
                    parsed_output_netjson_html = sh_access_lists_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Learned_VLAN/%s_show_access_lists_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Learned_VLAN/%s_show_access_lists_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store ACLs in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_access_lists)

                # Show access-session
                if self.parsed_show_access_session is not None:
                    sh_access_sessions_template = env.get_template('show_access_sessions.j2')
                    sh_access_sessions_totals_template = env.get_template('show_access_sessions_totals.j2')
                    sh_access_sessions_interface_details_template = env.get_template('show_access_sessions_interface_details.j2')
                    directory_names = "Show_Access_Sessions"
                    file_names = "show_access_session" 

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.json" % (device.alias)):
                       os.remove("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.json" % (device.alias))

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.yaml" % (device.alias)):
                       os.remove("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.yaml" % (device.alias))

                    for filetype in filetype_loop:
                        if os.path.exists("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.%s" % (device.alias,filetype)):
                            os.remove("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.%s" % (device.alias,filetype))

                    with open("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.csv" % device.alias,'a') as csv:
                        csv.seek(0, 0)
                        csv.write("Interface,User Name,Mac Address,Current Policy,Domain,IPv4 Address,IPv6 Address,VLAN,Method,State,Host Mode,Session Timeout Remaining,Status")
                        csv.close()                                   

                    with open("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.md" % device.alias,'a') as md:
                        md.seek(0, 0)
                        md.write("# Show Access-Session Interface Details")
                        md.write("\n")
                        md.write("| Interface | User Name | Mac Address | Current Policy | Domain | IPv4 Address | IPv6 Address | VLAN | Method | State | Host Mode | Session Timeout Remaining | Status |")
                        md.write("\n")
                        md.write("| --------- | --------- | ----------- | -------------- | ------ | ------------ | ------------ | ---- | ------ | ----- | --------- | ------------------------- | ------ |")
                        md.close() 

                    with open("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.html" % device.alias,'a') as html:
                        html.seek(0, 0)
                        html.write("<html><body><h1>Show Access Sessions</h1><table style=\"width:100%\">")
                        html.write("\n")
                        html.write("<tr><th>Interface</th><th>User Name</th><th>MAC Address</th><th>Current Policy</th><th>Domain</th><th>IPv4 Address</th><th>IPv6 Address</th><th>VLAN</th><th>Method</th><th>State</th><th>Host Mode</th><th>Session Timeout Remaining</th><th>Status</th></tr>")                     
                        html.close() 

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_access_session)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_access_session)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_access_sessions_template.render(to_parse_access_session=self.parsed_show_access_session['interfaces'],filetype_loop_jinja2=filetype)
                        parsed_output_totals_type = sh_access_sessions_totals_template.render(to_parse_access_session=self.parsed_show_access_session,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype) 
                    
                        with open("Camelot/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_totals.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_totals_type)
                            fh.close() 

                    # ----------------
                    # Store Access Session in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_access_session)

                    # Show access-session interface <int> details
                    for interface in self.parsed_show_access_session['interfaces']:
                        self.parsed_show_ip_access_session_interface_details = ParseShowCommandFunction.parse_show_command(steps, device, "show access-session interface %s details" % interface)

                        with steps.start('Store data',continue_=True) as step:       
                            with open("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.json" % (device.alias), "a") as fid:
                                json.dump(self.parsed_show_ip_access_session_interface_details, fid, indent=4, sort_keys=True)
                                fid.write('\n')
                                
                            with open("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.yaml" % (device.alias), "a") as yml:
                                yaml.dump(self.parsed_show_ip_access_session_interface_details, yml, allow_unicode=True)
                         
                            for filetype in filetype_loop:
                                parsed_output_type = sh_access_sessions_interface_details_template.render(to_parse_access_interface_details=self.parsed_show_ip_access_session_interface_details['interfaces'],filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.%s" % (device.alias,filetype), "a") as fh:
                                    fh.write(parsed_output_type)
                                    fh.close()

                    with open("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.html" % device.alias,'a') as html:
                        html.write("</table></body></html>")
                        html.close() 
                                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details.md --output Camelot/Cisco/IOS_XE/Show_Access_Session_Interface_Details/%s_show_access_session_interface_details_mind_map.html" % (device.alias,device.alias))

                    fid.close()
                    yml.close()

                if os.path.exists("Camelot/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session.md" % device.alias):
                    os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session.md --output Camelot/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_mind_map.html" % (device.alias,device.alias))

                if os.path.exists("Camelot/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_totals.md" % device.alias):
                    os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_totals.md --output Camelot/Cisco/IOS_XE/Show_Access_Sessions/%s_show_access_session_totals_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Access Session Interface Details in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_access_session_interface_details)

                # Show Authentication Sessions
                if self.parsed_show_authentication_sessions is not None:
                    sh_authetication_sessions_template = env.get_template('show_authentication_sessions.j2')
                    sh_authetication_sessions_totals_template = env.get_template('show_authentication_sessions_totals.j2')
                    sh_authentication_sessions_interface_details_template = env.get_template('show_authentication_sessions_interface_details.j2')
                    directory_names = "Show_Authentication_Sessions"
                    file_names = "show_authentication_sessions"

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.json" % (device.alias)):
                       os.remove("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.json" % (device.alias))

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.yaml" % (device.alias)):
                       os.remove("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.yaml" % (device.alias))

                    for filetype in filetype_loop:
                        if os.path.exists("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.%s" % (device.alias,filetype)):
                            os.remove("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.%s" % (device.alias,filetype))

                    with open("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.csv" % device.alias,'a') as csv:
                        csv.seek(0, 0)
                        csv.write("Interface,User Name,Mac Address,Current Policy,Domain,IPv4 Address,IPv6 Address,VLAN,Method,State,Host Mode,Session Timeout Remaining,Status")
                        csv.close()                                   

                    with open("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.md" % device.alias,'a') as md:
                        md.seek(0, 0)
                        md.write("# Show Authentication Session Interface Details")
                        md.write("\n")
                        md.write("| Interface | User Name | Mac Address | Current Policy | Domain | IPv4 Address | IPv6 Address | VLAN | Method | State | Host Mode | Session Timeout Remaining | Status |")
                        md.write("\n")
                        md.write("| --------- | --------- | ----------- | -------------- | ------ | ------------ | ------------ | ---- | ------ | ----- | --------- | ------------------------- | ------ |")
                        md.close() 

                    with open("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.html" % device.alias,'a') as html:
                        html.seek(0, 0)
                        html.write("<html><body><h1>Show Authentication Sessions</h1><table style=\"width:100%\">")
                        html.write("\n")
                        html.write("<tr><th>Interface</th><th>User Name</th><th>MAC Address</th><th>Current Policy</th><th>Domain</th><th>IPv4 Address</th><th>IPv6 Address</th><th>VLAN</th><th>Method</th><th>State</th><th>Host Mode</th><th>Session Timeout Remaining</th><th>Status</th></tr>")                     
                        html.close()

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_authentication_sessions)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_authentication_sessions)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_authetication_sessions_template.render(to_parse_authentication_sessions=self.parsed_show_authentication_sessions['interfaces'],filetype_loop_jinja2=filetype)
                        parsed_output_totals_type = sh_authetication_sessions_totals_template.render(to_parse_authentication_sessions=self.parsed_show_authentication_sessions,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)
                    
                        with open("Camelot/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_session_totals.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_totals_type)
                            fh.close()

                    # ----------------
                    # Store Authentication Session in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_authentication_sessions)

                    # Show authentication session interface <int> details
                    for interface in self.parsed_show_authentication_sessions['interfaces']:
                        self.parsed_show_authentication_session_interface_details = ParseShowCommandFunction.parse_show_command(steps, device, "show authentication session interface %s details" % interface)

                        with steps.start('Store data',continue_=True) as step:       
                            with open("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.json" % (device.alias), "a") as fid:
                                json.dump(self.parsed_show_authentication_session_interface_details, fid, indent=4, sort_keys=True)
                                fid.write('\n')
                                
                            with open("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.yaml" % (device.alias), "a") as yml:
                                yaml.dump(self.parsed_show_authentication_session_interface_details, yml, allow_unicode=True)
                         
                            for filetype in filetype_loop:
                                parsed_output_type = sh_authentication_sessions_interface_details_template.render(to_parse_access_interface_details=self.parsed_show_authentication_session_interface_details['interfaces'],filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.%s" % (device.alias,filetype), "a") as fh:
                                    fh.write(parsed_output_type)

                    with open("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.html" % device.alias,'a') as html:
                        html.write("</table></body></html>")
                        html.close() 
                                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details.md --output Camelot/Cisco/IOS_XE/Show_Authentication_Session_Interface_Details/%s_show_authentication_session_interface_details_mind_map.html" % (device.alias,device.alias))
                    
                    fh.close()
                    fid.close()
                    yml.close()

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions.md --output Camelot/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_sessions_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_session_totals.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_session_totals.md --output Camelot/Cisco/IOS_XE/Show_Authentication_Sessions/%s_show_authentication_session_totals_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Authentication Session Interface Details in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_authentication_session_interface_details)

                # Show CDP Neighbors
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
                                       
                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors.md --output Camelot/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_cdp_neighbors_netjson_json_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors['cdp'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_cdp_neighbors_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()

                    with open("Camelot/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_netgraph.html" % device.alias, "w") as fh:
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

                        with open("Camelot/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_totals)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail.md --output Camelot/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_CDP_Neighbors/%s_show_cdp_neighbors_detail_totals.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals.md --output Camelot/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_totals_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_cdp_neighbors_detail_netjson_json_template.render(to_parse_cdp_neighbors=self.parsed_show_cdp_neighbors_detail['index'],filetype_loop_jinja2=filetype,device_ip = device.connections.cli.ip)
                    parsed_output_netjson_html = sh_cdp_neighbors_detail_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()               

                    with open("Camelot/Cisco/IOS_XE/Show_CDP_Neighbors_Details/%s_show_cdp_neighbors_detail_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store CDP Neighbors Details in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_cdp_neighbors_detail)

                # Show environment all
                if self.parsed_show_environment is not None:
                    sh_environment_template = env.get_template('show_environment_all.j2')
                    directory_names = "Show_Environment"
                    file_names = "show_environment" 

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_environment)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_environment)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_environment_template.render(to_parse_environment=self.parsed_show_environment['switch'],filetype_loop_jinja2=filetype)
                      
                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Environment/%s_show_environment.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Environment/%s_show_environment.md --output Camelot/Cisco/IOS_XE/Show_Environment/%s_show_environment_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Environment in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_environment)

                # Show etherchannel summary
                if self.parsed_show_etherchannel_summary is not None:
                    sh_etherchannel_summary_template = env.get_template('show_etherchannel_summary.j2')
                    sh_etherchannel_summary_totals_template = env.get_template('show_etherchannel_summary_totals.j2')
                    directory_names = "Show_Etherchannel_Summary"
                    file_names = "show_etherchannel_summary"

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_etherchannel_summary)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_etherchannel_summary)

                    for filetype in filetype_loop: 
                        parsed_output_type = None
                        if 'interfaces' in self.parsed_show_etherchannel_summary:                          
                            parsed_output_type = sh_etherchannel_summary_template.render(to_parse_etherchannel_summary=self.parsed_show_etherchannel_summary['interfaces'],filetype_loop_jinja2=filetype)
                        parsed_totals = sh_etherchannel_summary_totals_template.render(to_parse_etherchannel_summary=self.parsed_show_etherchannel_summary,filetype_loop_jinja2=filetype)
                      
                        if parsed_output_type in locals():                                                    
                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                        with open("Camelot/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_totals)
                          fh.close()

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary.md --output Camelot/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals.md --output Camelot/Cisco/IOS_XE/Show_Etherchannel_Summary/%s_show_etherchannel_summary_totals_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store EtherChannel in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_etherchannel_summary)

                # Show interfaces
                if self.parsed_show_int is not None:
                    sh_int_template = env.get_template('show_interfaces.j2')
                    directory_names = "Show_Interfaces"
                    file_names = "show_int"

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_int)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_int)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_int_template.render(to_parse_interfaces=self.parsed_show_int,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Interfaces/%s_show_int.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Interfaces/%s_show_int.md --output Camelot/Cisco/IOS_XE/Show_Interfaces/%s_show_int_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Interfaces in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_int)

                # Show interfaces status
                if self.parsed_show_int_status is not None:
                    sh_int_status_template = env.get_template('show_int_status.j2')
                    directory_names = "Show_Interfaces_Status"
                    file_names = "show_int_status"

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_int_status)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_int_status)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_int_status_template.render(to_parse_interfaces=self.parsed_show_int_status['interfaces'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status.md --output Camelot/Cisco/IOS_XE/Show_Interfaces_Status/%s_show_int_status_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Interface Status in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_int_status)

                # Show interfaces trunk
                if self.parsed_show_interfaces_trunk is not None:
                    sh_interfaces_trunk_template = env.get_template('show_interfaces_trunk.j2')
                    directory_names = "Show_Interfaces_Trunk"
                    file_names = "show_interfaces_trunk"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_interfaces_trunk)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_interfaces_trunk)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_interfaces_trunk_template.render(to_parse_interfaces_trunk=self.parsed_show_interfaces_trunk['interface'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk.md --output Camelot/Cisco/IOS_XE/Show_Interfaces_Trunk/%s_show_interfaces_trunk_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Interface Status in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_interfaces_trunk)

                # Show Inventory
                if self.parsed_show_inventory is not None:
                    # 4500
                    sh_inventory_4500_template = env.get_template('show_inventory_4500.j2')

                    # 3850
                    sh_inventory_3850_template = env.get_template('show_inventory_3850.j2')

                    # 9300
                    sh_inventory_9300_template = env.get_template('show_inventory_9300.j2')

                    directory_names = "Show_Inventory"
                    file_names = "show_inventory" 

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_inventory)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_inventory)

                    for filetype in filetype_loop:
                        # 4500
                        if device.platform == "cat4500":
                            parsed_output_type = sh_inventory_4500_template.render(to_parse_inventory=self.parsed_show_inventory['main'],filetype_loop_jinja2=filetype)

                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                            if os.path.exists("Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md" % device.alias):
                                os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                        # 3850
                        elif device.platform == "cat3850":
                            parsed_output_type = sh_inventory_3850_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],filetype_loop_jinja2=filetype)

                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                            if os.path.exists("Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md" % device.alias):
                                os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                        # 9300
                        elif device.platform == "cat9300":
                            parsed_output_type = sh_inventory_9300_template.render(to_parse_inventory=self.parsed_show_inventory['slot'],filetype_loop_jinja2=filetype)
  
                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                            if os.path.exists("Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md" % device.alias):
                                os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory.md --output Camelot/Cisco/IOS_XE/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Inventory in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_inventory)

                # Show ip arp
                if self.parsed_show_ip_arp is not None:
                    sh_ip_arp_template = env.get_template('show_ip_arp.j2')
                    directory_names = "Show_IP_ARP"
                    file_names = "show_ip_arp"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_arp)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_arp)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_ip_arp_template.render(to_parse_ip_arp=self.parsed_show_ip_arp['interfaces'],filetype_loop_jinja2=filetype)
                      
                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp.md --output Camelot/Cisco/IOS_XE/Show_IP_ARP/%s_show_ip_arp_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP ARP in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_arp)

                # Show ip interface brief
                if self.parsed_show_ip_int_brief is not None:
                    sh_ip_int_brief_template = env.get_template('show_ip_int_brief.j2')
                    directory_names = "Show_IP_Interface_Brief"
                    file_names = "show_ip_int_brief"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_int_brief)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_int_brief)               
        
                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_int_brief_template.render(to_parse_interfaces=self.parsed_show_ip_int_brief['interface'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief.md --output Camelot/Cisco/IOS_XE/Show_IP_Interface_Brief/%s_show_ip_int_brief_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP Int Brief in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_int_brief)

                # Show IP OSPF
                if self.parsed_show_ip_ospf is not None:
                    sh_ip_ospf_template = env.get_template('show_ip_ospf.j2')
                    directory_names = "Show_IP_OSPF"
                    file_names = "show_ip_ospf"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_ospf)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_ospf)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf.md --output Camelot/Cisco/IOS_XE/Show_IP_OSPF/%s_show_ip_ospf_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP OSPF in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf)

                # Show IP OSPF Database
                if self.parsed_show_ip_ospf_database is not None:
                    sh_ip_ospf_database_template = env.get_template('show_ip_ospf_database.j2')
                    directory_names = "Show_IP_OSPF_Database"
                    file_names = "show_ip_ospf_database"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_access_lists)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_access_lists)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_database_template.render(to_parse_ip_ospf_database=self.parsed_show_ip_ospf_database['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database.md --output Camelot/Cisco/IOS_XE/Show_IP_OSPF_Database/%s_show_ip_ospf_database_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP OSPF Database in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf_database)

                # Show IP OSPF Interface
                if self.parsed_show_ip_ospf_interface is not None:
                    sh_ip_ospf_interface_template = env.get_template('show_ip_ospf_interface.j2')
                    directory_names = "Show_IP_OSPF_Interface"
                    file_names = "show_ip_ospf_interface"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_ospf_interface)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_ospf_interface)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_interface_template.render(to_parse_ip_ospf_interface=self.parsed_show_ip_ospf_interface['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface.md --output Camelot/Cisco/IOS_XE/Show_IP_OSPF_Interface/%s_show_ip_ospf_interface_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP OSPF Interface in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf_interface)

                # Show IP OSPF Neighbor
                if self.parsed_show_ip_ospf_neighbor is not None:
                    sh_ip_ospf_neighbor_template = env.get_template('show_ip_ospf_neighbor.j2')
                    directory_names = "Show_IP_OSPF_Neighbor"
                    file_names = "show_ip_ospf_neighbor"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_ospf_neighbor)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_ospf_neighbor)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_neighbor_template.render(to_parse_ip_ospf_neighbor=self.parsed_show_ip_ospf_neighbor['interfaces'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor.md --output Camelot/Cisco/IOS_XE/Show_IP_OSPF_Neighbor/%s_show_ip_ospf_neighbor_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store IP OSPF Neighbor in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf_neighbor)

                # Show IP OSPF Neighbor Detail
                if self.parsed_show_ip_ospf_neighbor_detail is not None:
                    sh_ip_ospf_neighbor_detail_template = env.get_template('show_ip_ospf_neighbor_detail.j2')
                    directory_names = "Show_IP_OSPF_Neighbor_Detail"
                    file_names = "show_ip_ospf_neighbor_detail"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ip_ospf_neighbor_detail)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ip_ospf_neighbor_detail)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_neighbor_detail_template.render(to_parse_ip_ospf_neighbor_detail=self.parsed_show_ip_ospf_neighbor_detail['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail.md --output Camelot/Cisco/IOS_XE/Show_IP_OSPF_Neighbor_Detail/%s_show_ip_ospf_neighbor_detail_mind_map.html" % (device.alias,device.alias))

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
                    
                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route.md --output Camelot/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_route_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_route_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)
                        fh.close()              

                    with open("Camelot/Cisco/IOS_XE/Show_IP_Route/%s_show_ip_route_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)
                        fh.close()

                    # ----------------
                    # Store IP Route Brief in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ip_route)

                # Show ISSU State Details
                if device.platform == "cat4500":
                    if self.parsed_show_issu_state is not None:
                        sh_issu_state_template = env.get_template('show_issu_state.j2')
                        directory_names = "Show_ISSU_State"
                        file_names = "show_issu_state"                    
                    
                        self.save_to_json_file(device, directory_names, file_names, self.parsed_show_issu_state)
                        self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_issu_state)                   
                    
                        for filetype in filetype_loop:
                            parsed_output_type = sh_issu_state_template.render(to_parse_issu_state=self.parsed_show_issu_state['slot'],filetype_loop_jinja2=filetype)

                            self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                        if os.path.exists("Camelot/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.md" % device.alias):
                            os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state.md --output Camelot/Cisco/IOS_XE/Show_ISSU_State/%s_show_issu_state_mind_map.html" % (device.alias,device.alias))

                        # ----------------
                        # Store ISSU State Details in Device Table in Database
                        # ----------------

                        table.insert(self.parsed_show_issu_state)

                # Show mac address-table
                if self.parsed_show_mac_address_table is not None:
                    sh_mac_address_table_template = env.get_template('show_mac_address_table.j2')
                    directory_names = "Show_MAC_Address_Table"
                    file_names = "show_mac_address_table"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_mac_address_table)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_mac_address_table)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_mac_address_table_template.render(to_parse_mac_address_table=self.parsed_show_mac_address_table['mac_table'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table.md --output Camelot/Cisco/IOS_XE/Show_MAC_Address_Table/%s_show_mac_address_table_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store MAC Address Table in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_mac_address_table)

                # Show ntp associations
                if self.parsed_show_ntp_associations is not None:
                    sh_ntp_associations_template = env.get_template('show_ntp_associations.j2')
                    directory_names = "Show_NTP_Associations"
                    file_names = "show_ntp_associations"                    
                    
                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_ntp_associations)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_ntp_associations)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_ntp_associations_template.render(to_parse_ntp_associations=self.parsed_show_ntp_associations,filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)                                                                     

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations.md --output Camelot/Cisco/IOS_XE/Show_NTP_Associations/%s_show_ntp_associations_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store NTP in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_ntp_associations)

                # Show power inline
                if self.parsed_show_power_inline is not None:
                    sh_power_inline_template = env.get_template('show_power_inline.j2')
                    sh_power_inline_totals_template = env.get_template('show_power_inline_totals.j2')
                    directory_names = "Show_Power_Inline"
                    file_names = "show_power_inline"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_power_inline)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_power_inline)

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_power_inline_template.render(to_parse_power_inline=self.parsed_show_power_inline['interface'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)                                                                 

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline.md --output Camelot/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_mind_map.html" % (device.alias,device.alias))

                    total_avail_counter = 0
                    total_used_counter = 0

                    for interface,value in self.parsed_show_power_inline['interface'].items():          
                        total_avail_counter += value['max']
                        total_used_counter += value['power']

                    for filetype in filetype_loop:  
                        parsed_output_type = sh_power_inline_totals_template.render(total_avail=total_avail_counter,total_used=total_used_counter,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_totals.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)                                                                     

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_totals.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_totals.md --output Camelot/Cisco/IOS_XE/Show_Power_Inline/%s_show_power_inline_totals_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Power Inline in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_power_inline)

                # Show version
                if self.parsed_show_version is not None:
                    sh_ver_template = env.get_template('show_version.j2')
                    directory_names = "Show_Version"
                    file_names = "show_version"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_version)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_version)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ver_template.render(to_parse_version=self.parsed_show_version['version'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_Version/%s_show_version.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Version/%s_show_version.md --output Camelot/Cisco/IOS_XE/Show_Version/%s_show_version_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store Version in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_version)

                # Show vlan
                if self.parsed_show_vlan is not None:
                    sh_vlan_template = env.get_template('show_vlan.j2')
                    directory_names = "Show_VLAN"
                    file_names = "show_vlan"                    

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_vlan)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_vlan)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_vlan_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_VLAN/%s_show_vlan.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_VLAN/%s_show_vlan.md --output Camelot/Cisco/IOS_XE/Show_VLAN/%s_show_vlan_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store VLAN in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_vlan)

                # Show vrf
                if self.parsed_show_vrf is not None:
                    sh_vrf_template = env.get_template('show_vrf.j2')
                    sh_ip_arp_vrf_template = env.get_template('show_ip_arp.j2')
                    sh_ip_route_template = env.get_template('show_ip_route.j2')
                    directory_names = "Show_VRF"
                    file_names = "show_vrf"  

                    self.save_to_json_file(device, directory_names, file_names, self.parsed_show_vrf)
                    self.save_to_yaml_file(device, directory_names, file_names, self.parsed_show_vrf)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_template.render(to_parse_vrf=self.parsed_show_vrf['vrf'],filetype_loop_jinja2=filetype)

                        self.save_to_specified_file_type(device, directory_names, file_names, parsed_output_type, filetype)

                    if os.path.exists("Camelot/Cisco/IOS_XE/Show_VRF/%s_show_vrf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_VRF/%s_show_vrf.md --output Camelot/Cisco/IOS_XE/Show_VRF/%s_show_vrf_mind_map.html" % (device.alias,device.alias))

                    # ----------------
                    # Store VRF in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_vrf)

                    # For Each VRF
                    for vrf in self.parsed_show_vrf['vrf']:
                      
                        # Show IP ARP VRF <VRF> 
                        with steps.start('Parsing ip arp vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_arp_vrf = device.parse("show ip arp vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))
                        if hasattr(Collect_Information, 'self.parsed_show_ip_arp_vrf'):
                            with steps.start('Store data',continue_=True) as step:

                                with open("Camelot/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                    json.dump(self.parsed_show_ip_arp_vrf, fid, indent=4, sort_keys=True)
                                    fid.close()

                                with open("Camelot/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                    yaml.dump(self.parsed_show_ip_arp_vrf, yml, allow_unicode=True)
                                    yml.close()

                                for filetype in filetype_loop:
                                    parsed_output_type = sh_ip_arp_vrf_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['interfaces'],filetype_loop_jinja2=filetype)

                                    with open("Camelot/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                        fh.write(parsed_output_type)
                                        fh.close()

                                if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md" % (device.alias,vrf)):
                                    os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md --output Camelot/Cisco/IOS_XE/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                                # ----------------
                                # Store IP ARP VRF in Device Table in Database
                                # ----------------

                                table.insert(self.parsed_show_ip_arp_vrf)

                        # Show IP ROUTE VRF <VRF>
                        with steps.start('Parsing ip route vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_route_vrf = device.parse("show ip route vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        if hasattr(Collect_Information, 'self.parsed_show_ip_route_vrf'):
                            with steps.start('Store data',continue_=True) as step:

                                with open("Camelot/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                    json.dump(self.parsed_show_ip_route_vrf, fid, indent=4, sort_keys=True)
                                    fid.close()

                                with open("Camelot/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                    yaml.dump(self.parsed_show_ip_route_vrf, yml, allow_unicode=True)
                                    yml.close()
                         
                                for filetype in filetype_loop:
                                    parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route_vrf['vrf'],filetype_loop_jinja2=filetype)

                                    with open("Camelot/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                        fh.write(parsed_output_type)
                                        fh.close()

                                if os.path.exists("Camelot/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md" % (device.alias,vrf)):
                                        os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md --output Camelot/Cisco/IOS_XE/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                                # ----------------
                                # Store IP Route VRF in Device Table in Database
                                # ----------------

                                table.insert(self.parsed_show_ip_route_vrf)

        db.close()
        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED)))    

# ----------------
# Save Functions 
# ----------------
    def save_to_json_file(self, device, directory, file_name, content):
        file_path = "Camelot/Cisco/IOS_XE/{}/{}_{}.json".format(directory, device.alias, file_name)
        with open(file_path, "w") as json_file:
            json.dump(content, json_file, indent=4, sort_keys=True)
            json_file.close()
    
    def save_to_yaml_file(self, device, directory, file_name, content):
        file_path = "Camelot/Cisco/IOS_XE/{}/{}_{}.yaml".format(directory, device.alias, file_name)
        with open(file_path, "w") as yml_file:
            yaml.dump(content, yml_file, allow_unicode=True)
            yml_file.close()
    
    def save_to_specified_file_type(self, device, directory, file_name, content, file_type):
        file_path = "Camelot/Cisco/IOS_XE/{}/{}_{}.{}".format(directory, device.alias, file_name, file_type)
        with open(file_path, "w") as opened_file:
            opened_file.write(content)
            opened_file.close()
