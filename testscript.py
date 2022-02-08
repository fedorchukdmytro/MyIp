
import logging
from logging.config import stopListening
from socket import timeout
import paramiko
from pyats import aetest
import subprocess
from subprocess import PIPE
import json
import xtelnet
import sys
import time
import multiprocessing

logger = logging.getLogger(__name__)

parameters = {}

t = xtelnet.session()
parameters.update({'t': t })

class CommonSetup(aetest.CommonSetup):
    
    @aetest.subsection
    def common_telnet(self, t):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>TELNET<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        ip = '10.0.0.3'
        t.connect(ip, username='root', password='danya', p=23, timeout=10)
        output1 = t.execute('tcpdump -i br0 -nn host 10.0.0.10 and udp -c 500 -w tcpdump_out.pcap')
        print(output1)        
        
    
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
        client_process = subprocess.Popen([util, flag1, IPAddress, flag5, flag2, flag3, flag4], stdout=PIPE, stderr=PIPE)
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
        assert (data['end']['streams'][0]['udp']['bytes'] / 1000) > 20
        assert (data['end']['streams'][0]['udp']['bits_per_second'] / 1000) > 30
        print(data)

    @aetest.test
    def verifying_client_standart_error(self, client_process):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>client standart error<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        assert client_process.stderr.readlines() == []


    @aetest.test
    def verifying_tcpdump_out_pcap_getsizeof(self, ssh_client, sftp):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>pulling the file into CONTAINER OMG<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        # ftp_client.get('/srv/tftp/tcpdump_out.pcap','/pyats/MyIp_SSH_to_myMac/tcpdump_out.pcap')    
        # subprocess.run('scp fdmytro@10.0.0.1:/srv/tftp/tcpdump_out.pcap /pyats/MyIp_SSH_to_myMac/tcpdump_out.pcap')
        # ssh_client.exec_command('scp fdmytro@10.0.0.1:/srv/tftp/tcpdump_out.pcap /app/tcpdump_out.pcap')
        localpath = 'tcpdump_out.pcap'
        remotepath = '/srv/tftp/tcpdump_out.pcap'
        p1 = multiprocessing.Process(target= (sftp.get(remotepath, localpath)))
        p1.start()
        p1.join()
        print(sys.getsizeof('tcpdump_out.pcap'))
        assert sys.getsizeof('tcpdump_out.pcap') > 60

class ScriptCommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, ssh_client, t, sftp):
        logger.info("Pass testcase cleanup")
        output2 = t.execute('tftp -pl tcpdump_out.pcap 10.0.0.1')
        print(output2)
        output3 = t.execute('rm tcpdump_out.pcap')
        print(output3)
        sftp.close()
        ssh_client.close()
        t.close()
if __name__ == '__main__': # pragma: no cover
    logging.root.setLevel(logging.INFO)
    aetest.main()