# ----------------
# Copyright
# ----------------
# Written by John Capobianco, March 2021
# Copyright (c) 2021 John Capobianco

# ----------------
# Python
# ----------------
import datetime
import logging
import uuid
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
es = Elasticsearch(cloud_id="{{ YOUR CLOUD ID HERE }}", http_auth=('elastic', '{{ YOUR PASSWORD HERE }}'))

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
            unique_id = uuid.uuid4().hex

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

            # show bgp process vrf all
            self.parsed_show_bgp_process_vrf_all = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp process vrf all")

            # Show BGP Sessions
            self.parsed_show_bgp_sessions = ParseShowCommandFunction.parse_show_command(steps, device, "show bgp sessions")

            # Show Interface Status
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

            # Show Port Channel Summary
            self.parsed_show_port_channel_summary = ParseShowCommandFunction.parse_show_command(steps, device, "show port-channel summary")

            # Show Version
            self.parsed_show_version = ParseShowCommandFunction.parse_show_command(steps, device, "show version")

            # Show VLAN
            self.parsed_show_vlan = ParseShowCommandFunction.parse_show_command(steps, device, "show vlan")

            # Show VRF
            self.parsed_show_vrf = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf")

            # show VRF all detail
            self.parsed_show_vrf_all_detail = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf all detail")

            # show VRF all interface
            self.parsed_show_vrf_all_interface = ParseShowCommandFunction.parse_show_command(steps, device, "show vrf all interface")

            # ---------------------------------------
            # Post to ElasticSearch
            # ---------------------------------------         
            with steps.start('Post To ElasticSearch',continue_=True) as step:
                print(Panel.fit(Text.from_markup(WRITING)))
                
                ###############################
                # Genie learn().info section
                ###############################

                # Learned ACLs
                if self.learned_acl is not None:
                    learned_acl_elastic_template = env.get_template('elastic_standards.j2')
                    learned_acl_elastic = learned_acl_elastic_template.render(to_normalize_for_elastic=self.learned_acl)

                #    # ----------------
                #    # Store acl in Elastic
                #    # ----------------
                    es.index(index='%s_learned_acl' % device.alias.lower(), id=unique_id, 
                             body=learned_acl_elastic)

                # Learned ARP
                if self.learned_arp is not None:
                    learned_arp_elastic_template = env.get_template('elastic_standards.j2')
                    learned_arp_elastic = learned_arp_elastic_template.render(to_normalize_for_elastic=self.learned_arp)

                    # ----------------
                    # Store arp in Elastic
                    # ----------------
                    es.index(index='%s_learned_arp' % device.alias.lower(), id=unique_id, 
                             body=learned_arp_elastic)

                # Learned BGP
                if self.learned_bgp is not None:
                    learned_bgp_elastic_template = env.get_template('elastic_standards.j2')
                    learned_bgp_elastic = learned_bgp_elastic_template.render(to_normalize_for_elastic=self.learned_bgp)

                    # ----------------
                    # Store bgp in Elastic
                    # ----------------
                    es.index(index='%s_learned_bgp' % device.alias.lower(), id=unique_id, 
                             body=learned_bgp_elastic)

                # Learned Interface
                if self.learned_interface is not None:
                    learned_interface_elastic_template = env.get_template('elastic_standards.j2')
                    learned_interface_elastic = learned_interface_elastic_template.render(to_normalize_for_elastic=self.learned_interface)

                    # ----------------
                    # Store Interface in Elastic
                    # ----------------
                    es.index(index='%s_learned_interface' % device.alias.lower(), id=unique_id, 
                             body=learned_interface_elastic)

                # Learned OSPF
                if self.learned_ospf is not None:
                    learned_ospf_elastic_template = env.get_template('elastic_standards.j2')
                    learned_ospf_elastic = learned_ospf_elastic_template.render(to_normalize_for_elastic=self.learned_ospf)
                    # ----------------
                    # Store ospf in Elastic
                    # ----------------
                    es.index(index='%s_learned_ospf' % device.alias.lower(), id=unique_id, 
                             body=learned_ospf_elastic)

                # Learned Platform
                if self.learned_platform is not None:
                    learned_platform_elastic_template = env.get_template('elastic_standards.j2')
                    learned_platform_elastic = learned_platform_elastic_template.render(to_normalize_for_elastic=self.learned_platform)
                    # ----------------
                    # Store platform in Elastic
                    # ----------------
                    es.index(index='%s_learned_platform' % device.alias.lower(), id=unique_id, 
                             body=learned_platform_elastic)                

                # Learned Routing
                if self.learned_routing is not None:
                    learned_routing_elastic_template = env.get_template('elastic_standards.j2')
                    learned_routing_elastic = learned_routing_elastic_template.render(to_normalize_for_elastic=self.learned_routing)
                    # ----------------
                    # Store routing in Elastic
                    # ----------------
                    es.index(index='%s_learned_routing' % device.alias.lower(), id=unique_id, 
                             body=learned_routing_elastic) 

                # Learned VLAN
                if self.learned_vlan is not None:
                    learned_vlan_elastic_template = env.get_template('elastic_standards.j2')
                    learned_vlan_elastic = learned_vlan_elastic_template.render(to_normalize_for_elastic=self.learned_vlan)
                    # ----------------
                    # Store vlan in Elastic
                    # ----------------
                    es.index(index='%s_learned_vlan' % device.alias.lower(), id=unique_id, 
                             body=learned_vlan_elastic)

                # Learned VRF
                if self.learned_vrf is not None:
                    learned_vrf_elastic_template = env.get_template('elastic_standards.j2')
                    learned_vrf_elastic = learned_vrf_elastic_template.render(to_normalize_for_elastic=self.learned_vrf)
                    # ----------------
                    # Store vrf in Elastic
                    # ----------------
                    es.index(index='%s_learned_vrf' % device.alias.lower(), id=unique_id, 
                             body=learned_vrf_elastic)

                ###############################
                # Genie Show Command Section
                ###############################
                
                # Show BGP Process VRF all
                if self.parsed_show_bgp_process_vrf_all is not None:
                    show_bgp_process_vrf_all_elastic_template = env.get_template('elastic_standards.j2')
                    show_bgp_process_vrf_all_elastic = show_bgp_process_vrf_all_elastic_template.render(to_normalize_for_elastic=self.parsed_show_bgp_process_vrf_all)
                    # ----------------
                    # Store BGP Process VRF all in Elastic
                    # ----------------
                    es.index(index='%s_show_bgp_process_vrf_all' % device.alias.lower(), id=unique_id, 
                             body=show_bgp_process_vrf_all_elastic)

                # Show BGP Sessions
                if self.parsed_show_bgp_sessions is not None:
                    show_bgp_sessions_elastic_template = env.get_template('elastic_standards.j2')
                    show_bgp_sessions_elastic = show_bgp_sessions_elastic_template.render(to_normalize_for_elastic=self.parsed_show_bgp_sessions)
                    # ----------------
                    # Store BGP in Elastic
                    # ----------------
                    es.index(index='%s_show_bgp_sessions' % device.alias.lower(), id=unique_id, 
                             body=show_bgp_sessions_elastic)

                # Show Interface Status
                if self.parsed_show_int_status is not None:
                    show_int_status_elastic_template = env.get_template('elastic_standards.j2')
                    show_int_status_elastic = show_int_status_elastic_template.render(to_normalize_for_elastic=self.parsed_show_int_status)
                    # ----------------
                    # Store Interface in Elastic
                    # ----------------
                    es.index(index='%s_show_interface_status' % device.alias.lower(), id=unique_id, 
                             body=show_int_status_elastic)

                # Show Inventory
                if self.parsed_show_inventory is not None:
                    show_inventory_elastic_template = env.get_template('elastic_standards.j2')
                    show_inventory_elastic = show_inventory_elastic_template.render(to_normalize_for_elastic=self.parsed_show_inventory)
                    # ----------------
                    # Store Inventory in Elastic
                    # ----------------
                    es.index(index='%s_show_inventory' % device.alias.lower(), id=unique_id, 
                             body=show_inventory_elastic)

                # Show IP Interface Brief
                if self.parsed_show_ip_int_brief is not None:
                    show_ip_int_brief_elastic_template = env.get_template('elastic_standards.j2')
                    show_ip_int_brief_elastic = show_ip_int_brief_elastic_template.render(to_normalize_for_elastic=self.parsed_show_ip_int_brief)
                    # ----------------
                    # Store IP Interface in Elastic
                    # ----------------
                    es.index(index='%s_show_ip_interface_brief' % device.alias.lower(), id=unique_id, 
                             body=show_ip_int_brief_elastic)

                # Show IP OSPF
                if self.parsed_show_ip_ospf is not None:
                    show_ip_ospf_elastic_template = env.get_template('elastic_standards.j2')
                    show_ip_ospf_elastic = show_ip_ospf_elastic_template.render(to_normalize_for_elastic=self.parsed_show_ip_ospf)
                    # ----------------
                    # Store IP OSPF in Elastic
                    # ----------------
                    es.index(index='%s_show_ip_ospf' % device.alias.lower(), id=unique_id, 
                             body=show_ip_ospf_elastic)

                # Show IP Route
                if self.parsed_show_ip_route is not None:
                    show_ip_route_elastic_template = env.get_template('elastic_standards.j2')
                    show_ip_route_elastic = show_ip_route_elastic_template.render(to_normalize_for_elastic=self.parsed_show_ip_route)
                    # ----------------
                    # Store IP Route in Elastic
                    # ----------------
                    es.index(index='%s_show_ip_route' % device.alias.lower(), id=unique_id, 
                             body=show_ip_route_elastic)

                # Show MAC Address Table
                if self.parsed_show_mac_address_table is not None:
                    show_mac_address_table_elastic_template = env.get_template('elastic_standards.j2')
                    show_mac_address_table_elastic = show_mac_address_table_elastic_template.render(to_normalize_for_elastic=self.parsed_show_mac_address_table)
                    # ----------------
                    # Store MAC Address Table in Elastic
                    # ----------------
                    es.index(index='%s_show_mac_address_table' % device.alias.lower(), id=unique_id, 
                             body=show_mac_address_table_elastic)

                # Show Port-Channel Summary
                if self.parsed_show_port_channel_summary is not None:
                    show_port_channel_summary_elastic_template = env.get_template('elastic_standards.j2')
                    show_port_channel_summary_elastic = show_port_channel_summary_elastic_template.render(to_normalize_for_elastic=self.parsed_show_port_channel_summary)
                    # ----------------
                    # Store Port-Channel Summary in Elastic
                    # ----------------
                    es.index(index='%s_show_port_channel_summary' % device.alias.lower(), id=unique_id, 
                             body=show_port_channel_summary_elastic)

                # Show Version
                if self.parsed_show_version is not None:
                    show_version_elastic_template = env.get_template('elastic_standards.j2')
                    show_version_elastic = show_version_elastic_template.render(to_normalize_for_elastic=self.parsed_show_version)
                    # ----------------
                    # Store Version in Elastic
                    # ----------------
                    es.index(index='%s_show_version' % device.alias.lower(), id=unique_id, 
                             body=show_version_elastic)

                # Show VLAN
                if self.parsed_show_vlan is not None:
                    show_vlan_elastic_template = env.get_template('elastic_standards.j2')
                    show_vlan_elastic = show_vlan_elastic_template.render(to_normalize_for_elastic=self.parsed_show_vlan)
                    # ----------------
                    # Store vlan in Elastic
                    # ----------------
                    es.index(index='%s_show_vlan' % device.alias.lower(), id=unique_id, 
                             body=show_vlan_elastic)

                # Show VRF
                if self.parsed_show_vrf is not None:
                    show_vrf_elastic_template = env.get_template('elastic_standards.j2')
                    show_vrf_elastic = show_vrf_elastic_template.render(to_normalize_for_elastic=self.parsed_show_vrf)
                    # ----------------
                    # Store vrf in Elastic
                    # ----------------
                    es.index(index='%s_show_vrf' % device.alias.lower(), id=unique_id, 
                             body=show_vrf_elastic)

                # Show VRF all detail
                if self.parsed_show_vrf_all_detail is not None:
                    show_vrf_all_detail_elastic_template = env.get_template('elastic_standards.j2')
                    show_vrf_all_detail_elastic = show_vrf_all_detail_elastic_template.render(to_normalize_for_elastic=self.parsed_show_vrf_all_detail)
                    # ----------------
                    # Store vrf_all_detail in Elastic
                    # ----------------
                    es.index(index='%s_show_vrf_all_detail' % device.alias.lower(), id=unique_id, 
                             body=show_vrf_all_detail_elastic)

                # Show VRF all interface
                if self.parsed_show_vrf_all_interface is not None:
                    show_vrf_all_interface_elastic_template = env.get_template('elastic_standards.j2')
                    show_vrf_all_interface_elastic = show_vrf_all_interface_elastic_template.render(to_normalize_for_elastic=self.parsed_show_vrf_all_interface)
                    print (show_vrf_all_interface_elastic)
                    # ----------------
                    # Store vrf_all_interface in Elastic
                    # ----------------
                    es.index(index='%s_show_vrf_all_interface' % device.alias.lower(), id=unique_id, 
                             body=show_vrf_all_interface_elastic)

        # Goodbye Banner
        print(Panel.fit(Text.from_markup(FINISHED)))
