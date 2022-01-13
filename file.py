from pathlib import Path
import os


# from py_job import test_path

import logging

from pyats import aetest

logger = logging.getLogger(__name__)

class tc_one(aetest.Testcase):

    @aetest.setup
    def prepare_testcase(self, section):
        logger.info("Preparing the test")
        logger.info(section)

    @aetest.test
    def is_there_file(self):
       assert os.path.isfile('output.json')  == True

    @aetest.cleanup
    def clean_testcase(self):
        logger.info("Pass testcase cleanup")

# if __name__ == '__main__': # pragma: no cover
#     aetest.main()
   