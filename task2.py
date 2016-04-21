#VHLAND002
#python file for task 2
#Bandwidth usage

import subprocess as sp
import os
import task1v2 as t1
import datetime
import operator

day1Dict = {"",0}
day2Dict = {"",0}
day3Dict = {"",0}
day4Dict = {"",0}
day5Dict = {"",0}
day6Dict = {"",0}
day7Dict = {"",0}


outgoing = {"":0}
incoming = {"":0}



def decodeName(filename):
    buf = 8
    year = filename[10+buf:14+buf]
    month = filename[14+buf:16+buf]
    day = filename[16+buf:18+buf]
    hour = filename[18+buf:20+buf]
    minute = filename[20+buf:22+buf]
    second = filename[22+buf:24+buf]
    print year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second


sourceDest = []
#$ ipsumdump -s -d -r traffic/eth1_eth2_20110207201002

def readInPackets(filename):
    p = sp.Popen(('ipsumdump', '-t', '-s', '-d', '--wire-length', '-r', "traffic/eth1_eth2_20110207201002"), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        splitter = row.split()

        if len(splitter) < 4:
            continue
        source = splitter[1]
        dest = splitter[2]
        # check for local traffic
        if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):

            #format time
            time = datetime.datetime.fromtimestamp(float(splitter[0])).strftime('%Y-%m-%d %H:%M:%S')


            #print "time " + str(time)

            if str(time) not in outgoing:
                outgoing[str(time)] = 0
            if str(time) not in incoming:
                incoming[str(time)] = 0



            # check if outgoing or incoming connection
            if t1.isLocal(source):
                # means outgoing
                if str(time) in outgoing:
                    outgoing[str(time)] += int(splitter[3])
            elif t1.isLocal(dest):
                #means incoming
                if str(time) in incoming:
                    incoming[str(time)] += int(splitter[3])







#delete inits
# del day1Dict[""]
# del day2Dict[""]
# del day3Dict[""]
# del day4Dict[""]
# del day5Dict[""]
# del day6Dict[""]
# del day7Dict[""]

def main():
    filedirs = t1.readDir()
    ipsumdumpappr = True
    tcpstatappr = False
    for f in filedirs:
        if tcpstatappr:
            decodeName(f)
            getBits(f)
            getBytes(f)
            break
        elif ipsumdumpappr:
            readInPackets(f)
            break

    sortedKeys = incoming.keys()
    sortedKeys.sort()
    #sortedincoming = sorted(incoming.keys(), key=operator.itemgetter(1))
    for i in sortedKeys:
         print str(i) + "\t incoming: " + str(incoming[str(i)]) + "bps\t outgoing: " + str(outgoing[str(i)]) + "bps"









def getBytes(filename):
    print "********************bytes**********************"
    p = sp.Popen(('tcpstat', '-o', '%B', '-r', filename), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        splitd = row.split(".")
        total = 0
        for i in splitd:
            total += int(i)
        print "::::per sec::::"
        print "total bps: " + str(total)
        print "kbps: " + str(total / 1024)
        print "mbps: " + str(total / 1024 / 1024)
        print "::::per min::::"
        print "bpm: " + str(total * 60)
        print "kbpm: " + str(total * 60 / 1024)
        print "mbpm: " + str(total * 60 / 1024 / 1024)
        print "::::per hr ::::"
        print "bph: " + str(total * 3600)
        print "kbph: " + str(total * 3600 / 1024)
        print "mbph: " + str(total * 3600 / 1024 / 1024)



def getBits(filename):
    print "********************bits**********************"
    p = sp.Popen(('tcpstat', '-o', '%b', '-r', filename), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        splitd = row.split(".")
        total = 0
        for i in splitd:
            total += int(i)
        print "::::per sec::::"
        print "total bps: " + str(total)
        print "kbps: " + str(total * 1024)
        print "mbps: " + str(total * 1024 / 1024)
        print "::::per min::::"
        print "bpm: " + str(total * 60)
        print "kbpm: " + str(total * 60 / 1024)
        print "mbpm: " + str(total * 60 / 1024 / 1024)
        print "::::per hr ::::"
        print "bph: " + str(total * 3600)
        print "kbph: " + str(total * 3600 / 1024)
        print "mbph: " + str(total * 3600 / 1024 / 1024)



if __name__ == '__main__':
    main()