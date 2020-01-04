# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 12:32:05 2019

@author: Alex Kwan, Semantic Technologies Lab


"""
import re
import subprocess

class ontology:
    def __init__(self,p9directory,inFileDirectory,filename):
        self.p9directory = p9directory
        self.inFileDirectory = inFileDirectory
        self.filename = filename
        self.axioms = []
        self.falseAxioms = []
        self.axiomFalseAxiomDict = {}
        self.falseAxiomsSkolemized = {}
        self.parseAxioms()
        self.skolemizeFalseAxioms()
        
    # Run command prompt
    def runCommand(self, command):
        subprocess.call(command, cwd=self.p9directory,shell=True)
    
    def getAxioms(self):
        return self.axioms
    
    def getFalseAxioms(self):
        return self.falseAxioms
    
    def getAxiomFalseAxiomDict(self):
        return self.axiomFalseAxiomDict
    
    def getFalseAxiomsSkolemized(self):
        return self.falseAxiomsSkolemized
   
    def skolemizeFalseAxioms(self):
        #Create input file with single axiom to clausify in Prover9
        for falseAxiom in self.falseAxioms:
            #falseAxiom = self.falseAxioms[0]
            #'w', Write - will overwrite any existing content
            writeFile = open(self.p9directory + '\\singleFalseAxiom.in', 'w')
            writeFile.write('formulas(assumptions).\n' + falseAxiom + '\nend_of_list.')
            writeFile.close()
            self.runCommand('prover9 -f singleFalseAxiom.in > singleFalseAxiom.out')
            #Extract clauses from out file
            openFile =  open(self.p9directory + '\\singleFalseAxiom.out', 'r').readlines()
            reviewLine = False
            formulasTimesEncountered = 0
            clauseList = []
            for line in openFile:
                #Extract lines that contain clausify and are between the first formulas(sos). and end_of_list.
                if 'formulas(sos).' in line:
                    reviewLine = True
                    formulasTimesEncountered +=1
                if ('[clausify(1)].' in line and reviewLine == True and formulasTimesEncountered == 1):
                    line = line.replace('  [clausify(1)].\n', '')
                    clauseList.append(line)
                if 'end_of_list.' in line:
                    reviewLine = False
            #writeFile.close()
            self.falseAxiomsSkolemized.update({falseAxiom: clauseList})
        #print(self.falseAxiomsSkolemized)
            
        return
    
    #Uses .in file to extract axioms into a list: self.axioms
    def parseAxioms(self):
        openFile = open(self.inFileDirectory + '\\' + self.filename +  '.in', 'r').readlines()
        
        #Remove everything before "formulas(assumptions)." and after "%Class Carindality". Delete all comment lines, starting with "%". 
        keepLine = False
        axiomsList = []
        for line in openFile:
            if 'formulas(assumptions).' in line:
                keepLine=True
                continue
            if 'end_of_list.' in line:
                keepLine=False
                continue
            if '% Class cardinality' in line:
                keepLine = False
                continue
            if keepLine == True and "%" not in line:
                axiomsList.append(line.replace('\n','') .replace('\t','').replace('  ',''))
        

        axiomsString = ''.join(axiomsList)
        #positive look behind, keeps the period
        self.axioms = re.split(r'(?<=\.)',axiomsString)
        # Remove empty elements
        self.axioms = list(filter(None, self.axioms))
        for axiom in self.axioms:
            falseAxiom = "-(" + axiom[:-1] + ")."
            self.axiomFalseAxiomDict.update({falseAxiom:axiom})
            self.falseAxioms.append(falseAxiom)
        #self.falseAxioms = ["-(" + axiom[:-1] + ")." for axiom in self.axioms]
        return