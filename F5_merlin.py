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
from pyats.log.utils import banner
from jinja2 import Environment, FileSystemLoader
from ascii_art import GREETING, LEARN, RUNNING, WRITING, FINISHED

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

template_dir = 'templates/f5'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Load Credentials 
# ----------------

with open("testbed/testbed_f5.yaml") as stream:
    testbed = yaml.safe_load(stream)

# ---------------------------------------
# API Get Token
# ---------------------------------------

for device,value in testbed['devices'].items():
    api_username = testbed["devices"][device]["credentials"]["default"]["username"]
    api_password = testbed["devices"][device]["credentials"]["default"]["password"]
    device_alias = testbed["devices"][device]["alias"]
    f5_token_raw = requests.post("https://%s/mgmt/shared/authn/login" % device, json={"username":"%s" % api_username, "password": "%s" % api_password,"loginprovidername": "tmos"}, verify=False)
    f5_token_json = f5_token_raw.json()
    f5_usable_token = f5_token_json["token"]["token"]

headers={"X-F5-Auth-Token":f5_usable_token}

# ----------------
# AE Test Setup
# ----------------
class common_setup(aetest.CommonSetup):
    """Common Setup section"""
    @aetest.subsection
    def connect_to_devices(self):
        """Connect to all the devices"""
        print(Panel.fit(Text.from_markup(GREETING)))

# ----------------
# Test Case #1 - Go to F5 API
# ----------------
class Collect_Information(aetest.Testcase):
    """Parse all the commands"""

    @aetest.test
    def parse(self, section, steps):
        """ Testcase Setup section """
        for device in testbed['devices']:
            print(Panel.fit(Text.from_markup(RUNNING)))

            # VS
            with steps.start('Requesting VS API Information',continue_=True) as step:
                try:
                    self.raw_vs = requests.get("https://%s/mgmt/tm/ltm/virtual" % device_alias, headers=headers, verify=False)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))

            with steps.start('Requesting SSL API Information',continue_=True) as step:
                try:
                    self.raw_ssl_cert = requests.get("https://%s/mgmt/tm/sys/file/ssl-cert" % device_alias, headers=headers, verify=False)
                    print(Panel.fit(Text.from_markup(CLOUD)))
                except Exception as e:
                    step.failed('There was a problem with the API\n{e}'.format(e=e))

            # ---------------------------------------
            # Generate CSV / MD / HTML / Mind Maps
            # ---------------------------------------

            with steps.start('Store data',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                
                # VS
                if hasattr(self, 'raw_vs'):
                    self.vs_json = self.raw_vs.json()
                    vs_template = env.get_template('virtual_servers.j2')

                    with open("Camelot/F5/Virtual_Servers/%s_virtual_servers.json" % device_alias, "w") as fid:
                        json.dump(self.vs_json, fid, indent=4, sort_keys=True)

                    with open("Camelot/F5/Virtual_Servers/%s_virtual_servers.yaml" % device_alias, "w") as yml:
                        yaml.dump(self.vs_json, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_vs = vs_template.render(to_parse_vs=self.vs_json['items'],filetype_loop_jinja2=filetype)

                        with open("Camelot/F5/Virtual_Servers/%s_virtual_servers.%s" % (device_alias,filetype), "w") as fh:
                            fh.write(parsed_output_vs) 
                    
                        os.system("markmap Camelot/F5/Virtual_Servers/%s_virtual_servers.md --output Camelot/F5/Virtual_Servers/%s_virtual_servers_mind_map.html" % (device_alias,device_alias))

                # SSL Certificates
                if hasattr(self, 'raw_ssl_cert'):
                    self.ssl_cert_json = self.raw_ssl_cert.json()
                    ssl_cert_template = env.get_template('ssl_certificates.j2')

                    with open("Camelot/F5/SSL_Certificates/%s_ssl_certificates.json" % device_alias, "w") as fid:
                        json.dump(self.ssl_cert_json, fid, indent=4, sort_keys=True)

                    with open("Camelot/F5/SSL_Certificates/%s_ssl_certificates.yaml" % device_alias, "w") as yml:
                        yaml.dump(self.ssl_cert_json, yml, allow_unicode=True)

                    for filetype in filetype_loop:
                        parsed_output_ssl_cert = ssl_cert_template.render(to_parse_ssl_cert=self.ssl_cert_json['items'],filetype_loop_jinja2=filetype)

                        with open("Camelot/F5/SSL_Certificates/%s_ssl_certificates.%s" % (device_alias,filetype), "w") as fh:
                            fh.write(parsed_output_ssl_cert) 
                    
                        os.system("markmap Camelot/F5/SSL_Certificates/%s_ssl_certificates.md --output Camelot/F5/SSL_Certificates/%s_ssl_certificates_mind_map.html" % (device_alias,device_alias))

        # ---------------------------------------
        # You Made It 
        # ---------------------------------------
        print(Panel.fit(Text.from_markup(FINISHED)))    