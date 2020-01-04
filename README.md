This repository will allow you to evaluate Prover9's performance to detect inconsistencies within a generated dataset for a given ontology specified in first order logic (.in)


You only needs to edit the specified lines in **DatasetGeneratorAndBenchMarks.py** and provide .in files. 
If you only have .clif files you can install Macleod to convert from .clif to .p9 using **clifToInConverter.py** and then convert .p9 to .in using **p9OutToInConverter.py**

1. Please install Prover9 and Mace4 found at [https://www.cs.unm.edu/~mccune/prover9/gui/v05.html]

For Windows, download the file: **Prover9-Mace4-v05-setup.exe** and follow the given instructions to download MSVCP71.DLL as well

2. Download and unzip this repository to where you installed Prover9 and Mace4

For example if you installed Prover9 at C:/

For a detailed motivation of this work and the overall findings, please refer to the given Report.pdf
