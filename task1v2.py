#tcpdump -r eth1_eth2_20110207003505 'icmp' -w outfile.pcap




import subprocess as sp
import os

numberDict = {400:0}
nameDict = {"":0}
newFileName = "outputfiles/output"


def filterPackets(filename, newFileName,i):
    p = sp.Popen(('tcpdump', '-r', "./traffic/" + filename, 'icmp', '-w', newFileName+str(i)), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        print row


#checks if an IP is local
def isLocal(ip):
    if ip[0:7] == "192.168" or ip[0:3] == "10.":
        return True
    else:
        return False


def extractTypeAndCode(filename):
    #ipsumdump -r --src --icmp-type --icmp-code --icmp-type-name --icmp-code-name outfile.pcap
    p = sp.Popen(('ipsumdump', '-r', '--src', '--dst', '--icmp-type', '--icmp-code', '--icmp-type-name', '--icmp-code-name',"outputfiles/"+filename), stdout=sp.PIPE)

    for row in iter(p.stdout.readline, b''):
        #split into seperate parts
        splitted = row.split()

        if len(splitted) == 6:
            #get source & dest
            source = splitted[0]
            dest = splitted[1]

            # here we filter out local traffic by removing any errors involving 192.168.x.x and 10.x.x.x IP's
            if (isLocal(source) and not isLocal(dest)) or (not isLocal(source) and isLocal(dest)):

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







def main():
    index = 0
    # read input and write to new files
    for f in os.listdir("./traffic"):
        filterPackets(f, "outputfiles/output", index)
        index += 1
    # read new output
    for k in os.listdir("./outputfiles"):
        extractTypeAndCode(k)

    del nameDict[""]
    del numberDict[400]

    for item in nameDict:
        print item + " : " + str(nameDict[item])

    for item in numberDict:
        print item + " : " + str(numberDict[item])

if __name__ == '__main__':
    main()