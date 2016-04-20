#VHLAND002
#python file for task 3
#Traffic by bytes

import subprocess as sp
import operator
import os
from collections import defaultdict

#ipsumdump -p -S -D -L -r traffic/eth1_eth2_20110207003505


#def filterResults()


UDPIncoming = {"":0}
UDPOutgoing = {"":0}
TCPIncoming = {"":0}
TCPOutgoing = {"":0}

#type, source port, dest port, size
p = sp.Popen(('ipsumdump', '-p', '-S', '-D', '-L', '-r', 'traffic/eth1_eth2_20110207003505'), stdout=sp.PIPE)
for row in iter(p.stdout.readline, b''):
    #print row
    splitted = row.split()


    if splitted[0] == "T":
        keyOut = splitted[1]
        keyIn = splitted[2]
        count = int(splitted[3])
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

    elif splitted[0] == "U":
        keyOut = splitted[1]
        keyIn = splitted[2]
        count = int(splitted[3])
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

# print TCPIncoming
# print "********"
# print TCPOutgoing
# print "********"
# print UDPIncoming
# print "********"
# print UDPOutgoing

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

