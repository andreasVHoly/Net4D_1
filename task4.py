#VHLAND002
#python file for task 4
#http trafiic


import subprocess as sp
import operator


import task1v2 as t1


domains = {"":0}

def runCommand(filename):
    #run command
    print "trying to read file: " + filename
    p = sp.Popen(('httpry', '-r', filename), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        splitter = row.split()
        #print splitter
        # we are only looking at get's
        if splitter[5] == "GET":
            domain = ""
            count = 0
            # we start from the back looking for .
            for i in range(len(splitter[6])-1, -1, -1):
                if splitter[6][i] == "." and count == 0:
                    count += 1
                    domain = splitter[6][i] + domain
                elif splitter[6][i] == "." and count == 1:
                    break
                else:
                    domain = splitter[6][i] + domain
            domain = "*." + domain
            if domain in domains:
                domains[domain] += 1
            else:
                domains[domain] = 1



def cleanDomains():
    sortedDomain = sorted(domains.items(), key=operator.itemgetter(1))

    for i in range(len(sortedDomain) - 1, len(sortedDomain) - 10, -1):
        print sortedDomain[i]



def main():
    filedirs = t1.readDir()
    for f in filedirs:
        runCommand(f)
    del domains[""]
    #sort domain
    cleanDomains()

if __name__ == '__main__':
    main()