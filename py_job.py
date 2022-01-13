import os
from pyats.easypy import Task

def main():
    
    test_path = os.path.dirname(os.path.abspath(__file__))
   
    task_1 = Task(testscript = os.path.join(test_path, 'server.py'))
    task_2 = Task(testscript = os.path.join(test_path, 'client.py'))
    
   
    task_1.start()
    task_2.start()
    
    task_1.wait()
    task_2.wait()

    task_3 = Task(testscript = os.path.join(test_path, 'test.py'))
    
    task_4 = Task(testscript = os.path.join(test_path, 'file.py'))
    
    task_3.start()
    task_3.wait()

    task_4.start()
    task_4.wait()