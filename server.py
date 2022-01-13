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
    def server_launching(self):
       server = subprocess.Popen(['iperf3' , '-s', '--one-off'])

    @aetest.cleanup
    def clean_testcase(self):
        logger.info("Pass testcase cleanup")

# if __name__ == '__main__': # pragma: no cover
#     aetest.main()