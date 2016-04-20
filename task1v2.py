#tcpdump -r eth1_eth2_20110207003505 'icmp' -w outfile.pcap




import subprocess as sp
import os

dicti = {"":0}
newFileName = "outputfiles/output"

def filterPackets(filename,i):
    p = sp.Popen(('tcpdump', '-r', "traffic/" + filename, 'icmp', '-w', newFileName+str(i)), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        print row

def extractTypeAndCode(filename):

    p = sp.Popen(('ipsumdump', '-r', '--src', '--icmp-type', '--icmp-code',"outputfiles/"+filename), stdout=sp.PIPE)

    for row in iter(p.stdout.readline, b''):
        #print row.rstrip()
        #split into seperate parts
        splitted = row.split()
        if (len(splitted) == 3):

             # here we filter out local traffic by removing any errors involving 192.168.x.x and 10.x.x.x IP's
            if splitted[0][0:7] != "192.168" and splitted[0][0:3] != "10.":

                #add into dictionary if new and increment count if not
                message = str(splitted[1]) + "," + str(splitted[2])
                if (str(splitted[1]).isdigit()):
                    if dicti.has_key(message):
                        dicti[message] += 1
                    else:
                        dicti[message] = 1




index = 0
for f in os.listdir("./traffic"):
    filterPackets(f,index)
    index += 1

for k in os.listdir("./outputfiles"):
    extractTypeAndCode(k)

del dicti[""]
for item in dicti:
    print item + " : " + str(dicti[item])