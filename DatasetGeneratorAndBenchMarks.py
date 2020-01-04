# -*- coding: utf-8 -*-
import dataset
import ontology
import benchmarks
import glob, os
import csv

# Can convert .clif files to .p9.out with Macleod
# python tasks/check_consistency_all.py C:\Users\Alex\Documents\GitHub\colore\ontologies\bipartite_incidence\ 

# --- USERS MODIFY JUST THESE LINES ---
p9directory = r'C:\Gruninger_Research\Prover9-Mace4\bin-win32' #Prover9 and Mace4 application installation directory
inFileDirectory = r'C:\Gruninger_Research\Prover9-Mace4\bin-win32\bipartite_incidence_in_files4' #Input file(s) directory
classCardinalityRange = {'point': 3, 'line': 3} # Specify ontology classes and class cardinality ranges 
properties = ['in'] # Specify ontology properties
cardinalityPermutationNumModels = [1,10,25,50,75,100] 
maxSecondsMace = 3600
maxSecondsProver = 3600
maxMegsProver = 2000
# ----------------------------------

#Clear performance.csv
row = ['filename', 'falseAxiom','axiom','location','dataset','numOntologyAxioms','factsInserted','p9Time','emptyDatasetCardinalityPermutations']
with open (p9directory +'\performance.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(row)

for filename in glob.iglob(os.path.join(inFileDirectory , '*.in')):
    filename = filename.replace(inFileDirectory,'').replace('\\','').replace('.in','')
    print(filename)
    # 'r' converts normal string to raw string
    #directory = r'C:\Users\Alex\OneDrive\Documents\1. U OF T\Gruninger Research\Prover9-Mace4\bin-win32\\'  + filename)
    #os.mkdir(r'C:\Users\Alex\OneDrive\Documents\1. U OF T\Gruninger Research\Prover9-Mace4\bin-win32\\' + filename)
    
    #cardinality dictionary for each class

    # list of relations, assume know signature beforehand
    classes= list(classCardinalityRange.keys())
    relations = classes + properties
    # models for each cardinality combination
    #cardinalityPermutationNumModels = [1,10,50,100,150,200,250,275]
    #cardinalityPermutationNumModels = [1,10]

    #maxSecondsProver = 60*60*60*24
    
    newOntology = ontology.ontology(p9directory,inFileDirectory,filename)
    
    # dataset keys are filename and number of models
    datasets = {}
    for numModels in cardinalityPermutationNumModels:
        datasets.update({str(filename)+"_dataset" + str(numModels) : dataset.dataset(p9directory, inFileDirectory, filename, newOntology.getAxioms(), classes, properties, classCardinalityRange, numModels, maxSecondsMace)})
    
    factsInsertedList = []
    factsInsertedDict = {}
    emptyPermutationsDict = {}
    for key in datasets.keys():
        eachDataset = datasets.get(key)
        factsInsertedList.append(eachDataset.getFactsInserted())
        factsInsertedDict.update({key:eachDataset.getFactsInserted()})
        emptyPermutationsDict.update({key:eachDataset.getNumEmptyCardinalityPermutations()})
    factsInsertedList.sort()
    
    newBenchmarks = benchmarks.benchmarks(p9directory, filename, classes, datasets,factsInsertedList, factsInsertedDict, emptyPermutationsDict, newOntology.getAxioms(), newOntology.getFalseAxioms(), newOntology.getAxiomFalseAxiomDict(), newOntology.getFalseAxiomsSkolemized(), maxSecondsProver, maxMegsProver)

    #print(newBenchmarks.factsInsertedList)
    
    # Move all ontology files into separate folder named after ontology
    #for ontologyFiles in glob.iglob(os.path.join(p9directory , str(filename) + '*')):
    #    print(ontologyFiles)