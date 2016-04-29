#tcpdump -r eth1_eth2_20110207003505 'icmp' -w outfile.pcap




import subprocess as sp
import os

numberDict = {400:0}
nameDict = {"":0}
outputNames = []


def filterPackets(filename, newFileName):
    p = sp.Popen(('tcpdump', '-r', filename, 'icmp', '-w', newFileName), stdout=sp.PIPE)
    outputNames.append(newFileName)
    for row in iter(p.stdout.readline, b''):
        print "filtering..."


#checks if an IP is local
def isLocal(ip):
    if ip[0:7] == "192.168" or ip[0:3] == "10.":
        return True
    else:
        return False


def extractTypeAndCode(filename):
    #ipsumdump -r --src --icmp-type --icmp-code --icmp-type-name --icmp-code-name outfile.pcap
    p = sp.Popen(('ipsumdump', '-r', '--src', '--dst', '--icmp-type', '--icmp-code', '--icmp-type-name', '--icmp-code-name', filename), stdout=sp.PIPE)

    for row in iter(p.stdout.readline, b''):
        # split into seperate parts
        splitted = row.split()

        if len(splitted) == 6:
            # get source & dest
            source = splitted[0]
            dest = splitted[1]

            # here we filter out local traffic by removing any ip's involving 192.168.x.x and 10.x.x.x IP's
            if (isLocal(source) and not isLocal(dest)) or (not isLocal(source) and isLocal(dest)):
                # add into dictionary if new and increment count if not
                message = str(splitted[2]) + "," + str(splitted[3])

                if message in numberDict:
                    numberDict[message] += 1
                else:
                    numberDict[message] = 1

                message2 = str(splitted[4]) + " " + str(splitted[5])

                if message2 in nameDict:
                    nameDict[message2] += 1
                else:
                    nameDict[message2] = 1




def readDir():
    fileDirs = []

    # read in files from directory
    for f in os.listdir("traffic/"):
        print "found: " + f
        if os.path.isfile(os.path.join("traffic/", f)):
            fileDirs.append(os.path.join("traffic/", f))

    print str(len(fileDirs)) + " files found"
    return fileDirs


def writeOutput(filename):
    # delete inits
    del nameDict[""]
    del numberDict[400]
    f = file(filename, "w")

    for item in nameDict:
        print item + " : " + str(nameDict[item])
        f.write(item + " : " + str(nameDict[item]) + "\n")

    for item2 in numberDict:
        print item2 + " : " + str(numberDict[item2])
        f.write(item2 + " : " + str(numberDict[item2]) + "\n")
    f.close()


def main():
    index = 0
    # read input and write to new files
    fileDirs = readDir()
    for f in fileDirs:
        filterPackets(f, "outputfiles/output"+str(index))
        index += 1
    # read new output
    for k in outputNames:
        extractTypeAndCode(k)

    writeOutput("task1output.txt")


if __name__ == '__main__':
    main()