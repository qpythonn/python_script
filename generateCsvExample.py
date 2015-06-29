# This script aims at generating csv file that will be use to apply Btag SF. 

import ROOT
# OR using standalone code:
ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cc+')

# instantiate a calibration
calib = ROOT.BTagCalibration("MyBtagAlgo")

# create a test histogram
testhist=ROOT.TH1D("testhist","testhist", 10, 0, 1)
testhist.SetBinContent(1,2)
testhist.SetBinContent(2,5)
testhist.SetBinContent(3,1)
testhist.SetBinContent(4,6)
testhist.SetBinContent(5,0)
testhist.SetBinContent(6,2.5)
testhist.SetBinContent(7,8.7)
testhist.SetBinContent(8,9.1)


# this you need to do for every histogram:
params = ROOT.BTagEntry.Parameters(
0, # 0 means loose
"ttbar", # type of measurement / ask B-Tag conveners
"central", # systematic
0, # 0 means b-flavor
-2.4, 2.4, 
20, 800, 
0, 1,
)
entry = ROOT.BTagEntry(
testhist,
params
)
calib.addEntry(entry)


# when you are done adding the entries
with open('MyBtagAlgo_13TEV_RUNXYZ_TODAY.csv', 'w') as f:
    f.write(calib.makeCSV())
