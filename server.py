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
        ssh_client.connect(hostname='172.22.35.18' ,username='dmytrofedorchuk',password='eternity')
        parameters.update({'ssh_client': ssh_client })
        stdin, stdout, sterr = ssh_client.exec_command('iperf3 -s --one-off')
       

    @aetest.test
    def client_launching(self):
        with open('output.json', 'w') as f:
            client_process = subprocess.Popen(['iperf3', '-c', '172.22.35.18', '-J'], stdout=f,)
        client_process.wait()
       
       # remote_connection.send("iperf3 -s") 
        # remote_connection.send("\n") 
        
    # @aetest.cleanup
    # def clean_testcase(self, ssh_client):
    #     logger.info("Pass testcase cleanup")
    #     ssh_client.close()
        
# if __name__ == '__main__': # pragma: no cover
#     aetest.main()