# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 23:46:56 2019

@author: Alex
"""
p9directory = r'C:\Gruninger_Research\Prover9-Mace4'
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
import math


#Load the file with Pandas
df = pd.read_csv(p9directory +'\performance_bipartite_old_new_protege.csv')

filenames = df.filename.unique()
falseAxioms = df.axiom.unique()
locations = df.location.unique()


#Create lists to plot


#Separate graphs for each axiom: 4 lines representing each test, X axis: number of facts, Y axis: time(seconds)
# x axis values - num facts in each dataset remain the same for all false axioms         
    #plt.figure()
    #Error when ncols = 1, without adding the squeeze keyword you always get a 2D array
for axiom in falseAxioms:
    fig, ax = plt.subplots(figsize=(20,30),nrows=math.ceil(len(locations)/2), ncols=2, squeeze=False)
    plt.suptitle(str(axiom))
    #Without flatten, ax is a two-dimensional array: one dimension for the rows, one for the columns
    ax = ax.flatten()
    #for row in ax:
    #for col in row:
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) + cycler('linestyle', ['-', '--', ':', '-.'])))
    for a,location in zip(ax,locations):
        for filename in filenames:
            factsInserted = df.loc[(df['filename'] == filename) & (df['axiom'] == axiom) & (df['location'] == location), 'factsInserted']
            plotTimes = df.loc[(df['filename'] == filename) & (df['axiom'] == axiom) & (df['location'] == location), 'p9Time']
            a.title.set_text(str(location) + " " + str(filename))
            a.plot(factsInserted, plotTimes, label = str(filename), marker = 'o') 
            a.set(xlabel='Facts Inserted',ylabel='Prover9 time (seconds)')
            a.legend() 
            #plt.xscale('log', basex=10)
        #plt.show()
        #plt.savefig(p9directory + '//' + str(axiom) +'_benchmarks.png', bbox_inches='tight')
            