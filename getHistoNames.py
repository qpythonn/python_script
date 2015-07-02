# this script makes a list of all the histogram contained in a root file or a list of root files
# FIXME: write ouput in a file, put root as argument...


import os,sys
from string import *
from ROOT import *
import time
from array import *


# File names                                                                                     
samples = []
samples.append(['output_TT', 'TTJets'])

# Get the FullSim and FastSim files:                                                             
fFl = []
fFs = []
for s in samples:
    fFl.append(TFile(s[0]+'Full.root'))
    fFs.append(TFile(s[0]+'Fast.root'))

# Get the histogram names in an example ROOT file:
histnames = []
rootkeys = fFs[0].GetListOfKeys()
for key in rootkeys:
    histnames.append(key.GetName())

print histnames
