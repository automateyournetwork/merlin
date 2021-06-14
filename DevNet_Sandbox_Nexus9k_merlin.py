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

if os.path.exists("Camelot/Cisco/DevNet_Sandbox/The_Grail/Nexus9K_Grail_DB.json"):
    os.remove("Camelot/Cisco/DevNet_Sandbox/The_Grail/Nexus9K_Grail_DB.json")

db = TinyDB('Camelot/Cisco/DevNet_Sandbox/The_Grail/Nexus9K_Grail_DB.json')

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
            # show bgp process vrf all
            self.parsed_show_bgp_process_vrf_all = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp process vrf all")
            # Show BGP Sessions
            self.parsed_show_bgp_sessions = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp sessions")
            # Show Interfaces Status
            self.parsed_show_int_status = ParseShowCommandFunction.parse_show_command(steps, device, "show interface status")
            # Show Inventory
            self.parsed_show_inventory = ParseShowCommandFunction.parse_show_command(steps, device, "show inventory")
            # Show IP Interface Brief
            self.parsed_show_ip_int_brief = ParseShowCommandFunction.parse_show_command(steps, device, "show ip interface brief")
            # Show IP OSPF
            self.parsed_show_ip_ospf = ParseShowCommandFunction.parse_show_command(steps, device, "show ip ospf")
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
            # show VRF all detail
            self.parsed_show_vrf_all_detail = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf all detail")
            # show vrf all interface
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
                    directory = "Learned_ACL"
                    file_name = "learned_acl"

                    self.save_to_json_file(device, directory, file_name, self.learned_acl)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_acl)            

                    for filetype in filetype_loop:
                        parsed_output_type = learned_acl_template.render(to_parse_access_list=self.learned_acl['acls'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl.md --output Camelot/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_acl_netjson_json_template.render(to_parse_access_list=self.learned_acl['acls'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_acl_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_ACL/%s_learned_acl_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

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
                    directory = "Learned_ARP"
                    file_name = "learned_arp"

                    self.save_to_json_file(device, directory, file_name, self.learned_arp)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_arp)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_arp_template.render(to_parse_arp=self.learned_arp['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 

                    for filetype in filetype_loop:
                        parsed_output_type = learned_arp_statistics_template.render(to_parse_arp=self.learned_arp['statistics'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.md --output Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_mind_map.html" % (device.alias,device.alias))

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics.md --output Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_arp_netjson_json_template.render(to_parse_arp=self.learned_arp['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    parsed_output_netjson_json = learned_arp_statistics_netjson_json_template.render(to_parse_arp=self.learned_arp['statistics'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_arp_statistics_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_ARP/%s_learned_arp_statistics_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store ARP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_arp)

                # Learned BGP
                if self.learned_bgp is not None:
                    learned_bgp_template = env.get_template('learned_bgp.j2')
                    learned_bgp_netjson_json_template = env.get_template('learned_bgp_netjson_json.j2')
                    learned_bgp_netjson_html_template = env.get_template('learned_bgp_netjson_html.j2')
                    directory = "Learned_BGP"
                    file_name = "learned_bgp"

                    self.save_to_json_file(device, directory, file_name, self.learned_bgp)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_bgp)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_bgp_template.render(to_parse_bgp=self.learned_bgp['instance'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp.md --output Camelot/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_bgp_netjson_json_template.render(to_parse_bgp=self.learned_bgp['instance'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_bgp_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_BGP/%s_learned_bgp_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store BGP in Device Table in Database
                    # ----------------

                    table.insert(self.learned_bgp)

                # Learned Interface
                if self.learned_interface is not None:
                    learned_interface_template = env.get_template('learned_interface.j2')
                    learned_interface_netjson_json_template = env.get_template('learned_interface_netjson_json.j2')
                    learned_interface_netjson_html_template = env.get_template('learned_interface_netjson_html.j2')
                    learned_interface_enable_netjson_json_template = env.get_template('learned_interface_enabled_netjson_json.j2')
                    learned_interface_enable_netjson_html_template = env.get_template('learned_interface_enabled_netjson_html.j2')
                    directory = "Learned_Interface"
                    file_name = "learned_interface"

                    self.save_to_json_file(device, directory, file_name, self.learned_interface)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_interface)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_interface_template.render(to_parse_interface=self.learned_interface,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface.md --output Camelot/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_interface_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                    parsed_output_netjson_html = learned_interface_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    parsed_output_netjson_json = learned_interface_enable_netjson_json_template.render(to_parse_interface=self.learned_interface,device_alias = device.alias)
                    parsed_output_netjson_html = learned_interface_enable_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_enabled_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Interface/%s_learned_interface_enabled_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)                        

                    # ----------------
                    # Store Interface in Device Table in Database
                    # ----------------

                    table.insert(self.learned_interface)

                # Learned OSPF
                if self.learned_ospf is not None:
                    learned_ospf_template = env.get_template('learned_ospf.j2')
                    learned_ospf_netjson_json_template = env.get_template('learned_ospf_netjson_json.j2')
                    learned_ospf_netjson_html_template = env.get_template('learned_ospf_netjson_html.j2')

                    directory = "Learned_OSPF"
                    file_name = "learned_ospf"
                    self.save_to_json_file(device, directory, file_name, self.learned_ospf)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_ospf)

                    # ----------------
                    # Store OSPF in Device Table in Database
                    # ----------------

                    table.insert(self.learned_ospf)

                # Learned Platform
                if self.learned_platform is not None:
                    learned_platform_template = env.get_template('learned_platform.j2')
                    learned_platform_netjson_json_template = env.get_template('learned_platform_netjson_json.j2')
                    learned_platform_netjson_html_template = env.get_template('learned_platform_netjson_html.j2')
                    directory = "Learned_Platform"
                    file_name = "learned_platform"

                    self.save_to_json_file(device, directory, file_name, self.learned_platform)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_platform)            

                    for filetype in filetype_loop:
                        parsed_output_type = learned_platform_template.render(to_parse_platform=self.learned_platform,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_Platform/%s_learned_platform.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_Platform/%s_learned_platform.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_Platform/%s_learned_platform.md --output Camelot/Cisco/DevNet_Sandbox/Learned_Platform/%s_learned_platform_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_platform_netjson_json_template.render(to_parse_platform=self.learned_platform,device_alias = device.alias)
                    parsed_output_netjson_html = learned_platform_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Platform/%s_learned_platform_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Platform/%s_learned_platform_netgraph.html" % device.alias, "w") as fh:
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
                    directory = "Learned_Routing"
                    file_name = "learned_routing"

                    self.save_to_json_file(device, directory, file_name, self.learned_routing)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_routing)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_routing_template.render(to_parse_routing=self.learned_routing['vrf'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing.md --output Camelot/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_routing_netjson_json_template.render(to_parse_routing=self.learned_routing['vrf'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_routing_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/%s_learned_routing_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Routing in Device Table in Database
                    # ----------------

                    table.insert(self.learned_routing)

                # Learned VLAN
                if self.learned_vlan is not None:
                    learned_vlan_template = env.get_template('learned_vlan.j2')
                    learned_vlan_netjson_json_template = env.get_template('learned_vlan_netjson_json.j2')
                    learned_vlan_netjson_html_template = env.get_template('learned_vlan_netjson_html.j2')
                    directory = "Learned_VLAN"
                    file_name = "learned_vlan"

                    self.save_to_json_file(device, directory, file_name, self.learned_vlan)
                    self.save_to_yaml_file(device, directory, file_name, self.learned_vlan)

                    for filetype in filetype_loop:
                        parsed_output_type = learned_vlan_template.render(to_parse_vlan=self.learned_vlan['vlans'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan.md --output Camelot/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_vlan_netjson_json_template.render(to_parse_vlan=self.learned_vlan['vlans'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_vlan_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_VLAN/%s_learned_vlan_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

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

                        with open("Camelot/Cisco/DevNet_Sandbox/Learned_VRF/%s_learned_vrf.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Learned_VRF/%s_learned_vrf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Learned_VRF/%s_learned_vrf.md --output Camelot/Cisco/DevNet_Sandbox/Learned_VRF/%s_learned_vrf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = learned_vrf_netjson_json_template.render(to_parse_vrf=self.learned_vrf['vrfs'],device_alias = device.alias)
                    parsed_output_netjson_html = learned_vrf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_VRF/%s_learned_vrf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_VRF/%s_learned_vrf_netgraph.html" % device.alias, "w") as fh:
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
                    directory = "Show_Access_Lists"
                    file_name = "show_access_lists"

                    self.save_to_json_file(device, directory, file_name, self.parsed_show_access_lists)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_access_lists)
                    # with open("Camelot/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.json" % device.alias, "w") as fid:
                    #   json.dump(self.parsed_show_access_lists, fid, indent=4, sort_keys=True)

                    # with open("Camelot/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.yaml" % device.alias, "w") as yml:
                    #   yaml.dump(self.parsed_show_access_lists, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_access_lists_template.render(to_parse_access_list=self.parsed_show_access_lists,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists.md --output Camelot/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_access_lists_netjson_json_template.render(to_parse_access_list=self.parsed_show_access_lists,device_alias = device.alias)
                    parsed_output_netjson_html = sh_access_lists_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Access_Lists/%s_show_access_lists_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store ACLs in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_access_lists)

                # Show BGP process vrf all
                if self.parsed_show_bgp_process_vrf_all is not None:
                    sh_bgp_process_vrf_all_template = env.get_template('show_bgp_process_vrf_all.j2')                  
                    sh_bgp_process_vrf_all_netjson_json_template = env.get_template('show_bgp_process_vrf_all_netjson_json.j2')
                    sh_bgp_process_vrf_all_netjson_html_template = env.get_template('show_bgp_process_vrf_all_netjson_html.j2')
                    
                    directory = "Show_BGP_Process_VRF_All"
                    file_name = "show_bgp_process_vfr_all"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_bgp_process_vrf_all)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_bgp_process_vrf_all)
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_bgp_process_vrf_all_template.render(to_parse_bgp=self.parsed_show_bgp_process_vrf_all,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all.md --output Camelot/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_bgp_process_vrf_all_netjson_json_template.render(to_parse_bgp=self.parsed_show_bgp_process_vrf_all,device_alias = device.alias)
                    parsed_output_netjson_html = sh_bgp_process_vrf_all_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_BGP_Process_VRF_All/%s_show_bgp_process_vrf_all_netgraph.html" % device.alias, "w") as fh:
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
                    directory = "Show_BGP_Sessions"
                    file_name = "show_bgp_sessions"

                    self.save_to_json_file(device, directory, file_name, self.parsed_show_bgp_sessions)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_bgp_sessions)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_bgp_sessions_template.render(to_parse_bgp=self.parsed_show_bgp_sessions,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type) 
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions.md --output Camelot/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_bgp_sessions_netjson_json_template.render(to_parse_bgp=self.parsed_show_bgp_sessions,device_alias = device.alias)
                    parsed_output_netjson_html = sh_bgp_sessions_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_BGP_Sessions/%s_show_bgp_sessions_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store BGP Sessions in Device Table in Database
                    # ----------------

                    table.insert(self.parsed_show_bgp_sessions)

                # Show interface status
                if self.parsed_show_int_status is not None:
                    sh_int_status_template = env.get_template('show_interface_status.j2')
                    sh_int_status_netjson_json_template = env.get_template('show_interface_status_netjson_json.j2')
                    sh_int_status_netjson_html_template = env.get_template('show_interface_status_netjson_html.j2')
                    sh_int_status_connected_netjson_json_template = env.get_template('show_interface_status_connected_netjson_json.j2')
                    sh_int_status_connected_netjson_html_template = env.get_template('show_interface_status_connected_netjson_html.j2')

                    directory = "Show_Interface_Status"
                    file_name = "show_int_status"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_int_status)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_int_status)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_int_status_template.render(to_parse_interface=self.parsed_show_int_status['interfaces'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)  

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status.md --output Camelot/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_int_status_netjson_json_template.render(to_parse_interface=self.parsed_show_int_status['interfaces'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_int_status_netjson_html_template.render(device_alias = device.alias)
                    parsed_output_connected_netjson_json = sh_int_status_connected_netjson_json_template.render(to_parse_interface=self.parsed_show_int_status['interfaces'],device_alias = device.alias)
                    parsed_output_connected_netjson_html = sh_int_status_connected_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_connected_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_connected_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Interface_Status/%s_show_int_status_connected_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_connected_netjson_html)

                # Show Inventory
                if self.parsed_show_inventory is not None:
                    # Nexus 
                    sh_inventory_nexus_template = env.get_template('show_inventory.j2')
                    sh_inventory_netjson_json_template = env.get_template('show_inventory_netjson_json.j2')
                    sh_inventory_netjson_html_template = env.get_template('show_inventory_netjson_html.j2')

                    directory = "Show_Inventory"
                    file_name = "show_inventory"

                    self.save_to_json_file(device, directory, file_name, self.parsed_show_inventory)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_inventory)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_inventory_nexus_template.render(to_parse_inventory_name=self.parsed_show_inventory['name'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                        if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.md" % device.alias):
                            os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory.md --output Camelot/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_inventory_netjson_json_template.render(to_parse_inventory_name=self.parsed_show_inventory['name'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_inventory_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Inventory/%s_show_inventory_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Inventory in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_inventory)

                # Show ip interface brief
                if self.parsed_show_ip_int_brief is not None:
                    sh_ip_int_brief_template = env.get_template('show_ip_interface_brief.j2')
                    sh_ip_int_brief_netjson_json_template = env.get_template('show_ip_interface_brief_netjson_json.j2')
                    sh_ip_int_brief_netjson_html_template = env.get_template('show_ip_interface_brief_netjson_html.j2')

                    directory = "Show_IP_Interface_Brief"
                    file_name = "show_ip_int_brief"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_ip_int_brief)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_ip_int_brief)              
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_int_brief_template.render(to_parse_interfaces=self.parsed_show_ip_int_brief['interface'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief.md --output Camelot/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_int_brief_netjson_json_template.render(to_parse_interfaces=self.parsed_show_ip_int_brief['interface'],device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_int_brief_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_int_brief_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store IP Int Brief in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_ip_int_brief)

                # Show IP OSPF
                if self.parsed_show_ip_ospf is not None:
                    sh_ip_ospf_template = env.get_template('show_ip_ospf.j2')
                    sh_ip_ospf_netjson_json_template = env.get_template('show_ip_ospf_netjson_json.j2')
                    sh_ip_ospf_netjson_html_template = env.get_template('show_ip_ospf_netjson_html.j2')

                    directory = "Show_IP_OSPF"
                    file_name = "show_ip_ospf"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_ip_ospf)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_ip_ospf)              
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_ospf_template.render(to_parse_ip_ospf=self.parsed_show_ip_ospf['vrf'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf.md --output Camelot/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_ospf_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_ospf['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_ospf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_OSPF/%s_show_ip_ospf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store IP OSPF in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_ip_ospf)

                # Show ip Route
                if self.parsed_show_ip_route is not None:
                    sh_ip_route_template = env.get_template('show_ip_route.j2')
                    sh_ip_route_netjson_json_template = env.get_template('show_ip_route_netjson_json.j2')
                    sh_ip_route_netjson_html_template = env.get_template('show_ip_route_netjson_html.j2')

                    directory = "Show_IP_Route"
                    file_name = "show_ip_route"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_ip_route)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_ip_route)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)
                    
                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route.md --output Camelot/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ip_route_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ip_route_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route/%s_show_ip_route_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store IP Route Brief in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_ip_route)

                # Show mac address-table
                if self.parsed_show_mac_address_table is not None:
                    sh_mac_address_table_template = env.get_template('show_mac_address_table.j2')
                    sh_mac_address_netjson_json_template = env.get_template('show_mac_address_table_netjson_json.j2')
                    sh_mac_address_netjson_html_template = env.get_template('show_mac_address_table_netjson_html.j2')

                    directory = "Show_MAC_Address_Table"
                    file_name = "show_mac_address_table"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_mac_address_table)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_mac_address_table)
                    
                    for filetype in filetype_loop:
                        parsed_output_type = sh_mac_address_table_template.render(to_parse_mac_address_table=self.parsed_show_mac_address_table['mac_table'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table.md --output Camelot/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_mac_address_netjson_json_template.render(to_parse_mac_address_table=self.parsed_show_mac_address_table['mac_table'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_mac_address_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_MAC_Address_Table/%s_show_mac_address_table_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store MAC Table in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_mac_address_table)

                # Show port-channel summary
                if self.parsed_show_port_channel_summary is not None:
                    sh_portchannel_summary_template = env.get_template('show_portchannel_summary.j2')
                    sh_portchannel_summary_netjson_json_template = env.get_template('show_portchannel_summary_netjson_json.j2')
                    sh_portchannel_summary_netjson_html_template = env.get_template('show_portchannel_summary_netjson_html.j2')

                    directory = "Show_Port_Channel_Summary"
                    file_name = "show_port_channel_summary"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_port_channel_summary)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_port_channel_summary)

                    for filetype in filetype_loop:                       
                        parsed_output_type = sh_portchannel_summary_template.render(to_parse_etherchannel_summary=self.parsed_show_port_channel_summary['interfaces'],filetype_loop_jinja2=filetype)
                      
                        with open("Camelot/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary.md --output Camelot/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_portchannel_summary_netjson_json_template.render(to_parse_etherchannel_summary=self.parsed_show_port_channel_summary['interfaces'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_portchannel_summary_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Port_Channel_Summary/%s_show_port_channel_summary_netgraph.html" % device.alias, "w") as fh:
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

                    directory = "Show_Version"
                    file_name = "show_version"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_version)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_version)


                    for filetype in filetype_loop:
                        parsed_output_type = sh_ver_template.render(to_parse_version=self.parsed_show_version['platform'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_Version/%s_show_version.md --output Camelot/Cisco/DevNet_Sandbox/Show_Version/%s_show_version_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_ver_netjson_json_template.render(to_parse_version=self.parsed_show_version['platform'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_ver_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Version/%s_show_version_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_Version/%s_show_version_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store Version in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_version)

                # Show vrf
                if self.parsed_show_vrf is not None:
                    sh_vrf_template = env.get_template('show_vrf.j2')
                    sh_vrf_netjson_json_template = env.get_template('show_vrf_netjson_json.j2')
                    sh_vrf_netjson_html_template = env.get_template('show_vrf_netjson_html.j2') 
                    sh_ip_arp_vrf_template = env.get_template('show_ip_arp_vrf.j2')
                    sh_ip_arp_vrf_netjson_json_template = env.get_template('show_ip_arp_vrf_netjson_json.j2')
                    sh_ip_arp_vrf_netjson_html_template = env.get_template('show_ip_arp_vrf_netjson_html.j2')
                    sh_ip_arp_vrf_stats_template = env.get_template('show_ip_arp_vrf_statistics.j2')
                    sh_ip_route_vrf_netjson_json_template = env.get_template('show_ip_route_netjson_json.j2')
                    sh_ip_route_vrf_netjson_html_template = env.get_template('show_ip_route_netjson_html.j2')

                    directory = "Show_VRF"
                    file_name = "show_vrf"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_vrf)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_vrf)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_template.render(to_parse_vrf=self.parsed_show_vrf['vrfs'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.md --output Camelot/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_vrf_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf['vrfs'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vrf)

                # Show vrf all detail
                if self.parsed_show_vrf_all_detail is not None:
                    sh_vrf_all_detail_template = env.get_template('show_vrf_all_detail.j2')
                    sh_vrf_all_detail_netjson_json_template = env.get_template('show_vrf_all_detail_netjson_json.j2')
                    sh_vrf_all_detail_netjson_html_template = env.get_template('show_vrf_all_detail_netjson_html.j2') 

                    # with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.json" % device.alias, "w") as fid:
                    #   json.dump(self.parsed_show_vrf_all_detail, fid, indent=4, sort_keys=True)

                    # with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.yaml" % device.alias, "w") as yml:
                    #   yaml.dump(self.parsed_show_vrf_all_detail, yml, allow_unicode=True)

                    directory = "Show_VRF_All_Detail"
                    file_name = "show_vrf_all_detail"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_vrf_all_detail)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_vrf_all_detail)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_all_detail_template.render(to_parse_vrf=self.parsed_show_vrf_all_detail,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail.md --output Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_vrf_all_detail_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf_all_detail,filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_all_detail_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Detail/%s_show_vrf_all_detail_netgraph.html" % device.alias, "w") as fh:
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

                    directory = "Show_VRF_All_Interface"
                    file_name = "show_vrf_all_interface"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_vrf_all_interface)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_vrf_all_interface)

                    for filetype in filetype_loop:      
                        parsed_output_type = sh_vrf_all_interface_template.render(to_parse_vrf=self.parsed_show_vrf_all_interface,filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface.%s" % (device.alias,filetype), "w") as fh:
                          fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface.md --output Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_vrf_all_interface_netjson_json_template.render(to_parse_vrf=self.parsed_show_vrf_all_interface,filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vrf_all_interface_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF_All_Interface/%s_show_vrf_all_interface_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VRF Interface in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vrf_all_interface)

                # Show vlan
                if self.parsed_show_vlan is not None:
                    sh_vlan_template = env.get_template('show_vlan.j2')
                    sh_vlan_netjson_json_template = env.get_template('show_vlan_netjson_json.j2')
                    sh_vlan_netjson_html_template = env.get_template('show_vlan_netjson_html.j2')  

                    directory = "Show_VLAN"
                    file_name = "show_vlan"
                    self.save_to_json_file(device, directory, file_name, self.parsed_show_vlan)
                    self.save_to_yaml_file(device, directory, file_name, self.parsed_show_vlan)

                    for filetype in filetype_loop:
                        parsed_output_type = sh_vlan_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],filetype_loop_jinja2=filetype)

                        with open("Camelot/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan.%s" % (device.alias,filetype), "w") as fh:
                            fh.write(parsed_output_type)

                    if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan.md" % device.alias):
                        os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan.md --output Camelot/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan_mind_map.html" % (device.alias,device.alias))

                    parsed_output_netjson_json = sh_vlan_netjson_json_template.render(to_parse_vlan=self.parsed_show_vlan['vlans'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                    parsed_output_netjson_html = sh_vlan_netjson_html_template.render(device_alias = device.alias)

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan_netgraph.json" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_json)               

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VLAN/%s_show_vlan_netgraph.html" % device.alias, "w") as fh:
                        fh.write(parsed_output_netjson_html)

                    # ----------------
                    # Store VLAN Interface in Device Table in Databse
                    # ----------------

                    table.insert(self.parsed_show_vlan)

                    # For Each VRF
                    for vrf in self.parsed_show_vrf['vrfs']:

                        # Show IP ARP VRF <VRF> 
                        with steps.start('Parsing ip arp vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_arp_vrf = device.parse("show ip arp vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))

                        with steps.start('Store data',continue_=True) as step:

                            with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                                json.dump(self.parsed_show_ip_arp_vrf, fid, indent=4, sort_keys=True)

                            with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                                yaml.dump(self.parsed_show_ip_arp_vrf, yml, allow_unicode=True)

                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_arp_vrf_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['interfaces'],filetype_loop_jinja2=filetype)

                                with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                    fh.write(parsed_output_type)
        
                            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s.md --output Camelot/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))

                            parsed_output_netjson_json = sh_ip_arp_vrf_netjson_json_template.render(to_parse_ip_arp=self.parsed_show_ip_arp_vrf['interfaces'],filetype_loop_jinja2=filetype,device_alias = device.alias)
                            parsed_output_netjson_html = sh_ip_arp_vrf_netjson_html_template.render(device_alias = device.alias,vrf = vrf)

                            with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)               

                            with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_ARP_VRF/%s_show_ip_arp_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)

                            # ----------------
                            # Store IP ARP VRF Interface in Device Table in Databse
                            # ----------------

                            table.insert(self.parsed_show_ip_arp_vrf)

                        # Show IP ROUTE VRF <VRF>
                        with steps.start('Parsing ip route vrf',continue_=True) as step:
                            try:
                                self.parsed_show_ip_route_vrf = device.parse("show ip route vrf %s" % vrf)
                            except Exception as e:
                                step.failed('Could not parse it correctly\n{e}'.format(e=e))
                        with steps.start('Store data',continue_=True) as step:
                            with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.json" % (device.alias,vrf), "w") as fid:
                              json.dump(self.parsed_show_ip_route_vrf, fid, indent=4, sort_keys=True)
                            with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.yaml" % (device.alias,vrf), "w") as yml:
                              yaml.dump(self.parsed_show_ip_route_vrf, yml, allow_unicode=True)
                        
                            for filetype in filetype_loop:
                                parsed_output_type = sh_ip_route_template.render(to_parse_ip_route=self.parsed_show_ip_route_vrf['vrf'],filetype_loop_jinja2=filetype)
                                with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.%s" % (device.alias,vrf,filetype), "w") as fh:
                                  fh.write(parsed_output_type)
                            if os.path.exists("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md" % (device.alias,vrf)):
                                os.system("markmap --no-open Camelot/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s.md --output Camelot/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_mind_map.html" % (device.alias,vrf,device.alias,vrf))
                            parsed_output_netjson_json = sh_ip_route_vrf_netjson_json_template.render(to_parse_ip_route=self.parsed_show_ip_route['vrf'],filetype_loop_jinja2=filetype,vrf = vrf,device_alias = device.alias)
                            parsed_output_netjson_html = sh_ip_route_vrf_netjson_html_template.render(device_alias = device.alias,vrf = vrf)
                            with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_netgraph.json" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_json)               
                            with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Route_VRF/%s_show_ip_route_vrf_%s_netgraph.html" % (device.alias,vrf), "w") as fh:
                                fh.write(parsed_output_netjson_html)
                        # ----------------
                        # Store IP Route VRF Interface in Device Table in Databse
                        # ----------------
                        table.insert(self.parsed_show_ip_route_vrf)
        
        db.close()
        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED)))
     
    def save_to_json_file(self, device, directory, file_name, content):
        file_path = "Camelot/Cisco/DevNet_Sandbox/{}/{}_{}.json".format(directory, device.alias, file_name)
        with open(file_path, "w") as json_file:
            json.dump(content, json_file, indent=4, sort_keys=True)
            json_file.close()
    
    def save_to_yaml_file(self, device, directory, file_name, content):
        file_path = "Camelot/Cisco/DevNet_Sandbox/{}/{}_{}.yaml".format(directory, device.alias, file_name)
        with open(file_path, "w") as yml_file:
            yaml.dump(content, yml_file, allow_unicode=True)
            yml_file.close()
    
    def save_to_specified_file_type(self, device, directory, file_name, content, file_type):
        file_path = "Camelot/Cisco/DevNet_Sandbox/{}/{}_{}.{}".format(directory, device.alias, file_name, file_type)
        with open(file_path, "w") as opened_file:
            opened_file.write(content)
            opened_file.close()