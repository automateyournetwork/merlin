'''
To run the job:

$ pyats run job DevNet_Sandbox_Nexus9k_NXAPI_lancelot_job.py --testbed-file testbed/testbed_DevNet_Nexus9k_Sandbox.yaml

'''

import os
from genie.testbed import load

def main(runtime):

    # Find the location of the script in relation to the job file
    testscript = os.path.join(os.path.dirname(__file__), 'DevNet_Sandbox_Nexus9k_NXAPI_lancelot.py')

    # run script
    runtime.tasks.run(testscript=testscript)