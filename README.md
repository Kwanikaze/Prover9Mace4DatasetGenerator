This repository will allow you to evaluate Prover9's performance to detect inconsistencies within a generated dataset for a given ontology specified in first order logic (.in)


You only needs to edit the specified lines in **DatasetGeneratorAndBenchMarks.py** and provide .in files. 


1. Please install Prover9 and Mace4 found at [https://www.cs.unm.edu/~mccune/prover9/gui/v05.html]

For Windows, download the file: **Prover9-Mace4-v05-setup.exe** and follow the given instructions to download MSVCP71.DLL as well

2. Download and unzip this repository to where you installed Prover9 and Mace4

For example if you installed Prover9 at C:/

For a detailed motivation of this work and the overall findings, please refer to the given Report.pdf

## Converting .clif files to .in

If you only have .clif files you can install Macleod as found here: [https://github.com/thahmann/macleod]. Macelod is a set of Python 2 scripts that can do the translation from CLIF to the Prover9 and TPTP syntaxes locally on your machine.
For Windows, you will need to install the PyWin32 and WMI dependencies on top of the Python libraries mentioned in the Macleod README. 

FYI the installation instructions are a bit scattered on the GitHub repo, but some things to note:
- in addition to the README, also look at these instructions: https://github.com/thahmann/macleod/blob/master/doc/2014-07-31_setup.txt 
- make sure to clone our COLORE repository (http://github.com/gruninger/colore) onto your computer
- clone Torsten's scripts into their own folder
- change the paths in macleod_win.conf to point to the required folders
- edit your Python System Path variable to include the macleod/bin folder (Section 2, Step 4: https://github.com/thahmann/macleod/blob/master/doc/Macleod-Manual.pdf)


The script **clifToInConverter.py** runs Macleod from the command line to convert from .clif to .p9 and then use **p9OutToInConverter.py** to convert the Macleod output of .p9.out files to .in.
