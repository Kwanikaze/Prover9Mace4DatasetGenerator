# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 11:20:01 2019

@author: Alex
"""
import glob, os
import dataset
import ontology
import re



p9directory = r'C:\Gruninger_Research\Prover9-Mace4\bin-win32'
inFileDirectory = r'C:\Gruninger_Research\Prover9-Mace4\bin-win32\bipartite_incidence_in_files_protege'

for filename in glob.iglob(os.path.join(inFileDirectory , '*.in')):
    filename = filename.replace(inFileDirectory,'').replace('\\','').replace('.in','')
    print(filename)
    # 'r' converts normal string to raw string
    #directory = r'C:\Users\Alex\OneDrive\Documents\1. U OF T\Gruninger Research\Prover9-Mace4\bin-win32\\'  + filename)
    #os.mkdir(r'C:\Users\Alex\OneDrive\Documents\1. U OF T\Gruninger Research\Prover9-Mace4\bin-win32\\' + filename)
    
    #cardinality dictionary for each class
    classCardinalityRange = {'point': 3, 'line': 3}
    # list of relations, assume know signature beforehand
    classes= list(classCardinalityRange.keys())
    properties = ['in']
    relations = classes + properties
    # models for each cardinality combination
    #cardinalityPermutationNumModels = [1,10,50,100,150,200,250,275]
    #cardinalityPermutationNumModels = [1,10]
    cardinalityPermutationNumModels = [1,10,25,50,75,100]
    #cardinalityPermutationNumModels = [100]
    maxSecondsMace = 3600
    maxSecondsProver = 3600
    maxMegsProver = 2000
    #maxSecondsProver = 60*60*60*24
    
    newOntology = ontology.ontology(p9directory,inFileDirectory,filename)
    
    # dataset keys are filename and number of models
    datasets = {}
    for numModels in cardinalityPermutationNumModels:
        datasets.update({str(filename)+"_dataset" + str(numModels) : dataset.dataset(p9directory, inFileDirectory, filename, newOntology.getAxioms(), classes, properties, classCardinalityRange, numModels, maxSecondsMace)})


ontologyOWLDirectory = r'C:\Gruninger_Research\Stacy\In to OWL\OntologyOWL'
protegeDirectory = r'C:\Gruninger_Research\Stacy\In to OWL'
ontologyURI = 'http://www.semanticweb.org/alex/ontologies/2019/7/untitled-ontology-43'

#Only a single key in the dataset
#Adding the same dataset to all .OWL files
for key in datasets.keys():
    eachDataset = datasets.get(key)
    uniqueModels = eachDataset.getUniqueModels()
    numberInstances = eachDataset.getDatasetConstantCounter()
    for filename in glob.iglob(os.path.join(ontologyOWLDirectory, '*.owl')):
        filename = filename.replace(ontologyOWLDirectory,'').replace('\\','').replace('.owl','')
        print(filename)

        openFile = open(ontologyOWLDirectory  + '\\' + filename +  '.owl', 'r').readlines()
        writeFile = open(protegeDirectory + '\\' + filename + "_" + str(eachDataset.getcardinalityPermutationNumModels()) +  '.OWL', 'w')
        keepLine = True
        for line in openFile:
            if 'Declaration(ObjectProperty(<http://www.semanticweb.org/ontologies/2016/3/weak_tripartite.owl#in>))' in line:
                writeFile.write(line)    
                for i in range(0,numberInstances):
                    #Named Individual
                    writeFile.write("Declaration(NamedIndividual(<http://www.semanticweb.org/alex/ontologies/2019/7/untitled-ontology-43#" + str(i) +">))\n")
                continue
            if line == ')':
                writeFile.write('############################\n#   Named Individuals\n############################\n')
                for model in uniqueModels:
                    for eachRelation in uniqueModels.get(model):
                        for i in range(0,len(uniqueModels.get(model)[eachRelation])):
                            if eachRelation in classes:
                                #Class Assertion
                                #ClassAssertion(:Point <http://www.semanticweb.org/alex/ontologies/2019/7/untitled-ontology-43#2>)
                                writeFile.write("ClassAssertion(:" + eachRelation + " <" + ontologyURI + "#" + str(uniqueModels.get(model)[eachRelation][i])[1:-1] + ">)\n")
                            elif eachRelation in properties:
                                IDs = []
                                #Search for all non numbers, replace all non numbers and non-commas with nothing
                                IDs.append(re.sub("[^0-9,]", "", str(uniqueModels.get(model)[eachRelation][i])[1:-1]))
                                instances = []
                                for pair in IDs:
                                    IDs = [p for p in pair.split(',')]
                                    IDs = list(map(int, IDs))
                                    instances.append(IDs)
                                instances = instances[0]
                                #Object Property Assertion(in)
                                #ObjectPropertyAssertion(<http://www.semanticweb.org/ontologies/2016/3/weak_tripartite.owl#in> <http://www.semanticweb.org/alex/ontologies/2019/7/untitled-ontology-43#2> <http://www.semanticweb.org/alex/ontologies/2019/7/untitled-ontology-43#3>)
                                writeFile.write("ObjectPropertyAssertion(<http://www.semanticweb.org/ontologies/2016/3/weak_tripartite.owl#" + eachRelation + "> <" + ontologyURI +"#" + str(instances[0]) + "> <" + ontologyURI + "#" + str(instances[1]) + ">)\n")
            if keepLine == True:
                writeFile.write(line)
        writeFile.close()
    


#Assumes already created .OWL file for given ontology
#Protege has no command line tools







