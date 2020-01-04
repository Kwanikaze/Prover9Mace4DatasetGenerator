# -*- coding: utf-8 -*-
import string
import subprocess
import re
from itertools import groupby
import copy
import os

class dataset:
    def __init__(self, p9directory, inFileDirectory, filename, axioms, classes, properties, classCardinalityRange, cardinalityPermutationNumModels, maxSeconds):
        self.p9directory = p9directory
        self.inFileDirectory = inFileDirectory
        self.filename = filename
        self.classes = classes
        self.properties = properties
        self.relations = self.classes + self.properties
        #Place all dictionary values into a list
        self.classCardinalityRange = classCardinalityRange
        # Constraint to stop searching when the n-th structure has been found.
        self.cardinalityPermutationNumModels = cardinalityPermutationNumModels
        self.numModelAxiom = "  assign(max_models, " + str(cardinalityPermutationNumModels) + ")."
        self.maxSecondsAxiom = "  assign(max_seconds, " + str(maxSeconds) + ")."
        self.models = {}  # Dictionary of dictionaries of lists, Dictionary key is both cardinality permutation and model number
        self.uniqueModels = {}
        self.factsInserted = 0
        self.numCardinalityPermutations = 0
        self.numEmptyCardinalityPermutations = 0
        self.datasetConstantCounter = 0
        self.axioms = axioms
        self.createDataset()
        return
    
    def getcardinalityPermutationNumModels(self):
        return self.cardinalityPermutationNumModels
    
    def getDatasetConstantCounter(self):
        return self.datasetConstantCounter
    
    def getUniqueModels(self):
        return self.uniqueModels
    
    def getFactsInserted(self):
        return self.factsInserted
    
    def getNumEmptyCardinalityPermutations(self):
        return self.numEmptyCardinalityPermutations
    
    #Main function, calls all helper functions to create dataset function
    def createDataset(self):        
        #Tuples for each permutations
        self.cardinalityPermutations = self.findAllCardinalityPermutations(list(self.classCardinalityRange.values()))
        for perm in self.cardinalityPermutations:
            classCardinalityPerm = {}
            for i in range(0, len(self.classCardinalityRange)):
                classCardinalityPerm.update({list(self.classCardinalityRange.keys())[i]:perm[i]})
            print(classCardinalityPerm)
            cardinalityAxioms = self.createCardinalityAxioms(classCardinalityPerm)
            self.inputAndCookedFile(cardinalityAxioms, classCardinalityPerm)
            self.parseCookedFile(classCardinalityPerm)
            self.numCardinalityPermutations += 1
        self.uniqueConstants()
        self.addDatasetConstantsToInputFile()
        #self.numCardinalityPermutations = len(tuple(i for i in self.cardinalityPermutations))
        print(str(self.factsInserted) + " facts inserted with " + str(self.cardinalityPermutationNumModels) + " model(s) for each of the " + str(self.numCardinalityPermutations) 
        + " class cardinality permutations. There was " + str(self.numEmptyCardinalityPermutations) + " cardinality permutation(s) that returned no model(s).")
        return
        #return self.uniqueModels
    
    #Recursive function to find all cardinality permutations
    def findAllCardinalityPermutations(self, limits):
         # Generate all permutations with separate limits for each index    
        if not limits:
            yield()
            return
        
        for l in self.findAllCardinalityPermutations(limits[1:]):
            for i in range(1, limits[0]+1):
                yield (i,) + l
                
    #Creates axiom for each class
    def createCardinalityAxioms(self, classCardinality):
        cardinalityAxioms = []
        for key, value in classCardinality.items():
            #Create list of letter constants
            cardinalityString = ""
            letters = list(string.ascii_lowercase)[0:value]
            existsLetters = ['exists ' + letter + ' ' for letter in letters]
            cardinalityString += ("".join(str(x) for x in existsLetters)) + "("
            existsClassLetter = [key + '(' + letter + ')' for letter in letters]
            cardinalityString += (" & ".join(str(x) for x in existsClassLetter))
            if value > 1:
                # add a!=b, a!=c, b!=c
                counter = 0
                while counter < value:
                    counter2 = counter + 1
                    var1 = letters[counter]
                    while counter2 < value:
                        var2 = letters[counter2]
                        cardinalityString += (" & -(" + var1 + "=" + var2 + ")")
                        counter2 += 1        
                    counter += 1
            cardinalityString += ")."
            cardinalityAxioms.append(cardinalityString)
        return cardinalityAxioms
    
    # Run command prompt
    def runCommand(self, command):
        subprocess.call(command, cwd=self.p9directory,shell=True)
    
    # Obtain  .out and .cooked file
    def inputAndCookedFile(self, cardinalityAxioms, classCardinalityPerm):
        #Read the file entirely, then open the same file in write mode and append when at the end
        #Open .in file in read mode, 'r'
        openFile = open(self.inFileDirectory + '\\' + self.filename +  '.in', 'r').readlines()
        writeFile = open(self.p9directory + '\\' + self.filename + str(self.cardinalityPermutationNumModels) +  '.in', 'w')
        
        # modify with constants and cardinality and domain start_size
        cardinalityAxiomsCommentExists = False
        printedMace4Options = False
        FirstEndofListNotYetEncountered = True
        keepLine = True
        for line in openFile:
            #add numModel axiom after "if(Mace4).   % Options for Mace4"
            if  'if(Mace4).   % Options for Mace4' in line:
                writeFile.write(line)
                newLine = "%s" % (self.numModelAxiom)
                writeFile.write(newLine + "\n")
                newLine = "%s" % (self.maxSecondsAxiom)
                writeFile.write(newLine + "\n")
                printedMace4Options = True
                continue
            if 'formulas(assumptions).' in line and printedMace4Options == False:
                writeFile.write('if(Mace4).   % Options for Mace4' + "\n")
                newLine = "%s" % (self.numModelAxiom)
                writeFile.write(newLine + "\n")
                newLine = "%s" % (self.maxSecondsAxiom)
                writeFile.write(newLine + "\n")
                writeFile.write('end_if.' + "\n")
                writeFile.write(line)
                printedMace4Options = True
                continue

            #Don't keep previous max_seconds and max_moxels lines
            if 'assign(max_seconds,' in line:
                continue
            if 'assign(max_models,' in line:
                continue
            #add cardinality axioms before first 'end_of_list'    
            if '% Class cardinality' in line:
                #Keep the Prover9 comment denoting where class cardinality axioms start
                writeFile.write(line)
                keepLine = False
                cardinalityAxiomsCommentExists = True
                continue
            if 'end_of_list.' in line and FirstEndofListNotYetEncountered == True:
                #If "% Class cardinality" is not in the file, add it
                if cardinalityAxiomsCommentExists == False:
                    writeFile.write("% Class cardinality" + "\n")        
                keepLine = True
                FirstEndofListNotYetEncountered = False
                for axiom in cardinalityAxioms:
                    newLine = "%s" % (axiom)
                    writeFile.write(newLine + "\n")
                writeFile.write(line)
                continue
            if keepLine == True:
                writeFile.write(line)
        writeFile.close()
        
        # https://www.cs.unm.edu/~mccune/mace4/manual/2009-02A/m4-options.html
        # https://www.cs.unm.edu/~mccune/prover9/manual/2009-11A/
        # mace4 -c -f uni_simple.in > uni_simple.mace4.out
        # interpformat cooked    -f uni_simple.mace4.out > uni_simple.cooked
        self.runCommand('mace4 -c -f ' + self.filename + str(self.cardinalityPermutationNumModels)  + '.in > ' + self.filename + str(self.cardinalityPermutationNumModels) + '.out')
        self.runCommand('interpformat cooked    -f ' + self.filename + str(self.cardinalityPermutationNumModels)  + '.out > ' + self.filename + str(self.cardinalityPermutationNumModels)  + '-' + re.sub("[^0-9]", "", str(list(classCardinalityPerm.values()))) + '.cooked')
    
    #Updates self.models with models from Cooked file
    def parseCookedFile(self, classCardinalityPerm):
        openFile = open(self.p9directory + '\\' + self.filename + str(self.cardinalityPermutationNumModels) + '-' + re.sub("[^0-9]", "", str(list(classCardinalityPerm.values()))) +  '.cooked')
        contentLines =  openFile.readlines()
        #Split list into list of lists, split based on "% Interpretation of size"
        contentLinesList = [list(g) for k,g in groupby(contentLines,lambda x:'% Interpretation of size' in x) if not k]
        #Drop first element as it doesn't contain a model just states: % number = 1 % seconds = 0
        if contentLinesList:
            del contentLinesList[0]
            modelNum = 0
            for modelLines in contentLinesList:
                relationsInstance = {}
                # split cooked in file after encountering each 
                for relation in self.relations:
                    #Find lines of each relation, Keep relation numeric IDs only without a dash
                    relationLines = [r for r in modelLines if "-" not in r and str("  " + relation + "(" ) in r]
                    #if not empty
                    if relationLines:
                        IDs = []
                        for line in relationLines:
                            #Search for all non numbers, replace all non numbers and non-commas with nothing
                            IDs.append(re.sub("[^0-9,]", "", str(line)))
                        if relation not in self.classes:
                            instances = []
                            for pair in IDs:
                                IDs = [p for p in pair.split(',')]
                                IDs = list(map(int, IDs))
                                instances.append(IDs)
                            relationsInstance.update({relation: instances})
                        else:      
                           IDs = list(map(int, IDs))
                           IDs = [[i] for i in IDs]
                           relationsInstance.update({relation: IDs })
                #Dictionary key is both cardinality permutation and model number
                self.models.update({str(modelNum) + "-" + re.sub("[^0-9]", "", str(list(classCardinalityPerm.values()))): relationsInstance})
                modelNum += 1
        else:
            self.numEmptyCardinalityPermutations += 1
            print(self.filename + re.sub("[^0-9]", "", str(list(classCardinalityPerm.values()))) +  '.cooked' + " is empty!")
    
    # Makes models not use same numeric constants
    def uniqueConstants(self):
        self.datasetConstantCounter = 0
        # A Python dictionary is a mutable data type
        self.uniqueModels = copy.deepcopy(self.models)
        for model in self.models:
            modelConstantCounter = 0
            #Loop through all relations, if there are is a constant change it
            constantExists = True
            while constantExists == True:
                constantExists = False
                for eachRelation in self.relations:
                    for i in range(0,len(self.models.get(model)[eachRelation])):
                        for j in range(0,len(self.models.get(model)[eachRelation][i])):
                            #Find constants starting from 0 to size n of each model
                            if modelConstantCounter == self.models.get(model)[eachRelation][i][j]:
                                constantExists = True
                                #Set model constant equal to dataset Counter constant
                                self.uniqueModels.get(model)[eachRelation][i][j] = self.datasetConstantCounter
                if constantExists == True:
                    modelConstantCounter +=1
                    self.datasetConstantCounter +=1
                    #print(self.datasetConstantCounter)
    # Adds all models to new .IN file
    def addDatasetConstantsToInputFile(self):
        # Add uniqueModels as constants
        openFile = open(self.inFileDirectory + '\\' + self.filename +  '.in', 'r').readlines()
        writeFile = open(self.p9directory + '\\' + self.filename + '_dataset' + str(self.cardinalityPermutationNumModels) + '.in', 'w')
            
        keepLine = True
        FirstEndofListNotYetEncountered = True
        for line in openFile:
            #Remove max_seconds and max_models
            if 'assign(max_seconds,' in line:
                continue
            if 'assign(max_models,' in line:
                continue 
            # Remove class cardinality comment and axioms
            if '% Class cardinality' in line:
                keepLine = False
                continue
            if 'end_of_list.' in line and FirstEndofListNotYetEncountered == True:
                FirstEndofListNotYetEncountered = False
                for model in self.uniqueModels:
                    for eachRelation in self.uniqueModels.get(model):
                        for i in range(0,len(self.uniqueModels.get(model)[eachRelation])):
                            #print(eachRelation + "(" + str(uniqueModels.get(model)[eachRelation][i])[1:-1] + ")")
                            writeFile.write(eachRelation + "(" + str(self.uniqueModels.get(model)[eachRelation][i])[1:-1] + ")."+ "\n")
                            self.factsInserted += 1
                keepLine = True
                writeFile.write(line)
                continue
            if keepLine == True:
                writeFile.write(line) 
        writeFile.close()
        
        #Rename writeFile with # facts inserted
        #os.rename(self.p9directory+'\\'+self.filename + '_dataset' + str(self.cardinalityPermutationNumModels) + '.in',self.p9directory+'\\'+ self.filename + '_dataset' + str(self.cardinalityPermutationNumModels) + '_'+ str(self.factsInserted) + '.in') 
        return
        