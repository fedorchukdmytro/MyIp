from pathlib import Path
import os
from . import test_path

import logging
import subprocess
from pyats import aetest

logger = logging.getLogger(__name__)

class tc_one(aetest.Testcase):

    @aetest.setup
    def prepare_testcase(self, section):
        logger.info("Preparing the test")
        logger.info(section)

    @aetest.test
    def is_there_file(self):
       assert os.path.join(test_path, 'server.py').is_file() == True

    @aetest.cleanup
    def clean_testcase(self):
        logger.info("Pass testcase cleanup")

# if __name__ == '__main__': # pragma: no cover
#     aetest.main()













os.path.join(test_path, 'server.py').is_file() == True
   