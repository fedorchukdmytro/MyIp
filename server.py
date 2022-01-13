import logging
import subprocess
from pyats import aetest
import paramiko
logger = logging.getLogger(__name__)
import time


parameters ={}

class tc_one(aetest.Testcase):
    
    @aetest.setup
    def prepare_testcase(self, section):
        
        logger.info("Preparing the test")
        logger.info(section)
        # server = subprocess.Popen("ssh {user}@{host} {cmd}".format(user='dmytrofedorchuk', host='172.22.35.18', cmd='-s'))     #, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='172.22.35.18' ,username='dmytrofedorchuk',password=PASSWORD)
        parameters.update({'ssh_client': ssh_client })
        # stdin, stdout, sterr = ssh_client.exec_command('/opt/homebrew/bin/iperf3 -s -1')

    @aetest.test
    def client_launching(self, ssh_client):
        stdin, stdout, sterr = ssh_client.exec_command('/opt/homebrew/bin/iperf3 -s -1')
        time.sleep(60)
       # remote_connection.send("iperf3 -s") 
        # remote_connection.send("\n") 
        
    @aetest.cleanup
    def clean_testcase(self, ssh_client):
        logger.info("Pass testcase cleanup")
        ssh_client.close()
        
# if __name__ == '__main__': # pragma: no cover
#     aetest.main()