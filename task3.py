#VHLAND002
#python file for task 3
#Traffic by bytes for each port

import subprocess as sp
import operator
import task1v2 as t1
import os

UDPPorts = {"":""}
TCPPorts = {"":""}
UDPIncoming = {"":0}
UDPOutgoing = {"":0}
TCPIncoming = {"":0}
TCPOutgoing = {"":0}

def readinPortFile():
    f = open("services", "r")
    for line in f:
        #read in port line & split
        splitter = line.split()
        #if valid line
        if len(splitter) > 0:
            #assign port based on protocol
            port = splitter[1][0:-4]
            protocol = splitter[1][-3:]
            if protocol == "tcp":
                #for name ref
                TCPPorts[port] = splitter[0]
                # for counting
                TCPIncoming[port] = 0
                TCPOutgoing[port] = 0
            elif protocol == "udp":
                #for name ref
                UDPPorts[port] = splitter[0]
                #for counting
                UDPIncoming[port] = 0
                UDPOutgoing[port] = 0

    #assign uncategorised category
    UDPIncoming["uncat"] = 0
    UDPOutgoing["uncat"] = 0
    TCPIncoming["uncat"] = 0
    TCPOutgoing["uncat"] = 0
    UDPPorts["uncat"] = "uncategorised UDP ports"
    TCPPorts["uncat"] = "uncategorised TCP ports"


def runIpSumDump(filename):
    #type, source ip, dest ip, source port, dest port, size
    print "trying to read " + filename
    p = sp.Popen(('ipsumdump', '-p', '-s', '-d', '-S', '-D', '-L', '-r', filename), stdout=sp.PIPE)
    #iterate over output
    for row in iter(p.stdout.readline, b''):
        #split line
        splitted = row.split()
        #ensure we have apcket information
        if len(splitted) == 6:
            #filter out local traffic
            source = splitted[1]
            dest = splitted[2]
            if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):
                #if we have a tcp connection
                if splitted[0] == "T":
                    #get values
                    keyOut = splitted[3]
                    keyIn = splitted[4]
                    count = int(splitted[5])
                    #incoming connection
                    if keyIn in TCPIncoming:
                        TCPIncoming[keyIn] += count
                    else:
                        TCPIncoming["uncat"] += count
                    #outgoing connection
                    if keyOut in TCPOutgoing:
                        TCPOutgoing[keyOut] += count
                    else:
                        TCPOutgoing["uncat"] += count


                #if we have a udp connection
                elif splitted[0] == "U":
                    #get values
                    keyOut = splitted[3]
                    keyIn = splitted[4]
                    count = int(splitted[5])
                    # incoming connection
                    if keyIn in UDPIncoming:
                        UDPIncoming[keyIn] += count
                    else:
                        UDPIncoming["uncat"] += count
                    # outgoing connection
                    if keyOut in UDPOutgoing:
                        UDPOutgoing[keyOut] += count
                    else:
                        UDPOutgoing["uncat"] += count

def writeToFile(filename):
    # sort dictionaries
    sorted_TCPOut = sorted(TCPOutgoing.items(), key=operator.itemgetter(1))
    sorted_TCPIn = sorted(TCPIncoming.items(), key=operator.itemgetter(1))
    sorted_UDPOut = sorted(UDPOutgoing.items(), key=operator.itemgetter(1))
    sorted_UDPIn = sorted(UDPIncoming.items(), key=operator.itemgetter(1))
    #create file for output
    f = file(filename, "w")
    csvf = open("task3csv.csv", "w")

    csvf.write("TCP Outbound ports\n")
    csvf.write("Port,Count\n")
    f.write("Outbound TCP Ports (port name/port number : bytes)\n")
    print "Outbound TCP Ports (port name/port number : bytes)"
    for i in range(len(sorted_TCPOut) - 1, len(sorted_TCPOut) - 10, -1):
        f.write(TCPPorts[sorted_TCPOut[i][0]] + "/" + sorted_TCPOut[i][0] + " \t: " + str(sorted_TCPOut[i][1]) + "\n")
        print TCPPorts[sorted_TCPOut[i][0]] + "/" + sorted_TCPOut[i][0] + " \t: " + str(sorted_TCPOut[i][1])
        csvf.write(TCPPorts[sorted_TCPOut[i][0]] + "," + str(sorted_TCPOut[i][1])+"\n")

    csvf.write("\nTCP Inbound ports\n")
    csvf.write("Port,Count\n")
    f.write("\nOutbound TCP Ports (port name/port number : bytes)\n")
    print "\nOutbound TCP Ports (port name/port number : bytes)"
    for i in range(len(sorted_TCPIn) - 1, len(sorted_TCPIn) - 10, -1):
        f.write(TCPPorts[sorted_TCPIn[i][0]] + "/" + sorted_TCPIn[i][0] + " \t: " + str(sorted_TCPIn[i][1]) + "\n")
        print TCPPorts[sorted_TCPIn[i][0]] + "/" + sorted_TCPIn[i][0] + " \t: " + str(sorted_TCPIn[i][1])
        csvf.write(TCPPorts[sorted_TCPIn[i][0]] + "," + str(sorted_TCPIn[i][1])+"\n")

    csvf.write("\nUDP outbound ports\n")
    csvf.write("Port,Count\n")
    f.write("\nOutbound TCP Ports (port name/port number : bytes)\n")
    print "\nOutbound TCP Ports (port name/port number : bytes)"
    for i in range(len(sorted_UDPOut) - 1, len(sorted_UDPOut) - 10, -1):
        f.write(UDPPorts[sorted_UDPOut[i][0]] + "/" + sorted_UDPOut[i][0] + " \t: " + str(sorted_UDPOut[i][1]) + "\n")
        print UDPPorts[sorted_UDPOut[i][0]] + "/" + sorted_UDPOut[i][0] + " \t: " + str(sorted_UDPOut[i][1])
        csvf.write(UDPPorts[sorted_UDPOut[i][0]] + "," + str(sorted_UDPOut[i][1])+"\n")

    csvf.write("\nUDP Inbound ports\n")
    csvf.write("Port,Count\n")
    f.write("\nOutbound TCP Ports (port name/port number : bytes)\n")
    print "\nOutbound TCP Ports (port name/port number : bytes)"
    for i in range(len(sorted_UDPIn) - 1, len(sorted_UDPIn) - 10, -1):
        f.write(UDPPorts[sorted_UDPIn[i][0]] + "/" + sorted_UDPIn[i][0] + " \t: " + str(sorted_UDPIn[i][1]) + "\n")
        print UDPPorts[sorted_UDPIn[i][0]] + "/" + sorted_UDPIn[i][0] + " \t: " + str(sorted_UDPIn[i][1])
        csvf.write(UDPPorts[sorted_UDPIn[i][0]] + "," + str(sorted_UDPIn[i][1])+"\n")

    f.close()
    csvf.close()



def main():
    readinPortFile()
    fileDirs = t1.readDir()
    #run over files
    for fle in fileDirs:
        print fle
        runIpSumDump(fle)

    # remove inits
    del TCPIncoming[""]
    del TCPOutgoing[""]
    del UDPOutgoing[""]
    del UDPIncoming[""]
    writeToFile("task3output.txt")

if __name__ == '__main__':
    main()


