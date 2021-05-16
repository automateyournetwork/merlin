# ----------------
# Copyright
# ----------------
# Written by John Capobianco, March 2021
# Copyright (c) 2021 John Capobianco

# ----------------
# Python
# ----------------
import os
import yaml
import json
import logging
from rich import print
from rich.panel import Panel
from rich.text import Text
from pyats import aetest
from jinja2 import Environment, FileSystemLoader

template_dir = "templates/juniper"
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Get logger for script
# ----------------
log = logging.getLogger(__name__)

# ----------------
# Filetypes 
# ----------------

filetype_loop = ["csv","md","html"]

class common_setup(aetest.CommonSetup):
    """Common Setup section"""

    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all the devices"""
        testbed.connect()


# Testcase name : tc_one
class CollectInformation(aetest.Testcase):
    """Parse all the commands"""

    @aetest.test
    def parse(self, testbed, section, steps):
        """ Testcase Setup section """
        # ---------------------------------------
        # Loop over devices
        # ---------------------------------------
        for device in testbed:

            with steps.start("Parsing show system information", continue_=True) as step:
                try:
                    self.parsed_system_information = device.parse("show system information")
                except Exception as e:
                    step.failed("Could not parse it correctly\n{e}".format(e=e))

            with steps.start("Parsing show chassis hardware", continue_=True) as step:
                try:
                    self.parsed_chassis_hardware = device.parse("show chassis hardware")
                except Exception as e:
                    step.failed("Could not parse it correctly\n{e}".format(e=e))

            with steps.start("Store data", continue_=True) as step:

                # Show system information
                if hasattr(self, "parsed_system_information"):
                    sh_system_information_csv_template = env.get_template("show_system_information.j2")

                with open(f"Camelot/Juniper/Show_System_Information/{device.alias}_show_system_information.json", "w") as fid:
                    json.dump(self.parsed_system_information, fid, indent=4, sort_keys=True)

                with open(f"Camelot/Juniper/Show_System_Information/{device.alias}_show_system_information.yaml", "w") as yml:
                    yaml.dump(self.parsed_system_information, yml, allow_unicode=True)

                for filetype in filetype_loop:
                    parsed_output_type = (sh_system_information_csv_template.render(variable=self.parsed_system_information["system-information"], filetype_loop_jinja2=filetype))

                    with open(f"Camelot/Juniper/Show_System_Information/{device.alias}_show_system_information.{filetype}", "w") as fh:
                        fh.write(parsed_output_type)

                os.system(f"markmap Camelot/Juniper/Show_System_Information/{device.alias}_show_system_information.md --output Camelot/Juniper/Show_System_Information/{device.alias}_show_system_information.html")

                # Show chassis hardware
                if hasattr(self, "parsed_chassis_hardware"):
                    sh_chassis_hardware_csv_template = env.get_template("show_chassis_hardware.j2")

                with open(f"Camelot/Juniper/Show_Chassis_Hardware/{device.alias}_show_chassis_hardware.json", "w") as fid:
                    json.dump(self.parsed_chassis_hardware, fid, indent=4, sort_keys=True)

                with open(f"Camelot/Juniper/Show_Chassis_Hardware/{device.alias}_show_chassis_hardware.yaml", "w") as yml:
                    yaml.dump(self.parsed_chassis_hardware, yml, allow_unicode=True)

                for filetype in filetype_loop:
                    parsed_output_type = sh_chassis_hardware_csv_template.render(variable=self.parsed_chassis_hardware["chassis-inventory"]["chassis"], filetype_loop_jinja2=filetype)

                    with open(f"Camelot/Juniper/Show_Chassis_Hardware/{device.alias}_show_chassis_hardware.{filetype}", "w") as fh:
                        fh.write(parsed_output_type)

                os.system(f"markmap Camelot/Juniper/Show_Chassis_Hardware/{device.alias}_show_chassis_hardware.md --output Camelot/Juniper/Show_Chassis_Hardware/{device.alias}_show_chassis_hardware.html")

        # Goodbye Banner
