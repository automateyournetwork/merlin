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
import ftplib
import re
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from pyats import topology
from pyats.log.utils import banner
from genie.utils.diff import Diff
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, LEARN, RUNNING, WRITING, PUSH_INTENT, DIFF, NO_DIFF
from general_functionalities import ParseConfigFunction, ParseLearnFunction
from datetime import datetime
from contextlib import redirect_stdout

log = logging.getLogger(__name__)
template_dir = 'templates/cisco/ios_xe'
env = Environment(loader=FileSystemLoader(template_dir))
timestr = datetime.now().strftime("%Y%m%d_%H%M%S")

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
            # Load Data Model
            # ---------------------------------------           
            with open("data_models/%s.yaml" % device.alias) as stream:
                data_model = yaml.safe_load(stream)
            # ---------------------------------------
            # Genie learn('config').info for pre-change state 
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN)))

            self.learned_config = ParseConfigFunction.parse_learn(steps, device, "config")
            original_learned_config = self.learned_config

            # Routing
            self.learned_routing = ParseLearnFunction.parse_learn(steps, device, "routing")
            pre_change_default_route = self.learned_routing['vrf']['default']['address_family']['ipv4']['routes']['0.0.0.0/0']['next_hop']['next_hop_list'][1]['next_hop']
            print (pre_change_default_route)

            #----------------------------------------
            # Confirm All Interfaces Are Up First
            #----------------------------------------
            with steps.start('Pre-Change Interface Check',continue_=True) as step:
                all_interfaces_up = "true"
                interface_list = ("GigabitEthernet1","GigabitEthernet2","GigabitEthernet3")
                for interface in interface_list:
                    if "shutdown" in original_learned_config['interface %s' % interface]:
                        all_interfaces_up = "false"
                        log.info("Interface is shutdown")
                    else:
                        log.info("Interface is up")

            if all_interfaces_up == "true":
                log.info("The Device is Healthy: Proceeding with Deployment")
                #----------------------------------------
                # Write Pre-Change File
                #----------------------------------------
            
                with steps.start('Store Original Golden Image',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))
                
                    original_config_filename = "%s_Original_Golden_SSH_Image_%s.json" % (timestr,device.alias)
                    # Write Original Learned Config as JSON
                    if hasattr(self, 'learned_config'):
                        with open("Camelot/Cisco/DevNet_Sandbox/Lancelot/Golden_Image/%s" % original_config_filename, "w") as fid:
                            json.dump(self.learned_config, fid, indent=4, sort_keys=True)
                            fid.close()

                # ---------------------------------------
                # Create Intent from Template and Data Models
                # ---------------------------------------
                with steps.start('Generating Intent From Data Model and Template',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(RUNNING)))
                    intended_config_template = env.get_template('intended_ssh_config.j2')
                    rendered_intended_config = intended_config_template.render(host_data_model=data_model)

                    with open("Camelot/Cisco/DevNet_Sandbox/Lancelot/Intended_Config/%s_Intended_SSH_Config.txt" % timestr, "w") as fid:
                        fid.write(rendered_intended_config)
                        fid.close()
                
                # ---------------------------------------
                # Push Intent to FTP Server
                # ---------------------------------------         
                with steps.start('Push Intent to FTP Server',continue_=True) as step:
                    ftp = ftplib.FTP()
                    host = "10.10.20.50"
                    port = 2121
                    ftp.connect(host, port)
                    print (ftp.getwelcome())
                    try:
                        print ("Logging in...")
                        ftp.login()
                    except:
                        "failed to login"
                    print ("Storing file")
                    file = open("Camelot/Cisco/DevNet_Sandbox/Lancelot/Intended_Config/%s_Intended_SSH_Config.txt" % timestr, "rb")
                    ftp.storbinary("STOR Intended_Config", file)
                    file.close()
                    ftp.close()

                # ---------------------------------------
                # Copy file from FTP server to Bootflash
                # ---------------------------------------         
                device.api.copy_to_device(
                        protocol="ftp",
                        server="10.10.20.50:2121",
                        remote_path="Intended_Config",
                        local_path="bootflash:/")

                # ---------------------------------------
                # Trigger Config Replace
                # --------------------------------------- 
                device.execute("configure replace bootflash:/Intended_Config force")

                # ---------------------------------------
                # Re-capture state
                # ---------------------------------------
                print(Panel.fit(Text.from_markup(LEARN)))

                self.learned_config = ParseConfigFunction.parse_learn(steps, device, "config")
                new_learned_config = self.learned_config

                # Routing
                self.learned_routing = ParseLearnFunction.parse_learn(steps, device, "routing")
                post_change_default_route = self.learned_routing['vrf']['default']['address_family']['ipv4']['routes']['0.0.0.0/0']['next_hop']['next_hop_list'][1]['next_hop']
                print (pre_change_default_route)

                ## ---------------------------------------
                ## Write post-change state
                ## ---------------------------------------
                with steps.start('Store New Golden Image',continue_=True) as step:
                    print(Panel.fit(Text.from_markup(WRITING)))
                
                    new_config_filename = "%s_Golden_SSH_Image_%s.json" % (timestr,device.alias)

                    ## Write New Learned Config as JSON
                    if hasattr(self, 'learned_config'):
                        with open("Camelot/Cisco/DevNet_Sandbox/Lancelot/Golden_Image/%s" % new_config_filename, "w") as fid:
                            json.dump(self.learned_config, fid, indent=4, sort_keys=True)
                            fid.close()

                ## ---------------------------------------
                ## Show the differential 
                ## ---------------------------------------
                with steps.start('Show Differential',continue_=True) as step:
                    config_diff = Diff(original_learned_config, new_learned_config)
                    config_diff.findDiff()
                
                    if config_diff.diffs:
                        print(Panel.fit(Text.from_markup(DIFF)))
                        print(config_diff)
                
                        with open('Camelot/Cisco/DevNet_Sandbox/Lancelot/Changes/%s_SSH_Changes.txt' % timestr, 'w') as f:
                            with redirect_stdout(f):
                                print(config_diff)
                                f.close()
    
                    else:
                        print(Panel.fit(Text.from_markup(NO_DIFF)))
                    
                        with open('Camelot/Cisco/DevNet_Sandbox/Lancelot/Changes/%s_SSH_Changes.txt' % timestr, 'w') as f:
                            f.write("IDEMPOTENT - NO CHANGES")
                            f.close()

                ## ---------------------------------------
                ## Ping Test
                ## ---------------------------------------
                with steps.start('PING Test',continue_=True) as step:
                    destination_list = ("10.10.20.254","10.10.100.100")
                    failed = "false"
                    for destination in destination_list:           
                        try:
                            result = device.ping(destination)
                            log.info(result)

                        except Exception as e:
                            log.info("We could NOT ping the loopback so we rolling back to startup-config")
                            device.execute("configure replace nvram:startup-config force")                                    
                            self.failed('Ping {} from device {} failed with error: {}'.format(
                                                destination,
                                                device,
                                                str(e),
                                            )
                                        )
                        else:
                            match = re.search(r'Success rate is (?P<rate>\d+) percent', result)
                            success_rate = match.group('rate')

                            log.info('Ping {} with success rate of {}%'.format(
                                                        destination,
                                                        success_rate,
                                                    )
                                                )
                            if success_rate != "100":
                                failed = "true"

                    #----------------------------------------
                    # Confirm All Interfaces Are Up First
                    #----------------------------------------
                    with steps.start('POST-Change Interface Check',continue_=True) as step:
                        all_interfaces_up = "true"
                        interface_list = ("GigabitEthernet1","GigabitEthernet2","GigabitEthernet3","Loopback100")
                        for interface in interface_list:
                            if "shutdown" in new_learned_config['interface %s' % interface]:
                                all_interfaces_up = "false"
                                log.info("Interface is shutdown")
                            else:
                                log.info("Interface is up")

                    #----------------------------------------
                    # Confirm the default route is unchanged
                    #----------------------------------------
                    with steps.start('POST-Change Default Route Test',continue_=True) as step:
                        bad_default_route = "false"
                        if pre_change_default_route != post_change_default_route:
                            bad_default_route = "true"
                            log.info("Bad Default Route")
                        else:
                            log.info("Unchanged Default Route")

                    ## ---------------------------------------
                    ## Commit or Rollback
                    ## ---------------------------------------
                    with steps.start('Commit or Rollback',continue_=True) as step:
                        if failed == "true" or all_interfaces_up == "false" or bad_default_route == "true":
                            log.info("We could NOT ping or Interfaces are DOWN so we rolling back to startup-config")
                            device.execute("configure replace nvram:startup-config force")
                        else:
                            log.info("We could ping,all Interfaces are UP, and default route is unchanged so we are saving the configuration")
                            device.execute("write mem")
            else:
                log.info("Sorry all of the Interfaces were NOT UP so we cancelled the deployment")
