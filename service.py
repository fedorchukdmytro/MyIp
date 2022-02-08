from time import sleep
import time
import testscript
# for _ in range(0,5):
#     testscript.aetest.main()
#     import subprocess

# subprocess.call("Script1.py", shell=True)# do whatever is in test1.py


import subprocess
attempt = 1
for _ in range(0,100):
    _ = subprocess.Popen(['python3 testscript.py -datafile data/simple_data.yaml'], shell=True)
    _.wait()
    time.sleep(10)
    print(f'********************************************* ATTEMPT NUMBER {attempt}***************************************************')
    attempt += 1
