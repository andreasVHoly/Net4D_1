#VHLAND002
#python file for task 2
#Bandwidth usage

import subprocess as sp
import os
import task1v2 as t1

day1Dict = {"",0}
day2Dict = {"",0}
day3Dict = {"",0}
day4Dict = {"",0}
day5Dict = {"",0}
day6Dict = {"",0}
day7Dict = {"",0}


def decodeName(filename):
    year = filename[10:14]
    month = filename[14:16]
    day = filename[16:18]
    hour = filename[18:20]
    minute = filename[20:22]
    second = filename[22:24]


sourceDest = []
#$ ipsumdump -s -d -r traffic/eth1_eth2_20110207201002

def readInPackets(filename):
    p = sp.Popen(('ipsumdump', '-s', '-d', '-r', "traffic/eth1_eth2_20110207201002"), stdout=sp.PIPE)
    count = 0
    for row in iter(p.stdout.readline, b''):
        splitter = row.split()
        source = splitter[0]
        dest = splitter[1]
        tempArray = [source,dest,0]
        sourceDest.append(tempArray)
        # here we filter out local traffic by removing any errors involving 192.168.x.x and 10.x.x.x IP's
        #if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):
        count += 1
    print count


def analizeFile(filename):
    #determine if it is an incoming connection or outgoing
        #if the source is a non-local ip then it is incoming
    p = sp.Popen(('tcpstat', '-r', "traffic/eth1_eth2_20110207201002"), stdout=sp.PIPE)
    count = 0
    for row in iter(p.stdout.readline, b''):
        #Time:1297105805	n=2	avg=124.50	stddev=44.50	bps=398.40
        splitter = row.split()
        num = ""
        for letter in splitter[1]:
            if letter.isdigit():
                num += letter
        count += int(num)
    print count





#delete inits
# del day1Dict[""]
# del day2Dict[""]
# del day3Dict[""]
# del day4Dict[""]
# del day5Dict[""]
# del day6Dict[""]
# del day7Dict[""]
#readInPackets("")
#analizeFile("")
# for i in sourceDest:
#     print i
#print len(sourceDest)
count = 0
print "********************bits**********************"
p = sp.Popen(('tcpstat', '-o', '%b','-r', "traffic/eth1_eth2_20110207201002"), stdout=sp.PIPE)
for row in iter(p.stdout.readline, b''):
    splitd = row.split(".")
    total = 0
    #print splitd
    for i in splitd:
        total += int(i)
    print "total bps: " + str(total)
    print "bph: " + str(total/3600)
    print "kbph: " + str(total/3600/1024)
    print "mbph: " + str(total/3600/1024/1024)
print "********************bytes**********************"
p = sp.Popen(('tcpstat', '-o', '%B','-r', "traffic/eth1_eth2_20110207201002"), stdout=sp.PIPE)
for row in iter(p.stdout.readline, b''):
    splitd = row.split(".")
    total = 0
    #print splitd
    for i in splitd:
        total += int(i)
    print "total bps: " + str(total)
    print "bph: " + str(total/3600)
    print "kbph: " + str(total/3600/1024)
    print "mbph: " + str(total/3600/1024/1024)















