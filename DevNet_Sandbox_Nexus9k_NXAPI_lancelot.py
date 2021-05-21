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
from genie.utils.diff import Diff
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, LEARN, RUNNING, WRITING, PUSH_INTENT, DIFF, NO_DIFF
from general_functionalities import ParseConfigFunction
from datetime import datetime
from contextlib import redirect_stdout

log = logging.getLogger(__name__)
template_dir = 'templates/cisco/nxos'
env = Environment(loader=FileSystemLoader(template_dir))
timestr = datetime.now().strftime("%Y%m%d_%H%M%S")

# ----------------
# Load Credentials 
# ----------------
with open("testbed/testbed_DevNet_Nexus9k_Sandbox.yaml") as stream:
    testbed = yaml.safe_load(stream)

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup): 
    """Common Setup section"""
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        print(Panel.fit(Text.from_markup(GREETING)))

# ----------------
# Test Case #1
# ----------------
class Collect_Information(aetest.Testcase):
    """Parse all the commands"""

    @aetest.test
    def parse(self, section, steps):
        """ Testcase Setup section """
        for device in testbed['devices']:
            print(Panel.fit(Text.from_markup(RUNNING)))

            # ----------------
            # Load Credentials 
            # ----------------
            for device,value in testbed['devices'].items():
                api_username = testbed["devices"][device]["credentials"]["default"]["username"]
                api_password = testbed["devices"][device]["credentials"]["default"]["password"]
                device_ip = testbed["devices"][device]["connections"]["cli"]["ip"]
                device_alias = testbed["devices"][device]["alias"]
                api_credentials={
                        "aaaUser": {
                            "attributes": {
                                "name": "%s" % api_username,
                                "pwd": "%s" % api_password
                    }}}
                headers = {'Content-Type':'application/json'}
                nxapi_token_raw = requests.post("https://%s/api/aaaLogin.json" % device_ip, headers=headers, data=json.dumps(api_credentials), verify=False,)
                nxapi_data = json.loads(nxapi_token_raw.text)['imdata'][0]
                nxapi_token = str(nxapi_data['aaaLogin']['attributes']['token'])
                auth_cookie = {"APIC-cookie": nxapi_token}

            # ---------------------------------------
            # Load Data Model
            # ---------------------------------------           
            with open("data_models/%s.yaml" % device_alias) as stream:
                data_model = yaml.safe_load(stream)

            # ---------------------------------------
            # NX-API Learn Full Pre-change state 
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN)))

            self.learned_config = requests.get("https://%s/api/mo/sys.json?rsp-subtree=full&rsp-prop-include=set-config-only" % device_ip, headers=headers, cookies=auth_cookie, verify=False)
            self.original_learned_config = self.learned_config.json()

            #----------------------------------------
            # Write Pre-Change File
            #----------------------------------------
            with steps.start('Store Original Golden Image',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                
                original_config_filename = "%s_Original_Golden_NXAPI_Image_%s.json" % (timestr,device_alias)
                # Write Original Learned Config as JSON
                if hasattr(self, 'learned_config'):
                    with open("Camelot/Cisco/DevNet_Sandbox/Lancelot/Golden_Image/%s" % original_config_filename, "w") as fid:
                        json.dump(self.original_learned_config, fid, indent=4, sort_keys=True)
                        fid.close()

            # ---------------------------------------
            # Create Intent from Template and Data Models
            # ---------------------------------------
            with steps.start('Generating Intent From Data Model and Template',continue_=True) as step:
                print(Panel.fit(Text.from_markup(RUNNING)))
                intended_config_template = env.get_template('intended_nxapi_config.j2')
                rendered_intended_config = intended_config_template.render(host_data_model=data_model)
                with open("Camelot/Cisco/DevNet_Sandbox/Lancelot/Intended_Config/%s_Intended_NXAPI_Config.json" % timestr, "w") as fid:
                    fid.write(rendered_intended_config)
                    fid.close()

            # ---------------------------------------
            # Push Intent - VLANS
            # ---------------------------------------         
            with steps.start('Push Intent',continue_=True) as step:
                print(Panel.fit(Text.from_markup(PUSH_INTENT)))
                push_intent = requests.put("https://%s/api/mo/sys/bd.json" % device_ip, headers=headers, data=rendered_intended_config, cookies=auth_cookie, verify=False)
                print(push_intent)
           
            # ---------------------------------------
            # NX-API Re-Learn Full Pre-change state 
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN)))

            self.learned_config = requests.get("https://%s/api/mo/sys.json?rsp-subtree=full&rsp-prop-include=set-config-only" % device_ip, headers=headers, cookies=auth_cookie, verify=False)
            self.new_learned_config = self.learned_config.json()

            # ---------------------------------------
            # Write post-change state
            # ---------------------------------------
            with steps.start('Store New Golden Image',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                
                new_config_filename = "%s_Golden_NXAPI_Image_%s.json" % (timestr,device_alias)

                # Write New Learned Config as JSON
                with open("Camelot/Cisco/DevNet_Sandbox/Lancelot/Golden_Image/%s" % new_config_filename, "w") as fid:
                    json.dump(self.new_learned_config, fid, indent=4, sort_keys=True)
                    fid.close()            

            # ---------------------------------------
            # Show the differential 
            # ---------------------------------------
            with steps.start('Show Differential',continue_=True) as step:
                config_diff = Diff(self.original_learned_config, self.new_learned_config)
                config_diff.findDiff()
                
                if config_diff.diffs:
                    print(Panel.fit(Text.from_markup(DIFF)))
                    print(config_diff)
                
                    with open('Camelot/Cisco/DevNet_Sandbox/Lancelot/Changes/%s_NXAPI_Changes.txt' % timestr, 'w') as f:
                        with redirect_stdout(f):
                            print(config_diff)
                            f.close()
    
                else:
                    print(Panel.fit(Text.from_markup(NO_DIFF)))
                    
                    with open('Camelot/Cisco/DevNet_Sandbox/Lancelot/Changes/%s_NXAPI_Changes.txt' % timestr, 'w') as f:
                        f.write("IDEMPOTENT - NO CHANGES")
                        f.close()