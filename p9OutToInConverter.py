# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 15:31:00 2019

@author: Alex
"""
import glob, os
#Opens all .p9 file outputted from Macleod, and returns a .in file for each with just the axioms
MacleodOutputFolder = r'C:\Users\Alex\Documents\GitHub\colore\ontologies\bipartite_incidence\output'
inFileDirectory = r'C:\Gruninger_Research\Prover9-Mace4\bin-win32\bipartite_incidence_in_files'

for filename in glob.iglob(os.path.join(MacleodOutputFolder, '*.p9.out')):
    openFile = open(filename, 'r').readlines()
    filename = filename.replace(MacleodOutputFolder,'').replace('\\','').replace('.p9.out','')
    writeFileName = str(filename) + '.in'
    writeFile = open(inFileDirectory + '\\' + writeFileName, 'w')
    keepLine = False
    #Combining axioms
    for line in openFile:
        if '============================== INPUT =================================' in line:
            writeFile.write('formulas(assumptions).\n')
            continue
        elif 'formulas(sos)' in line:
            keepLine = True
            continue
        elif '% Reading from file' in line:
            keepLine = False
            continue
        elif 'end_of_list.' in line:
            keepLine = False
            continue
        elif '============================== end of input ==========================' in line:
            writeFile.write('end_of_list.')
            break
        #Ignore definitions
        #Definitions are of the form where <-> is at the beginning of the axiom
            # (all x all y (relationName(x,y) <-> (... some conjunction or disjunction of sentences...))).
        #do want to keep axioms that have <-> if they're somewhere in the middle/end of the axiom
            # (all x all y (relationName(x,y) -> (... some sentence that contains <-> ... ))).
        # TODO add regex instead of relying on a space before the single arrow ' ->'
        elif ' ->' in line or '<->' in line:
            if '<->' not in line:
                keepLine = True
            elif ' ->' not in line:
                keepLine = False
            #Check if ' ->' exists in the line before the '<->'
            elif line.find(' ->') < line.find('<->'):
                keepLine = True
            else:
                keepLine = False
        if keepLine == True:
            writeFile.write(line)