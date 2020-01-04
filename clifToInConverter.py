# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:58:43 2019

@author: Alex
"""
import os
#import check_consistency

exec(open("C:/Reasoning/macleod/tasks/check_consistency.py C:/Users/Alex/Documents/GitHub/colore/ontologies/bipartite_incidence/bipartite_incidence.clif").read())

os.system("python C:/Reasoning/macleod/tasks/check_consistency.py C:/Users/Alex/Documents/GitHub/colore/ontologies/bipartite_incidence/bipartite_incidence.clif")
os.system("pause")

#Uses Macleod to convert .clif files to .in
import subprocess
subprocess.check_output('python C:/Reasoning/macleod/tasks/check_consistency.py C:/Users/Alex/Documents/GitHub/colore/ontologies/bipartite_incidence/bipartite_incidence.clif', cwd='C:/Users/Alex', shell=True)

def runCommand(command, directory):
    #subprocess.call(command, cwd=directory, shell=True)
    subprocess.call(command, cwd=directory, shell=True)
    
command = 'python tasks/check_consistency.py C:\\Users\\Alex\\Documents\\GitHub\\colore\\ontologies\\bipartite_incidence\\bipartite_incidence.clif'
macleodFolder =r'C:\Reasoning\macleod\\'

runCommand(command, macleodFolder)

print('hello')