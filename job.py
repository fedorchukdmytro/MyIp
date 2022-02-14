import os
from pyats.easypy import Task

def main():
    
    test_path = os.path.dirname(os.path.abspath(__file__))
   
    
    task_1 = Task(testscript = os.path.join(test_path, 'testscript.py'))
    task_2 = Task(testscript = os.path.join(test_path, 'testscript2.py'))
   
   
    
    task_1.start()
    task_1.wait()
    
    task_2.start()
    task_2.wait()

    