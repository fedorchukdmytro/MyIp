import subprocess


with open('output.json', 'w') as f:
    client_process = subprocess.Popen(['iperf3', '-c', '192.168.1.136', '-J'], stdout=f,)
client_process.wait()
# ssh_client.close()


