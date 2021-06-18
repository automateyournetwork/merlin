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
from requests_toolbelt.multipart.encoder import MultipartEncoder
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, LEARN, RUNNING, WRITING, FINISHED
from general_functionalities import ParseShowCommandFunction, ParseLearnFunction, ParseConfigFunction, ParseDictFunction

# ----------------
# Get logger for script
# ----------------

log = logging.getLogger(__name__)

# ----------------
# Template Directory
# ----------------

template_dir = 'templates/cisco/nxos'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# WebEx Setup
# ----------------
webex_roomid = "Y2lzY29zcGFyazovL3VzL1JPT00vOTI1YTdhMzAtY2QyMS0xMWViLWJkY2QtOTVkNWY1NmNmNzNh"
webex_token = "Mjk3YTNiNDQtZjU5Zi00MzE2LWExODQtMGQ0Y2MyMjVkM2UzYzQyNjRlZmItNThi_PF84_consumer"

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

            # ---------------------------------------
            # Genie learn().info for various functions
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN)))

            # Platform
            self.learned_platform = ParseDictFunction.parse_learn(steps, device, "platform")             

            # Routing
            self.learned_routing = ParseLearnFunction.parse_learn(steps, device, "routing")         

            # Show IP Interface Brief
            self.parsed_show_ip_int_brief = ParseShowCommandFunction.parse_show_command(steps, device, "show ip interface brief")

            # Show VRF
            self.parsed_show_vrf = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf")

            with steps.start('Create XLSX',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
  
                # -----------------------
                # Learned Platform
                # -----------------------
                if self.learned_platform is not None:
                    learned_platform_template = env.get_template('learned_platform.j2')
                    learned_platform_webex_adaptive_card_template = env.get_template('learned_platform_webex_adaptive_card.j2')
                    directory = "Learned_Platform"
                    file_name = "learned_platform"
                    parsed_output_xlsx = learned_platform_template.render(to_parse_platform=self.learned_platform,filetype_loop_jinja2="xlsx")

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Platform/%s_learned_platform.xlsx" % device.alias, "w") as fh:
                        fh.write(parsed_output_xlsx) 

                    m = MultipartEncoder({'roomId': webex_roomid,
                      'text': 'Learn Platform XLSX File',
                      'files': ("Camelot/Cisco/DevNet_Sandbox/Learned_Platform/%s_learned_platform.xlsx" % device.alias, open("Camelot/Cisco/DevNet_Sandbox/Learned_Platform/DevNet_Sandbox_Nexus9k_learned_platform.xlsx", "rb"),
                      'text/xlsx' )})
                      
                    # -----------------------
                    # Send to WebEx
                    # -----------------------
                    with steps.start('Send Adaptive Card',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))
                        # Adaptive Card
                        webex_adaptive_card = learned_platform_webex_adaptive_card_template.render(to_parse_platform=self.learned_platform,roomid = webex_roomid,device_id = device.alias)
                        print(webex_adaptive_card)
                        webex_adaptive_card_response = requests.post('https://webexapis.com/v1/messages', data=webex_adaptive_card, headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % webex_token })
                        print('The POST to WebEx had a response code of ' + str(webex_adaptive_card_response.status_code) + 'due to' + webex_adaptive_card_response.reason)

                    with steps.start('Send File',continue_=True) as step:
                        print(Panel.fit(Text.from_markup(WRITING)))
                        # File (XLSX)
                        webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m, headers={"Content-Type": m.content_type, "Authorization": "Bearer %s" % webex_token })
                        print('The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)

                # -----------------------
                # Learned Routing
                # -----------------------
                if self.learned_routing is not None:
                    learned_routing_template = env.get_template('learned_routing.j2')
                    learned_routing_webex_adaptive_card_template = env.get_template('learned_routing_webex_adaptive_card.j2')
                    directory = "Learned_Routing"
                    file_name = "learned_routing"         

                    parsed_output_xlsx = learned_routing_template.render(to_parse_routing=self.learned_routing,filetype_loop_jinja2="xlsx")

                    with open("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/%s_show_vrf.xlsx" % device.alias, "w") as fh:
                        fh.write(parsed_output_xlsx) 

                    m = MultipartEncoder({'roomId': webex_roomid,
                      'text': 'Learn Routing XLSX File',
                      'files': ("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/%s_show_vrf.xlsx" % device.alias, open("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/DevNet_Sandbox_Nexus9k_learned_routing.xlsx", "rb"),
                      'text/xlsx' )})

                    # -----------------------
                    # Send to WebEx
                    # -----------------------
                   
                    with steps.start('Send Adaptive Card',continue_=True) as step:
                        for learned_route,learned_value in self.learned_routing.items():
                            for learned_value,vrf_value in learned_value.items():                                  
                                for vrf_value,family_value in vrf_value.items():
                                    for family_value,route_value in family_value.items():
                                        for route_value,route in route_value.items():
                                            for route,route_detail in route.items():
                                                if route_detail['route'] == "0.0.0.0/0":                    
                                                    # Adaptive Card
                                                    print(Panel.fit(Text.from_markup(WRITING)))
                            
                                                    webex_adaptive_card = learned_routing_webex_adaptive_card_template.render(roomid = webex_roomid,device_id = device.alias,vrf=learned_value,address_family=family_value,route=route_detail)
                                                    print(webex_adaptive_card)
                                                    webex_adaptive_card_response = requests.post('https://webexapis.com/v1/messages', data=webex_adaptive_card, headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % webex_token })
                            
                                                    print('The POST to WebEx had a response code of ' + str(webex_adaptive_card_response.status_code) + 'due to' + webex_adaptive_card_response.reason)

                    with steps.start('Send File',continue_=True) as step:
                       print(Panel.fit(Text.from_markup(WRITING)))
                       # File (XLSX)
                       webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m, headers={"Content-Type": m.content_type, "Authorization": "Bearer %s" % webex_token })
                       print('The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)

                # -----------------------
                # Show IP Interface Brief
                # -----------------------
                if self.parsed_show_ip_int_brief is not None:
                    sh_ip_int_brief_template = env.get_template('show_ip_interface_brief.j2')
                    sh_ip_int_brief_webex_adaptive_card_template = env.get_template('show_ip_interface_brief_webex_adaptive_card.j2')                   
                    directory = "Show_IP_Interface_Brief"
                    file_name = "show_ip_interface_brief"         

                    parsed_output_xlsx = sh_ip_int_brief_template.render(to_parse_interfaces=self.parsed_show_ip_int_brief['interface'],filetype_loop_jinja2="xlsx")

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_interface_brief.xlsx" % device.alias, "w") as fh:
                        fh.write(parsed_output_xlsx) 

                    m = MultipartEncoder({'roomId': webex_roomid,
                      'text': 'Show IP Interface Brief XLSX File',
                      'files': ("Camelot/Cisco/DevNet_Sandbox/Show_IP_Interface_Brief/%s_show_ip_interface_brief.xlsx" % device.alias, open("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/DevNet_Sandbox_Nexus9k_learned_routing.xlsx", "rb"),
                      'text/xlsx' )})

                    # -----------------------
                    # Send to WebEx
                    # -----------------------
                   
                    with steps.start('Send Adaptive Card',continue_=True) as step:
                        
                        # Adaptive Card
                        print(Panel.fit(Text.from_markup(WRITING)))
                            
                        webex_adaptive_card = sh_ip_int_brief_webex_adaptive_card_template.render(roomid = webex_roomid,device_id = device.alias,to_parse_interfaces=self.parsed_show_ip_int_brief['interface'])
                        print(webex_adaptive_card)
                        webex_adaptive_card_response = requests.post('https://webexapis.com/v1/messages', data=webex_adaptive_card, headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % webex_token })
                            
                        print('The POST to WebEx had a response code of ' + str(webex_adaptive_card_response.status_code) + 'due to' + webex_adaptive_card_response.reason)

                    with steps.start('Send File',continue_=True) as step:
                       print(Panel.fit(Text.from_markup(WRITING)))
                       # File (XLSX)
                       webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m, headers={"Content-Type": m.content_type, "Authorization": "Bearer %s" % webex_token })
                       print('The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)

                # -----------------------
                # Show VRF
                # -----------------------
                if self.parsed_show_vrf is not None:
                    sh_vrf_template = env.get_template('show_vrf.j2')
                    sh_vrf_webex_adaptive_card_template = env.get_template('show_vrf_webex_adaptive_card.j2')                   
                    directory = "Learned_Routing"
                    file_name = "learned_routing"         

                    parsed_output_xlsx = sh_vrf_template.render(to_parse_vrf=self.parsed_show_vrf['vrfs'],filetype_loop_jinja2="xlsx")

                    with open("Camelot/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.xlsx" % device.alias, "w") as fh:
                        fh.write(parsed_output_xlsx) 

                    m = MultipartEncoder({'roomId': webex_roomid,
                      'text': 'Show VRF XLSX File',
                      'files': ("Camelot/Cisco/DevNet_Sandbox/Show_VRF/%s_show_vrf.xlsx" % device.alias, open("Camelot/Cisco/DevNet_Sandbox/Learned_Routing/DevNet_Sandbox_Nexus9k_learned_routing.xlsx", "rb"),
                      'text/xlsx' )})

                    # -----------------------
                    # Send to WebEx
                    # -----------------------
                   
                    with steps.start('Send Adaptive Card',continue_=True) as step:
                        
                        # Adaptive Card
                        print(Panel.fit(Text.from_markup(WRITING)))
                            
                        webex_adaptive_card = sh_vrf_webex_adaptive_card_template.render(roomid = webex_roomid,device_id = device.alias,to_parse_vrf=self.parsed_show_vrf['vrfs'])
                        print(webex_adaptive_card)
                        webex_adaptive_card_response = requests.post('https://webexapis.com/v1/messages', data=webex_adaptive_card, headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % webex_token })
                            
                        print('The POST to WebEx had a response code of ' + str(webex_adaptive_card_response.status_code) + 'due to' + webex_adaptive_card_response.reason)

                    with steps.start('Send File',continue_=True) as step:
                       print(Panel.fit(Text.from_markup(WRITING)))
                       # File (XLSX)
                       webex_file_response = requests.post('https://webexapis.com/v1/messages', data=m, headers={"Content-Type": m.content_type, "Authorization": "Bearer %s" % webex_token })
                       print('The POST to WebEx had a response code of ' + str(webex_file_response.status_code) + 'due to' + webex_file_response.reason)
    
        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED)))

    def save_to_specified_file_type(self, device, directory, file_name, content, file_type):
        file_path = "Camelot/Cisco/DevNet_Sandbox/{}/{}_{}.{}".format(directory, device.alias, file_name, file_type)
        with open(file_path, "w") as opened_file:
            opened_file.write(content)
            opened_file.close()           