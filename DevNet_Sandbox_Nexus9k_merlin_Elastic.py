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
import datetime
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
from elasticsearch import Elasticsearch
from elastic_enterprise_search import AppSearch

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
# Define Elastic
# ----------------
es = Elasticsearch(cloud_id="Merlin:dXMtd2VzdDEuZ2NwLmNsb3VkLmVzLmlvJDgzMmZiYjliOTExOTRiNWFiNjA0OTNiZmUyN2U3ZjRjJDZlMjM4ZDY0N2FhNjQwN2Y4OTYxYjg2NjU4MTc3OWM5", http_auth=('elastic', 'OqwelTPX21v3PguwPApy0LPu'))

#
# Timestamp
#

timestamp_json = '{ "Timestamp": %s }' % json.dumps(datetime.datetime.now().replace(microsecond=0).isoformat())

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
            device_alias_json = '{ "Device Alias": %s }' % device.alias

            # ----------------
            # Timestamp Elastic
            # ----------------

            es.index(index='%s_timestamp' % device.alias.lower() , ignore=400, 
                    id=id, body=timestamp_json)

            # ----------------
            # Add Device Alias Elastic
            # ----------------

            es.index(index='%s_device_alias' % device.alias.lower() , ignore=400, 
                    id=id, body=device_alias_json)

            # ---------------------------------------
            # Genie learn().info for various functions
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(LEARN)))

            # Interface
            self.learned_interface = ParseLearnFunction.parse_learn(steps, device, "interface")          

            # ---------------------------------------
            # Execute parser for various show commands
            # ---------------------------------------
            print(Panel.fit(Text.from_markup(RUNNING)))

            # ---------------------------------------
            # Post to ElasticSearch
            # ---------------------------------------         
            with steps.start('Post To ElasticSearch',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                
                ###############################
                # Genie learn().info section
                ###############################

                # Learned Interface
                if self.learned_interface is not None:
                    learned_interface_elastic_template = env.get_template('learned_interface_elastic.j2')
                    learned_interface_elastic = learned_interface_elastic_template.render(to_parse_interface=self.learned_interface)
                    print(learned_interface_elastic)
                    # ----------------
                    # Store Interface in Elastic
                    # ----------------

                    es.index(index='%s_learned_interface' % device.alias.lower() , ignore=400, 
                             id=id, body=learned_interface_elastic)

        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED)))