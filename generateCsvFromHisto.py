# This script aims at generating csv file that will be use to apply Btag SF. 
# It takes a list of histograms as input.


## TO DO
# Check for different tagger (not urgent) CSVIVF (urgent)
# add automatic check and the end of the script (python checkBTagCalibrationConsistency.py)
# add tight workig point
# extend bin of input
##


import ROOT
# OR using standalone code:
ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cc+')

# instantiate a calibration
calib = ROOT.BTagCalibration("CSV")

# Load the root file
inputFileName= ROOT.TFile("/user/qpython/BTagging/CMSSW_7_4_8/src/RecoBTag/PerformanceMeasurements/test/BTagAnalyzerMacros/CF_hist.root")

# vector of histo names
histnames = []
rootkeys = inputFileName.GetListOfKeys()
for key in rootkeys:
    histnames.append(key.GetName())
#    print histnames

print "List of all the histograms in the root file:" 
print histnames , "\n\n"
    
# vector of systematic "value"
systematic=["up","central","down"]

# Working point and Flavour
WP=-99
Flavour=-99
histname_trunc="hist"


# loop over all histograms -> loop over WP and Flavour
for hist_index in range(0,len(histnames)-1):
    testhist=inputFileName.Get(histnames[hist_index])


    # get the right flavour
    if "_b_0" in histnames[hist_index]:
        Flavour = 0
    elif "_c_0" in histnames[hist_index]:
        Flavour = 1 
    elif "_l_0"in histnames[hist_index]:
        Flavour = 2
    else:
        print "SOMETHING WENT WRONG"

    # get the right working point
    if "csvl" in histnames[hist_index]:
        WP = 0
    elif "csvm" in histnames[hist_index]:
        WP = 1
    elif "csvt" in histnames[hist_index]:
        WP = 2
    else:
        print "SOMETHING WENT WRONG"
    

    # splitting in the 3 available systematic "value" (up, central, down)
    for syst_n in range(0,len(systematic)):
        local_hist=testhist.Clone("systematic[syst_n]")
        print "systematic value is " , systematic[syst_n]
        temp_hist=testhist.Clone("systematic[syst_n]")

        # Loop over bin to create up and down systematics
        for bin_n in range (1,temp_hist.GetNbinsX()):
            if (systematic[syst_n]== "up"):
                local_hist.SetBinContent(bin_n, temp_hist.GetBinContent(bin_n)+temp_hist.GetBinError(bin_n))
            elif (systematic[syst_n]== "central"):
                if (False):
                    print "central!! -> do nothing"
            elif (systematic[syst_n]== "down"):
                local_hist.SetBinContent(bin_n, temp_hist.GetBinContent(bin_n)-temp_hist.GetBinError(bin_n))
            else:
                print "SOMETHING WENT WRONG"
            print "Bin content is ", local_hist.GetBinContent(bin_n)
    
        # this you need to do for every histogram:
        params = ROOT.BTagEntry.Parameters(
        WP, # 0 means loose
        "fastSim", # type of measurement 
        systematic[syst_n], # systematic
        Flavour, # 0 means b-flavor
        -2.4, 2.4, 
        20, 800, 
        0, 1,
        )
        entry = ROOT.BTagEntry(
        local_hist,
        params
        )
        calib.addEntry(entry)
        

# when you are done adding the entries
with open('CSV_13TEV_MC_25_09_2015.csv', 'w') as f:
    f.write(calib.makeCSV())
