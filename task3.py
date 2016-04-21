#VHLAND002
#python file for task 3
#Traffic by bytes

import subprocess as sp
import operator


import task1v2 as t1




UDPIncoming = {"":0}
UDPOutgoing = {"":0}
TCPIncoming = {"":0}
TCPOutgoing = {"":0}

#type, source port, dest port, size
p = sp.Popen(('ipsumdump', '-p', '-s', '-d', '-S', '-D', '-L', '-r', 'traffic/eth1_eth2_20110207201002'), stdout=sp.PIPE)
for row in iter(p.stdout.readline, b''):
    #print row
    splitted = row.split()
    #ensure we have apcket information
    if len(splitted) == 6:
        #filter out local traffic

        source = splitted[1]
        dest = splitted[2]

        if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):
            #if we have a tcp conn
            if splitted[0] == "T":
                #get values
                keyOut = splitted[3]
                keyIn = splitted[4]
                count = int(splitted[5])
                #incoming connection
                if TCPIncoming.has_key(keyIn):
                    TCPIncoming[keyIn] += count
                else:
                    TCPIncoming[keyIn] = count
                #outgoing connection
                if TCPOutgoing.has_key(keyOut):
                    TCPOutgoing[keyOut] += count
                else:
                    TCPOutgoing[keyOut] = count
            #if we have a udp conn
            elif splitted[0] == "U":
                #get values
                keyOut = splitted[3]
                keyIn = splitted[4]
                count = int(splitted[5])
                # incoming connection
                if UDPIncoming.has_key(keyIn):
                    UDPIncoming[keyIn] += count
                else:
                    UDPIncoming[keyIn] = count
                # outgoing connection
                if UDPOutgoing.has_key(keyOut):
                    UDPOutgoing[keyOut] += count
                else:
                    UDPOutgoing[keyOut] = count

#remove inits
del TCPIncoming[""]
del TCPOutgoing[""]
del UDPOutgoing[""]
del UDPIncoming[""]

#sort dictionaries
sorted_TCPOut = sorted(TCPOutgoing.items(), key=operator.itemgetter(1))
sorted_TCPIn = sorted(TCPIncoming.items(), key=operator.itemgetter(1))
sorted_UDPOut = sorted(UDPOutgoing.items(), key=operator.itemgetter(1))
sorted_UDPIn = sorted(UDPIncoming.items(), key=operator.itemgetter(1))


for i in range(len(sorted_TCPOut)-10,len(sorted_TCPOut)):
    print sorted_TCPOut[i]
print "********************************"
for i in range(len(sorted_TCPIn) - 10, len(sorted_TCPIn)):
    print sorted_TCPIn[i]
print "********************************"
for i in range(len(sorted_UDPOut)-10,len(sorted_UDPOut)):
    print sorted_UDPOut[i]
print "********************************"
for i in range(len(sorted_UDPIn)-10,len(sorted_UDPIn)):
    print sorted_UDPIn[i]

