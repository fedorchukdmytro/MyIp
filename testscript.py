
import logging
from logging.config import stopListening
import paramiko
from pyats import aetest
import subprocess
from subprocess import PIPE
import json

logger = logging.getLogger(__name__)

parameters = {}

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def common_setup_params_server(self, IPAddress, UserName, password, server_command):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>Lounching SSH with paramiko<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname = IPAddress ,username=UserName, password=password)
        
        parameters.update({'ssh_client': ssh_client })
        serv_stdin, serv_stdout, serv_sterr = ssh_client.exec_command(server_command)
        parameters.update({'serv_stdout': serv_stdout })
        parameters.update({'serv_stdin': serv_stdin })
        parameters.update({'serv_sterr': serv_sterr })

    @aetest.subsection
    def common_setup_params_client(self, IPAddress, util, flag1, flag2, flag3, flag4 ):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>Lounching iperf client with subprocess<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        client_process = subprocess.Popen([util, flag1, IPAddress, flag2, flag3, flag4], stdout=PIPE, stderr=PIPE)
        client_process.wait()
        parameters.update({'client_process': client_process })    
                       

class MyTestcase(aetest.Testcase):

    @aetest.test
    def uid_and_groups(self):
        logger.info('notice how testcase uid/groups are modified')
        logger.info('  uid = %s' % self.uid)
        logger.info('  groups = %s' % self.groups)
       

    @aetest.test
    def verifying_server_stdout(self, serv_stdout):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>server standart output<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        logger.info(serv_stdout.read().decode('ascii').strip("\n"))
      
    @aetest.test
    def verifying_server_sterr(self, serv_sterr):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>server standart error<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        assert serv_sterr.readlines() == []
        
    @aetest.test
    def verifying_client_return_code(self, client_process):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>client return code<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        assert client_process.returncode == 0
        
    @aetest.test
    def control_speed_test(self, client_process ):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>assertion speed test<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        data =json.loads(client_process.stdout.read().decode('ascii').strip("\n"))
        assert (data['end']['streams'][0]['receiver']['bytes'] / 1000000) > 20
        assert (data['end']['streams'][0]['receiver']['bits_per_second'] / 1000000) > 30
        print(data)

    @aetest.test
    def verifying_client_standart_error(self, client_process):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>client standart error<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        assert client_process.stderr.readlines() == []


class ScriptCommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, ssh_client):
        logger.info("Pass testcase cleanup")
        ssh_client.close()
if __name__ == '__main__': # pragma: no cover
    logging.root.setLevel(logging.INFO)
    aetest.main()