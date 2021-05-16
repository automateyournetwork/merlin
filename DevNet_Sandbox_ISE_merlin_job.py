'''
To run the job:

$ pyats run job DevNet_Sandbox_ISE_merlin_job.py

'''

import os
from genie.testbed import load

def main(runtime):

    # Find the location of the script in relation to the job file
    testscript = os.path.join(os.path.dirname(__file__), 'DevNet_Sandbox_ISE_merlin.py')

    # run script
    runtime.tasks.run(testscript=testscript)    