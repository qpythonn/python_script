import getopt
import sys
import string


raw_input="bla and bl0 /dataset/dd/dd/ = 10"


# x.split('separator',nofSeparation)
# split string "x" in a vector of string.
split_input=raw_input.split('bl0 ', 1)
print split_input


# load file
f = open('/user/qpython/TopBrussels7X/CMSSW_7_4_2/src/TopBrussels/DisplacedTops/scripts/output2_First10.txt', 'r')

for line in f:
    print line
    
    raw=line

    p1=raw.split("dataset ",1)
    p2=p1[1].split(" = ",1)
    p3=p2[0].split("/", 3)
#    print p3

    dataset=p3[1]
    nEvents=p2[1]
    
    print dataset
    print nEvents
    
    
