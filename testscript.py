import logging
from datetime import date, datetime
from socket import timeout
import paramiko
from pyats import aetest
import subprocess
from subprocess import PIPE
import json
import xtelnet
import os
import time
from load import load_params



parameters = dict(
    load_params()["parameters"],
    telemetry=None,
    # EDM_folders=EDM_folders,
)

logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):
    
    @aetest.subsection
    def ssh_connection_with_iperf_servet(self, ssh_ipaddress, ssh_username, ssh_password, server_command):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>Lounching SSH with paramiko<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname = ssh_ipaddress ,username=ssh_username, password=ssh_password, look_for_keys=False)
        parameters.update({'ssh_client': ssh_client })
        serv_stdin, serv_stdout, serv_sterr = ssh_client.exec_command(server_command)
        parameters.update({'serv_stdout': serv_stdout })
        parameters.update({'serv_stdin': serv_stdin })
        parameters.update({'serv_sterr': serv_sterr })
        
  
    @aetest.subsection
    def common_telnet_connection_with_BBB(self, BBB_ip_addreess, BBB_user_passwd, BBB_user_name):
        logger.info('>>>>>>>>>>>>>>>>>>>>>>>>TELNET<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        t = xtelnet.session()
        ip = BBB_ip_addreess
        t.connect(ip, username=BBB_user_name, password=BBB_user_passwd, p=23, timeout=10)
        tout2=t.execute('cd / && ls')
        parameters.update({'t':t}) 
        logger.info(tout2)
        
      
class MYTESTSUITE(aetest.Testcase):

    @aetest.test
    def traffic_capture_1(self, steps, ssh_ipaddress, util, flag1, flag2, flag3, flag4, t, traffic, bandwidth, script):
        
        client_process = subprocess.Popen([util, flag1, ssh_ipaddress, flag2, flag3, flag4, traffic, bandwidth], stdout=PIPE, stderr=PIPE)
        
        tout = t.execute(f"sh {script}", read_retries=70)
        

        data =json.loads(client_process.stdout.read().decode('ascii').strip("\n"))
        client_process.wait()
        
        with steps.start(
                "Run command 'Iperf3 client"
            ) as step:
                if (data['end']['streams'][0]['receiver']['bits_per_second'] / 100) > 5:
                    step.passed(f"Traffic is running through the SUT.")
                else:
                    step.failed("Trafic is not running")
        
        logger.info(tout[:60])
        logger.info(tout[-100:-1])
        logger.info(len(tout))
        
        with steps.start(
                "Run script.sh"
            ) as step:
                if 'tcpdump: listening' in tout[:60] :
                    step.passed(f"Output  = {tout[:60]}.")
                else:
                    step.failed("tcpdump didn't start ")

        
        with steps.start(
                "Wait 1 minute."
            ) as step:
                if 'tcpdump_out.pcap' and '100%'  in tout[-100:-1]:
                    step.passed(f"Output  = {tout[-100:-1]}.")
                else:
                    step.failed("Scrip failed ")
        
        
        t.execute('rm tcpdump_out.pcap')

        
    @aetest.test
    def manual_start_2(self,steps, t):
        
        tout = t.execute("ps aux | grep tcpdump") 
    
          
        with steps.start(
                "Verification of manual start requirement."
            ) as step:
                if  tout.count('tcpdump') == 1:
                    step.passed(f"System is booted. No capturing process exists")
                else:
                    step.failed("Failed. Started automatically")


    
    @aetest.test
    def tftp_transfer_verification_3(self, steps, ssh_ipaddress, util, flag1, flag2, flag3, flag4, t, traffic, bandwidth, script):
        client_process = subprocess.Popen([util, flag1, ssh_ipaddress, flag2, flag3, flag4, traffic, bandwidth], stdout=PIPE, stderr=PIPE)
        
        tout = t.execute(f"sh {script}", read_retries=70)
        

        data =json.loads(client_process.stdout.read().decode('ascii').strip("\n"))
        client_process.wait()
        
        
        with steps.start(
                "Run command 'Iperf3 client"
            ) as step:
                if (data['end']['streams'][0]['receiver']['bits_per_second'] / 100) > 5:
                    step.passed(f"Traffic is running through the SUT.")
                else:
                    step.failed("Trafic is not running")
        
        logger.info(tout[:60])
        logger.info(tout[-100:-1])
        logger.info(len(tout))
        file = os.stat('/srv/tftp/tcpdump_outTCP.pcap')
        
        with steps.start(
                "Run script.sh"
            ) as step:
                if 'tcpdump: listening' in tout[:60] :
                    step.passed(f"Output  = {tout[:60]}.")
                else:
                    step.failed("tcpdump didn't start ")

        
        
        logger.info(tout[-100:-1])

        with steps.start(
                "Wait 1 minute."
            ) as step:
                if 'tcpdump_out.pcap' and '100% ' in tout[-100:-1]:
                    step.passed(f"Output  = {tout[-100:-1]}.")
                else:
                    step.failed("Scrip failed ")

        with steps.start(
                "Transfer to the server."
            ) as step:
                if file.st_size > 100:
                    step.passed(f"File is on the server with size {file.st_size}.")
                else:
                    step.failed("Scrip failed ")
        
        
        client_process.wait()
        t.execute('rm tcpdump_out.pcap')
        
   
    @aetest.test
    def Verification_of_the_messages_in_the_logs_7(self, steps, ssh_ipaddress, util, flag1, flag2, flag3, flag4, t, traffic, bandwidth, script):
        client_process = subprocess.Popen([util, flag1, ssh_ipaddress, flag2, flag3, flag4, traffic, bandwidth], stdout=PIPE, stderr=PIPE)
        
        tout = t.execute(f"sh {script}", read_retries=70)
    
        data =json.loads(client_process.stdout.read().decode('ascii').strip("\n"))
        client_process.wait()
        
        with steps.start(
                "Run command 'Iperf3 client"
            ) as step:
                if (data['end']['streams'][0]['receiver']['bits_per_second'] / 100) > 5:
                    step.passed(f"Traffic is running through the SUT.")
                else:
                    step.failed("Trafic is not running")
        
        logger.info(tout[:60])
        logger.info(tout[-100:-1])
        logger.info(len(tout))
        
        
        with steps.start(
                "Run script.sh"
            ) as step:
                if 'tcpdump: listening' in tout[:60] :
                    step.passed(f"Output  = {tout[:60]}.")
                else:
                    step.failed("Log with needed message did not appear")

        
        with steps.start(
                "Wait 1 minute"
            ) as step:
                if 'tcpdump_out.pcap' and '100%' in tout[-100:-1]:
                    step.passed(f"Output  = {tout[-100:-1]}.")
                else:
                    step.failed("Log with needed message did not appear")
       
       
        
        t.execute('rm tcpdump_out.pcap')



    @aetest.test
    def Kernel_version_8(self, steps, t):
        kernel = t.execute('uname -r')
        logger.info(kernel)
        
        with steps.start(
                "Run 'uname -r'"
            ) as step:
                if '4.19' in kernel:
                    step.passed(f"Verified that version of kernel appeared in log = {kernel}.")
                else:
                    step.failed("Wrong log")

      
      
      
    @aetest.test
    def traffic_load_50_mb_9(self, steps, ssh_ipaddress, util, flag1, flag2, flag3, flag4, t, traffic, bandwidth, script):   
        client_process = subprocess.Popen([util, flag1, ssh_ipaddress, flag2, flag3, flag4, traffic, bandwidth], stdout=PIPE, stderr=PIPE)
        
        tout = t.execute(f"sh {script}", read_retries=70)
        

        data =json.loads(client_process.stdout.read().decode('ascii').strip("\n"))
        client_process.wait()
        
        
        with steps.start(
                "Run command 'Iperf3 client"
            ) as step:
                if (data['end']['streams'][0]['receiver']['bits_per_second'] / 100) > 5:
                    step.passed(f"Traffic is running through the SUT.")
                else:
                    step.failed("Trafic is not running")
        
        logger.info(tout[:60])
        logger.info(tout[-100:-1])
        logger.info(len(tout))
        
        with steps.start(
                "Run script.sh"
            ) as step:
                if 'tcpdump: listening' in tout[:60] :
                    step.passed(f"Output  = {tout[:60]}.")
                else:
                    step.failed("tcpdump didn't start ")

        logger.info(tout[:60])
        with steps.start(
                "Wait 1 minute."
            ) as step:
                if 'tcpdump_out.pcap' and '100% ' in tout[-100:-1]:
                    step.passed(f"Output  = {tout[-100:-1]}.")
                else:
                    step.failed("Scrip failed ")
        client_process.wait()
        
        tel = t.execute('ls -lah')
        
        with steps.start(
                "Run command 'ls -lah'"
            ) as step:
                if 'tcpdump_out.pcap' in tel:
                    step.passed(f"tcpdump_outTCP.pcap file with captured data is present in / folder with size greate than 0 bytes")
                else:
                    step.failed("File is not preset ...")
    
         
    @aetest.test
    def system_recover_10(self, t, steps, BBB_ip_addreess, BBB_user_name, BBB_user_passwd):

        t.execute('reboot')
        
        try :
            e = t.execute('ls -lah')
        except Exception:
            e = 'BBB rebooted'
            
        logger.info(e)
        t.close()
        
        with steps.start(
                "Reboot device"
            ) as step:
                if e == 'BBB rebooted':
                    step.passed(f"The device is rebooted")
                else:
                    step.failed("System is not rebooted")
        
        time.sleep(20)
        t2 = xtelnet.session()
        ip = BBB_ip_addreess
        t2.connect(ip, username=BBB_user_name, password=BBB_user_passwd, p=23, timeout=5)
        
        tout2=t2.execute('cd / && ls -lah')
        logger.info(tout2)

        with steps.start(
                "Run 'ls -lah'"
            ) as step:
                if 'tcpdump_out.pcap' in tout2:
                    step.passed(f"System recovered. File is present")
                else:
                    step.failed("File is not preset ...")
        
       
        
        parameters.update({'t2': t2})
  

class ScriptCommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, t2, ssh_client):
        logger.info("Pass testcase cleanup")
        t2.execute('rm tcpdump_out.pcap')
     
        ssh_client.close()
        t2.close()
       

if __name__ == '__main__':
    logging.root.setLevel(logging.INFO)
    aetest.main()