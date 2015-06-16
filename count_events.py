# This script will count the number of events per dataset for a list of datasets.
# Either you already have a list of dataset and you run count_events.py -i <yourfile>. Your file should not contain empty lines!
# If not a list of dataset will be created by making a DAS querry.

import sys, getopt
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT

#print "There is no input file, the list of dataset will be created by the das querry..."

# Option to give an list of dataset as argument
def main(argv):
    inputfile = ''
    try:
#        opts, args = getopt.getopt(argv,"hi:q",["ifile=","qquerry="])
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print "bad option(s)!! Syntax is ..."
        print 'count_events.py -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "calling for help!"
            print 'count_events.py -i <inputfile> '
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            if (inputfile != ""):
                print "The input file is '",inputfile,"'."
#        elif opt in ("-q","qquerry"):
#            querry = arg
#            print "querry is ", querry
if __name__ == "__main__":
    main(sys.argv[1:])
    


# Setting up
dbsCmd = "cd /cvmfs/cms.cern.ch/slc5_amd64_gcc462/cms/cmssw/CMSSW_6_0_1/src; eval `scramv1 runtime -sh`;"
pExe = Popen(dbsCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)


# Single dataset example
#dataset = "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaledown-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"
#dbsCmd1 = "das_client.py --query='file dataset=/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaledown-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM | grep file.nevents'"


# create a file only if not provided in the argument
if (len(sys.argv) == 1):
    # Crate a text file with the list of dataset you want to get the number of events of
    f0 = open('DR74_samples.txt', 'w')
    dbsCmd0 = "das_client.py --query='dataset=/*/*DR74*/MINIAODSIM' --limit=0"
    print "All the dataset that matches 'das_client.py --query='dataset=/*/*DR74*/MINIAODSIM' --limit=0' will be listed!"
    fetchsamples = Popen(dbsCmd0, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    # writte the list of dataset in the txt file
    for row in fetchsamples.stdout:
        if not (row.startswith("Showing")):
            f0.write(row)
    


datasets = []

# Text file containing the list of dataset is by default the one produced by the DAS querry
f = open('DR74_samples.txt', 'r')   

# overwritte only if the file was provided in the argument
if (len(sys.argv) > 1):
    if not (sys.argv[2] == ""):
        f = open(sys.argv[2], 'r')
        print "overwritting default input file argument!"


for dataset in f:
    # for each dataset declare a array that contains one entry per file, filled with the number of event for that file
    numbers = []
    # remove empty line (/n)
    dataset_clean = dataset[:-1]
    datasets.append(dataset_clean)
    dbsCmd1 = "das_client.py --query='file dataset=" + dataset_clean  +   " | grep file.nevents'"
    list = Popen(dbsCmd1, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    
    for line in list.stdout:
        if not (line.startswith("Showing")):
            linestr_clean = str(line)
            linestr_clean = linestr_clean[:-1]

        if not (linestr_clean == ""):
            number  = int(linestr_clean)
            numbers.append(number)

    print "The total number of events in the dataset " + dataset_clean +   " = " + str(sum(numbers))

