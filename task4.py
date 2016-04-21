#VHLAND002
#python file for task 4
#http trafiic


import subprocess as sp
import operator


import task1v2 as t1


domains = {"":0}

def runCommand():
    p = sp.Popen(('httpry', '-r', 'traffic/eth1_eth2_20110207201002'),stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        splitter = row.split()
        #we are only looking at get's
        #print splitter
        if splitter[5] == "GET":
            #need to loook at 5
            #print splitter[6]
            domain = ""
            count = 0
            #print len(splitter[6])-1
            for i in range(len(splitter[6])-1,-1,-1):
                #print splitter[6][i]
                if splitter[6][i] == "." and count == 0:
                    count += 1
                    domain = splitter[6][i] + domain
                elif splitter[6][i] == "." and count == 1:
                    break
                else:
                    domain = splitter[6][i] + domain
            domain = "*." + domain
            #print domain
            if domains.has_key(domain):
                domains[domain] += 1
            else:
                domains[domain] = 1



runCommand()
del domains[""]


# for item in domains:
#     print item + " : " + str(domains[item])

sorted_UDPIn = sorted(domains.items(), key=operator.itemgetter(1))


for i in range(len(sorted_UDPIn)-1,len(sorted_UDPIn)-10,-1):
    print sorted_UDPIn[i]



def main():
    readinPortFile()
    for f in os.listdir("./traffic"):
        runIpSumDump(f)

    # remove inits
    del TCPIncoming[""]
    del TCPOutgoing[""]
    del UDPOutgoing[""]
    del UDPIncoming[""]
    writeToFile("task3output.txt")

if __name__ == '__main__':
    main()