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
        opts, args = getopt.getopt(argv,"hi:p",["ifile=","ppatern"])
    except getopt.GetoptError:
        print "bad option(s)!! Syntax is ..."
        print 'count_events.py -i <inputfile> -p <patern>' 
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "calling for help!"
            print 'parsingScript.py -i <inputfile> '
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            if (inputfile != ""):
                print "The input file is '",inputfile,"'."
        elif opt in ("-p", "--ppatern"):
             patern= arg
             if (patern != ""):
                print "The split pattern is '", patern,"'."
if __name__ == "__main__":
    main(sys.argv[1:])




if (len(sys.argv) > 1):
    if not (sys.argv[2] == ""):
        # load file
        f = open(sys.argv[2], 'r')
        
        split_pattern=(sys.argv[4])
                       
        for line in f:
            p1=line.split(split_pattern,1)
            print p1[0]
            
        
    
