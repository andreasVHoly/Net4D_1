#VHLAND002
#python file for task 3
#Traffic by bytes for each port

import subprocess as sp
import operator
import task1 as t1
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


def basicCommand(filename):
    print "read file " + filename
    p = sp.Popen(('ipsumdump', '-p','-s', '-d', '-D', '-L', '-r', filename), stdout=sp.PIPE)
    # iterate over output
    for row in iter(p.stdout.readline, b''):
        # split line
        splitted = row.split()
        if splitted[0] == "T":
            # get values
            source = splitted[1]
            dest = splitted[2]
            if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):
                key = splitted[3]

                count = int(splitted[4])
                # incoming connection
                if key in TCPIncoming:
                    TCPIncoming[key] += count
                else:
                    TCPIncoming["uncat"] += count



        # if we have a udp connection
        elif splitted[0] == "U":
            # get values
            source = splitted[1]
            dest = splitted[2]
            if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):
                # if we have a tcp connection
                key = splitted[3]
                count = int(splitted[4])
                # incoming connection
                if key in UDPIncoming:
                    UDPIncoming[key] += count
                else:
                    UDPIncoming["uncat"] += count


def runIpSumDump(filename):
    #type, source ip, dest ip, source port, dest port, size
    print "read file " + filename
    p = sp.Popen(('ipsumdump', '-p', '-s', '-d', '-S', '-D', '-L', '-r', filename), stdout=sp.PIPE)
    #iterate over output
    for row in iter(p.stdout.readline, b''):
        #split line
        splitted = row.split()
        #ensure we have apcket information
        #if len(splitted) == 6:
        #filter out local traffic



        if splitted[0] == "T":
            # get values
            source = splitted[1]
            dest = splitted[2]
            if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):
                keyOut = splitted[3]
                keyIn = splitted[4]
                count = int(splitted[5])
                # incoming connection
                if keyIn in TCPIncoming:
                    TCPIncoming[keyIn] += count
                else:
                    TCPIncoming["uncat"] += count
                # outgoing connection
                if keyOut in TCPOutgoing:
                    TCPOutgoing[keyOut] += count
                else:
                    TCPOutgoing["uncat"] += count


        # if we have a udp connection
        elif splitted[0] == "U":
            # get values
            source = splitted[1]
            dest = splitted[2]
            if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):
            # if we have a tcp connection
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
    # f.write("Outbound TCP Ports (port name/port number : bytes)\n")
    # print "Outbound TCP Ports (port name/port number : bytes)"
    for i in range(len(sorted_TCPOut) - 1, len(sorted_TCPOut) - 12, -1):
        #f.write(TCPPorts[sorted_TCPOut[i][0]] + "/" + sorted_TCPOut[i][0] + " \t: " + str(sorted_TCPOut[i][1]) + "\n")
        #print TCPPorts[sorted_TCPOut[i][0]] + "/" + sorted_TCPOut[i][0] + " \t: " + str(sorted_TCPOut[i][1])
        csvf.write(TCPPorts[sorted_TCPOut[i][0]] + "," + str(sorted_TCPOut[i][1])+"\n")
    othertcpout = 0
    for i in range(0, len(sorted_TCPOut) - 11):
        othertcpout += sorted_TCPOut[i][1]
        # print UDPPorts[sorted_UDPIn[i][0]] + "/" + sorted_UDPIn[i][0] + " \t: " + str(sorted_UDPIn[i][1])
    csvf.write("Other," + str(othertcpout) + "\n")

    csvf.write("\nTCP Inbound ports\n")
    csvf.write("Port,Count\n")
    # f.write("\nOutbound TCP Ports (port name/port number : bytes)\n")
    # print "\nOutbound TCP Ports (port name/port number : bytes)"
    for i in range(len(sorted_TCPIn) - 1, len(sorted_TCPIn) - 12, -1):
        #f.write(TCPPorts[sorted_TCPIn[i][0]] + "/" + sorted_TCPIn[i][0] + " \t: " + str(sorted_TCPIn[i][1]) + "\n")
        #print TCPPorts[sorted_TCPIn[i][0]] + "/" + sorted_TCPIn[i][0] + " \t: " + str(sorted_TCPIn[i][1])
        csvf.write(TCPPorts[sorted_TCPIn[i][0]] + "," + str(sorted_TCPIn[i][1])+"\n")
    othertcpin = 0
    for i in range(0, len(sorted_TCPIn) - 11):
        othertcpin += sorted_TCPIn[i][1]
        # print UDPPorts[sorted_UDPIn[i][0]] + "/" + sorted_UDPIn[i][0] + " \t: " + str(sorted_UDPIn[i][1])
    csvf.write("Other," + str(othertcpin) + "\n")


    csvf.write("\nUDP outbound ports\n")
    csvf.write("Port,Count\n")
    #f.write("\nOutbound TCP Ports (port name/port number : bytes)\n")
    #print "\nOutbound TCP Ports (port name/port number : bytes)"
    for i in range(len(sorted_UDPOut) - 1, len(sorted_UDPOut) - 12, -1):
        #f.write(UDPPorts[sorted_UDPOut[i][0]] + "/" + sorted_UDPOut[i][0] + " \t: " + str(sorted_UDPOut[i][1]) + "\n")
        #print UDPPorts[sorted_UDPOut[i][0]] + "/" + sorted_UDPOut[i][0] + " \t: " + str(sorted_UDPOut[i][1])
        csvf.write(UDPPorts[sorted_UDPOut[i][0]] + "," + str(sorted_UDPOut[i][1])+"\n")
    otherudpout = 0
    for i in range(0, len(sorted_UDPOut) - 11):
        otherudpout += sorted_UDPOut[i][1]
        # print UDPPorts[sorted_UDPIn[i][0]] + "/" + sorted_UDPIn[i][0] + " \t: " + str(sorted_UDPIn[i][1])
    csvf.write("Other," + str(otherudpout) + "\n")


    csvf.write("\nUDP Inbound ports\n")
    csvf.write("Port,Count\n")
    #f.write("\nOutbound TCP Ports (port name/port number : bytes)\n")
    #print "\nOutbound TCP Ports (port name/port number : bytes)"



    for i in range(len(sorted_UDPIn) - 1, len(sorted_UDPIn) - 12, -1):
        #f.write(UDPPorts[sorted_UDPIn[i][0]] + "/" + sorted_UDPIn[i][0] + " \t: " + str(sorted_UDPIn[i][1]) + "\n")
        #print UDPPorts[sorted_UDPIn[i][0]] + "/" + sorted_UDPIn[i][0] + " \t: " + str(sorted_UDPIn[i][1])
        csvf.write(UDPPorts[sorted_UDPIn[i][0]] + "," + str(sorted_UDPIn[i][1])+"\n")
    otherudpin = 0
    for i in range(0,len(sorted_UDPIn)-11):
        otherudpin += sorted_UDPIn[i][1]
        #print UDPPorts[sorted_UDPIn[i][0]] + "/" + sorted_UDPIn[i][0] + " \t: " + str(sorted_UDPIn[i][1])
    csvf.write("Other," + str(otherudpin) + "\n")


    f.close()
    csvf.close()

def newWrite():
    sorted_TCPIn = sorted(TCPIncoming.items(), key=operator.itemgetter(1))
    sorted_UDPIn = sorted(UDPIncoming.items(), key=operator.itemgetter(1))

    csvf = open("task3csvnew.csv", "w")
    for i in sorted_TCPIn:

        csvf.write(str(i[0])+","+TCPPorts[i[0]] + "," + str(i[1])+"\n")
    csvf.write("\n\n")
    for j in sorted_UDPIn:

        csvf.write(str(j[0])+","+UDPPorts[j[0]] + "," + str(j[1]) + "\n")

def main():
    readinPortFile()
    fileDirs = t1.readDir()
    #run over files
    filecount = 1
    for fle in fileDirs:
        print "File " + str(filecount) + "/170"
        #runIpSumDump(fle)
        basicCommand(fle)
        filecount += 1

    # remove inits
    del TCPIncoming[""]
    del TCPOutgoing[""]
    del UDPOutgoing[""]
    del UDPIncoming[""]
    #writeToFile("task3output.txt")
    newWrite()

if __name__ == '__main__':
    main()
