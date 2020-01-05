# -*- coding: utf-8 -*-
import dataset
import ontology
import benchmarks
import glob, os
import csv
performance_file = r'..\bin-win32\performance.csv'
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
import math

# --- USERS MODIFY JUST THESE LINES ---
classCardinalityRange = {'point': 3, 'line': 3} # Specify ontology classes and class cardinality ranges 
properties = ['in'] # Specify ontology properties
#cardinalityPermutationNumModels = [1,10,25,50,75,100] 
cardinalityPermutationNumModels = [1,2,3,4,5] 
maxSecondsMace = 3600
maxSecondsProver = 3600
maxMegsProver = 2000
# ----------------------------------
p9directory = r'..\bin-win32' #Prover9 and Mace4 application installation directory
inFileDirectory = r'..\bin-win32\in_files' #Input file(s) directory, does not change

#Clear performance.csv
row = ['filename', 'falseAxiom','axiom','location','dataset','numOntologyAxioms','factsInserted','p9Time','emptyDatasetCardinalityPermutations']
with open (p9directory +'\performance.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(row)

for filename in glob.iglob(os.path.join(inFileDirectory , '*.in')):
    #Find name of filenames for all .in files.
    filename = filename.replace(inFileDirectory,'').replace('\\','').replace('.in','')
    print(filename)
    # 'r' converts normal string to raw string
    
    #cardinality dictionary for each class

    # list of relations, assume know signature beforehand
    classes= list(classCardinalityRange.keys())
    relations = classes + properties
    
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

#Graphs for each axiom
df = pd.read_csv(p9directory +'\performance.csv')
filenames = df.filename.unique()
falseAxioms = df.axiom.unique()
locations = df.location.unique()
#Create lists to plot
#Separate graphs for each axiom: 4 lines representing each test, X axis: number of facts, Y axis: time(seconds)
# x axis values - num facts in each dataset remain the same for all false axioms         
    #Error when ncols = 1, without adding the squeeze keyword you always get a 2D array
for axiom in falseAxioms:
    fig, ax = plt.subplots(figsize=(20,30),nrows=math.ceil(len(locations)/2), ncols=2, squeeze=False)
    plt.suptitle(str(axiom))
    #Without flatten, ax is a two-dimensional array: one dimension for the rows, one for the columns
    ax = ax.flatten()
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) + cycler('linestyle', ['-', '--', ':', '-.'])))
    for a,location in zip(ax,locations):
        for filename in filenames:
            factsInserted = df.loc[(df['filename'] == filename) & (df['axiom'] == axiom) & (df['location'] == location), 'factsInserted']
            plotTimes = df.loc[(df['filename'] == filename) & (df['axiom'] == axiom) & (df['location'] == location), 'p9Time']
            a.title.set_text(str(location) + " " + str(filename))
            a.plot(factsInserted, plotTimes, label = str(filename), marker = 'o') 
            a.set(xlabel='Facts Inserted',ylabel='Prover9 time (seconds)')
            a.legend() 