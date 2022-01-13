import logging
import json
from pyats import aetest

logger = logging.getLogger(__name__)

class tc_one(aetest.Testcase):

    @aetest.setup
    def prepare_testcase(self, section):
        logger.info("Preparing the test")
        logger.info(section)

  
    @aetest.test
    def assert_test(self):
        with open('output.json', 'r') as data_file:
            data = json.load(data_file)
            assert (data['end']['streams'][0]['receiver']['bytes'] / 1000000) > 40
            assert (data['end']['streams'][0]['receiver']['bits_per_second'] / 1000000) > 5
    @aetest.cleanup
    def clean_testcase(self):
        logger.info("Pass testcase cleanup")

# if __name__ == '__main__': # pragma: no cover
#     aetest.main()