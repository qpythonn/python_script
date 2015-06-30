# This script will count the number of events per dataset for a list of datasets.
# There is two distinct use cases:
# i) You already have a list of datasets for which you want to know the number of events of.
# Syntax example: "python count_events.py - i my_file.txt"  where my_file.txt is a file without any empty lines.
# ii) You do not have a list of datasets. In that case, a list of datasets that matches a das querry will be created by the script.
# Syntax example: "python count_events.py -q /*TTbar_13/*7_4_3-*/GEN-SIM-RECO"

import sys, getopt
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT


# Option to give an list of dataset as argument
def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:q",["ifile=","qquerry="])
    except getopt.GetoptError:
        print "Bad options! Use either ..."
        print "count_events.py -i <inputfile> or"
        print "count_events.py -q <querry>"
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
        elif opt in ("-q","qquerry"):
            querry = arg
            print "querry is ", querry
if __name__ == "__main__":
    main(sys.argv[1:])
    

if (len(sys.argv) == 5):
    print "too many arguments!"
    print "Use either ..."
    print "count_events.py -i <inputfile> or"
    print "count_events.py -q <querry>"
    sys.exit(2)

# Setting up
dbsCmd = "cd /cvmfs/cms.cern.ch/slc5_amd64_gcc462/cms/cmssw/CMSSW_6_0_1/src; eval `scramv1 runtime -sh`;"
pExe = Popen(dbsCmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)


# create a file if the -q option was used
if (len(sys.argv) > 1):
    if (sys.argv[1] == "-q"):
        querry=sys.argv[2]
        # Crate a text file with the list of dataset you want to get the number of events of
        f0 = open('querry_samples.txt', 'w')
        dbsCmd0 = "das_client.py --query='dataset="+querry+"' --limit=0"
        print "All the dataset that matches 'das_client.py --query='dataset="+querry+"' --limit=0' will be listed!"
        fetchsamples = Popen(dbsCmd0, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        # writte the list of dataset in the txt file
        for row in fetchsamples.stdout:
            if not (row.startswith("Showing")):
                f0.write(row)
        f0.close()
    


datasets = []

# Text file containing the list of dataset is by default the one produced by the DAS querry
f = open('querry_samples.txt', 'r')   

# overwritte the default file if a file was given using the -i option
if (len(sys.argv) > 1):
    if (sys.argv[1] == "-i"):
        f = open(sys.argv[2], 'r')
        print "overwritting default input file argument!"


for dataset in f:
    # for each dataset declare a array that contains one entry per file, filled with the number of event for that file
    numbers = []
    # remove empty line (/n)
    dataset_clean = dataset[:-1]
    datasets.append(dataset_clean)
    dbsCmd1 = "das_client.py --query='file dataset=" + dataset_clean  +   " | grep file.nevents' --limit=0"
    list = Popen(dbsCmd1, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    
    for line in list.stdout:
        if not (line.startswith("Showing")):
            linestr_clean = str(line)
            linestr_clean = linestr_clean[:-1]

        if not (linestr_clean == ""):
            number  = int(linestr_clean)
            numbers.append(number)
#        print numbers
    print "The total number of events in the dataset " + dataset_clean +   " = " + str(sum(numbers))

