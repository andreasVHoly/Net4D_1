#tcpdump -r eth1_eth2_20110207003505 'icmp' -w outfile.pcap




import subprocess as sp
import os

numberDict = {400:0}
nameDict = {"":0}
newFileName = "outputfiles/output"

def filterPackets(filename,i):
    p = sp.Popen(('tcpdump', '-r', "traffic/" + filename, 'icmp', '-w', newFileName+str(i)), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        print row

def extractTypeAndCode(filename):
    #ipsumdump -r --src --icmp-type --icmp-code --icmp-type-name --icmp-code-name outfile.pcap
    p = sp.Popen(('ipsumdump', '-r', '--src', '--dst', '--icmp-type', '--icmp-code', '--icmp-type-name', '--icmp-code-name',"outputfiles/"+filename), stdout=sp.PIPE)

    for row in iter(p.stdout.readline, b''):
        #print row.rstrip()
        #split into seperate parts
        splitted = row.split()

        if len(splitted) == 6:

             # here we filter out local traffic by removing any errors involving 192.168.x.x and 10.x.x.x IP's
            if (splitted[0][0:7] != "192.168" and splitted[0][0:3] != "10.") or (splitted[1][0:7] != "192.168" and splitted[1][0:3] != "10."):

                #add into dictionary if new and increment count if not
                message = str(splitted[2]) + "," + str(splitted[3])

                if numberDict.has_key(message):
                    numberDict[message] += 1
                else:
                    numberDict[message] = 1

                message = str(splitted[4]) + " " + str(splitted[5])

                if nameDict.has_key(message):
                    nameDict[message] += 1
                else:
                    nameDict[message] = 1




index = 0
for f in os.listdir("./traffic"):
    filterPackets(f,index)
    index += 1

for k in os.listdir("./outputfiles"):
    extractTypeAndCode(k)

del nameDict[""]
del numberDict[400]
for item in nameDict:
    print item + " : " + str(nameDict[item])

for item in numberDict:
    print item + " : " + str(numberDict[item])