# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:39:44 2019

@author: Alex
"""

#For each of the 5 datasets:
#	For each axiom in the ontology
#   o	Just negated(-), 3 tests
        # 	Beginning
        # 	End
        # 	Random
#   o	1 test Skolemized/Clausal
        # 	Split random

import subprocess
import re
import random
import matplotlib.pyplot as plt
from cycler import cycler
import math
import datetime
import csv

#OWL Axioms from 
# FHKB - Family History - 137 axioms


class benchmarks:
    def __init__(self, p9directory, filename, classes, datasets, factsInsertedList, factsInsertedDict,emptyPermutationsDict, axioms, falseAxioms, axiomFalseAxiomDict, falseAxiomsSkolemized, maxSeconds, maxMegs):
        self.p9directory = p9directory
        self.filename = filename
        self.classes = classes
        self.datasets = datasets
        self.factsInsertedList = factsInsertedList
        self.factsInsertedDict = factsInsertedDict
        self.emptyPermutationsDict = emptyPermutationsDict
        self.falseAxioms = falseAxioms
        self.axiomFalseAxiomDict = axiomFalseAxiomDict
        self.falseAxiomsSkolemized = falseAxiomsSkolemized
        self.locations = ['beginning', 'random', 'random-split', 'end']
        self.maxProofAxiom = "  assign(max_proofs, 0)."
        self.maxSecondsAxiom = "  assign(max_seconds, " + str(maxSeconds) + ")."
        self.maxMegsAxiom = "  assign(max_megs, " + str(maxMegs) + ")."
        self.proofTime = {}
        self.runBenchmarks()
        return
    
    # Run command prompt
    def runCommand(self, command):
        subprocess.call(command, cwd=self.p9directory,shell=True)
    
    def runBenchmarks(self):
        # Loop through each false axiom, dataset, location and record the time it takes to find a proof, inside a dictionary
        for falseAxiom in self.falseAxioms:
            for location in self.locations:
                for dataset in self.datasets:
                    print(str(datetime.datetime.now().time())+" "+ str(falseAxiom)+str(location)+str(dataset))
                    #print(str(falseAxiom) + str(dataset) + str(location))
                    writeFileName = self.falseAxiomInputFile(falseAxiom, dataset, location, self.factsInsertedDict.get(dataset))
                    #prover9 -f subset_trans.in > subset_trans.out
                    #[:-3] to remove .in
                    self.runCommand('prover9 -f ' + writeFileName +  ' > ' + writeFileName[:-3] + '.out')
                    #Extract just the proof with proof trans
                    #prooftrans -f subset_trans.out > subset_trans.proof1
                    self.runCommand('prooftrans -f ' + writeFileName[:-3] + '.out' + ' > ' + writeFileName[:-3] + '.proof1')
                    #Extract the time required to find a proof from the proof file
                    p9Time = self.extractProofTime(writeFileName)
                    print(str(p9Time) + ' seconds needed for ' + str(writeFileName))
                    self.proofTime.update({str(falseAxiom) + str(location) + str(dataset): p9Time })
                    #self.proofTime.update({falseAxiom: {location: { dataset: self.extractProofTime(writeFileName)}}})

                    #Write to excel
                    row = [self.filename, falseAxiom, str(self.axiomFalseAxiomDict.get(falseAxiom)), location, dataset, str(len(self.falseAxioms)), str(self.factsInsertedDict.get(dataset)), str(p9Time),str(self.emptyPermutationsDict.get(dataset))]
                    with open(self.p9directory + '\performance.csv', 'a',newline='') as appendFile:
                        writer = csv.writer(appendFile)
                        writer.writerow(row)
            
                    #print(self.filename)
                    #print(falseAxiom)
                    #print(location)
                    #print(dataset)
                    #print(self.factsInsertedDict.get(dataset))
                    #print(p9Time)
                    #print('-------')
        for key in self.proofTime.keys():
            print (key + str(self.proofTime.get(key)))
        self.graphTimes()

                
    #Separate graphs for each axiom: 4 lines representing each test, X axis: number of facts, Y axis: time(seconds)
    # x axis values - num facts in each dataset remain the same for all false axioms        
    def graphTimes(self):    
        #plt.figure()
        #Error when ncols = 1, without adding the squeeze keyword you always get a 2D array
        fig, ax = plt.subplots(figsize=(50,50),nrows=math.ceil(len(self.falseAxioms)/2), ncols=2, squeeze=False)
        plt.suptitle(self.filename)
        #Without flatten, ax is a two-dimensional array: one dimension for the rows, one for the columns
        ax = ax.flatten()
        #for row in ax:
            #for col in row:
        plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) + cycler('linestyle', ['-', '--', ':', '-.'])))
        for a,falseAxiom in zip(ax,self.falseAxioms):
            for location in self.locations:
                plotTimes = [] 
                a.title.set_text(str(falseAxiom) + ' | # clauses: ' + str(len(self.falseAxiomsSkolemized.get(falseAxiom))))
                for dataset in self.datasets:
                    plotTimes.append(self.proofTime.get(str(falseAxiom) + str(location) + str(dataset)))
                a.plot(self.factsInsertedList, plotTimes, label = location, marker = 'o') 
                a.set(xlabel='Facts Inserted',ylabel='Prover9 time (seconds)')
                a.legend()
        #plt.xscale('log', basex=10)
        #plt.show()
        plt.savefig(self.p9directory + '//' + self.filename +'_benchmarks.png', bbox_inches='tight')
        

    # Find time in .proof1 file            
    def extractProofTime(self, writeFileName):
        openFile = open(self.p9directory + '\\' + writeFileName[:-3] + '.proof1', 'r').readlines()
        #-1 if Prover9 timed out
        proofTime = -1
        proofTime = None
        for line in openFile:
            if '% Proof 1 at ' in line:
                # % Proof 1 at 0.00 (+ 0.00) seconds.
                #Remove everything after opening paranthesis, then remove all non-numbers except decimals.
                line = line.replace('% Proof 1 at', '')
                line = re.sub(r'\([^)]*\)', '', line)
                line = line.replace(' seconds.', '')
                proofTime = float(line.replace(' ','').replace('\n',''))
        return proofTime
            
                    
    # Overwriting the _negated_axiom file each time as we insert a falsified axiom in a specified location     
    def falseAxiomInputFile(self, falseAxiom, dataset, location,factsInserted):
        openFile = open(self.p9directory + '\\' + str(dataset) + '.in', 'r').readlines()
        writeFileName = str(dataset) + '_negated_axiom.in'
        writeFile = open(self.p9directory + '\\' + writeFileName, 'w')
        keepLine = True
        printedProver9Options = False
        
        if location == 'random' or location == 'random-split':
            #search for line where constants begin, eg. 'point(0)'
            searchString = self.classes[0] + '(0).'
            lineCounter = 0
            startLinePossibleInsertion = -1
            endLinePossibleInsertion = -1
            for line in openFile:
                if searchString in line:
                    startLinePossibleInsertion  = lineCounter
                if 'end_of_list.' in line:
                    endLinePossibleInsertion = lineCounter - 1
                lineCounter += 1
            if location == 'random':
                #Generate random line number to insert falsified axiom
                randomLineNumber = random.randint(startLinePossibleInsertion , endLinePossibleInsertion)
                openFile[randomLineNumber] = openFile[randomLineNumber] + "% Falsified Axiom \n" + falseAxiom + "\n"
                print(randomLineNumber)
            elif location == 'random-split':
                #Generate random line number for each of the clauses in the falsified axiom
                for clause in self.falseAxiomsSkolemized.get(falseAxiom):
                    randomLineNumber = random.randint(startLinePossibleInsertion , endLinePossibleInsertion)
                    openFile[randomLineNumber] = openFile[randomLineNumber] + "% Falsified Axiom Clause \n" + clause + "\n"
                    print(randomLineNumber)
            
            
        #return
        for line in openFile:
            if  'if(Prover9). % Options for Prover9' in line:
                writeFile.write(line)
                writeFile.write(self.maxProofAxiom + "\n")
                writeFile.write(self.maxSecondsAxiom + "\n")
                writeFile.write(self.maxMegsAxiom + "\n")
                printedProver9Options = True
                continue
            if 'formulas(assumptions).' in line:
                if printedProver9Options == False:
                    writeFile.write('if(Prover9). % Options for Prover9' + "\n")
                    writeFile.write(self.maxProofAxiom + "\n")
                    writeFile.write(self.maxSecondsAxiom + "\n")
                    writeFile.write(self.maxMegsAxiom + "\n")
                    printedProver9Options = True
                    writeFile.write('end_if.' + "\n")
                writeFile.write(line)
                if location == 'beginning':
                    writeFile.write("% Falsified Axiom \n")
                    writeFile.write(falseAxiom + "\n")
                continue
            if '  assign(max_proofs,' in line:
                continue
            if '  assign(max_seconds,' in line:
                continue
            #Remove class cardinality axioms
            if 'end_of_list.' in line:
                if location == 'end':
                    writeFile.write("% Falsified Axiom \n")
                    writeFile.write(falseAxiom + "\n")
                writeFile.write(line)
                continue
            if keepLine == True:
                writeFile.write(line)
        writeFile.close()    
        return writeFileName
    
