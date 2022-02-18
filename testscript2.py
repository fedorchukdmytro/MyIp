
# ser = serial.Serial("/dev/ttyACM0", 115200)
# ser.close()

import logging
from logging.config import stopListening
from datetime import datetime
from socket import timeout
import paramiko
from pyats import aetest
import subprocess
from subprocess import PIPE
import json
import xtelnet
import os

logger = logging.getLogger(__name__)

parameters = {}

t = xtelnet.session()
parameters.update({'t': t })

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
        sftp = ssh_client.open_sftp()
        parameters.update({'sftp': sftp})

    @aetest.subsection
    def common_setup_params_client(self, IPAddress, util, flag1, flag2, flag3, flag4, flag5 ):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>Lounching iperf client with subprocess<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        client_process = subprocess.Popen([util, flag5, flag1, IPAddress, flag2, flag3, flag4], stdout=PIPE, stderr=PIPE)
        client_process.wait()
        parameters.update({'client_process': client_process })    
    
   
    @aetest.subsection
    def telnet_connection_setup(self, t):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>TELNET<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        ip = '10.0.0.3'
        t.connect(ip, username='root', password='danya', p=23, timeout=1)
        output1 = t.execute('timeout -t 10 tcpdump -i br0 -nn -w tcpdump_outUDP.pcap')
        print(output1)   


class MyTestcase(aetest.Testcase):

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
    def verifying_client_standart_error(self, client_process):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>client standart error<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        assert client_process.stderr.readlines() == []

    @aetest.test
    def control_speed_test(self, client_process ):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>assertion speed test<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        data =json.loads(client_process.stdout.read().decode('ascii').strip("\n"))
        assert (data['end']['streams'][0]['udp']['bytes'] / 1000) > 10
        assert (data['end']['streams'][0]['udp']['bits_per_second'] / 1000) > 10
        # print(data)
        t.execute('tftp -pl tcpdump_outUDP.pcap 10.0.0.1')
    
    @aetest.test
    def verifying_file_consistensy(self, client_process):
        file = os.stat('/srv/tftp/tcpdump_outTCP.pcap')
        print('LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL')
        print(datetime.fromtimestamp(file.st_mtime))
        assert file.st_size > 1000
        print(file.st_size)
        print('LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL')

   
   

class ScriptCommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, ssh_client, t, sftp):
        logger.info("Pass testcase cleanup")
        t.execute('rm tcpdump_outUDP.pcap')
        sftp.close()
        ssh_client.close()
        t.close()

if __name__ == '__main__':
    logging.root.setLevel(logging.INFO)
    aetest.main()