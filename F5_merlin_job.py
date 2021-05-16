'''
To run the job:

$ pyats run job IOS_XE_merlin_job.py

'''

import os
from genie.testbed import load

def main(runtime):

    # Find the location of the script in relation to the job file
    testscript = os.path.join(os.path.dirname(__file__), 'F5_merlin.py')

    # run script
    runtime.tasks.run(testscript=testscript)    