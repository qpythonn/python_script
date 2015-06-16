import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        # first option is either h (for help) or i (for input file), second is o (output file)
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print "bad options!! Syntax is ..."
        print 'testOptions.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
            
if __name__ == "__main__":
    main(sys.argv[1:])

print sys.argv

print "sys.argv[2] is " ,sys.argv[2] 

if (len(sys.argv) > 1): 
    if not (sys.argv[1] == ""):
        print "arg is ", sys.argv[1]

