This repository will allow you to evaluate Prover9's performance to detect inconsistencies within a generated dataset for a given ontology specified in first order logic (.in).


## Installation
Please ensure you have Python 3 installed, I recommend Anaconda [https://www.anaconda.com/distribution/] as it will allow you to create environments for Python 2 as well (which is required to run the optional library Macleod Alpha as discussed in the last section below).

1. Please install Prover9 and Mace4 found at [https://www.cs.unm.edu/~mccune/prover9/gui/v05.html]

For Windows, download the file: **Prover9-Mace4-v05-setup.exe** and follow the given instructions to download **MSVCP71.DLL** as well

2. Running your terminal as Administrator, clone this repository to the directory of where you installed Prover9 and Mace4. For example if you installed Prover9-Mace4 at *C:\Program Files\Prover9-Mace4*, clone this repository to that same directory.

3. Create a folder named 'in_files' in the *\Prover9-Mace4\bin-win32\* directory and place your .in files there.


## For given ontologies, generating datasets with Mace4 and evaluating Prover9's performance to detect inconsistencies within the dataset
Running your IDE as an Administrator, you only need to edit the specified lines in **DatasetGeneratorAndBenchMarks.py**.
*classCardinalityRange* is a dictionary where the keys are the ontology classes and the values are the max cardinality requirements.
*properties* is a list for the ontology properties.
*cardinalityPermutationNumModels* is a list where the length of the list is the number of datasets to generate for each ontology.

For each axiom and ontology the scripts plot Prover9's time to detect a falsified axiom for each of the four locations: beginning, end, randomly placed, as well as skolemized and split up.

## Converting .clif files to .in

If you only have .clif files you can install Macleod as found here: [https://github.com/thahmann/macleod]. Macelod is a set of Python 2 scripts that can do the translation from CLIF to the Prover9 and TPTP syntaxes locally on your machine.
For Windows, you will need to install the PyWin32 and WMI dependencies on top of the Python libraries mentioned in the Macleod README. 

FYI the installation instructions are a bit scattered on the GitHub repo, but some things to note:
- in addition to the README, also look at these instructions: [https://github.com/thahmann/macleod/blob/master/doc/2014-07-31_setup.txt]
- clone Macleod scripts into their own folder
- change the paths in macleod_win.conf to point to the required folders
- edit your Python System Path variable to include the macleod/bin folder (Section 2, Step 4: https://github.com/thahmann/macleod/blob/master/doc/Macleod-Manual.pdf)


The script **clifToInConverter.py** runs Macleod from the command line to convert from .clif to .p9.out and then use **p9OutToInConverter.py** to convert the Macleod output of .p9.out files to .in.
