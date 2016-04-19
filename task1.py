#VHLAND002
#python file for task 1
#Extract ICMP messages


import subprocess as sp
import os

dicti = {"":0}

def task1(filename):
    #p = sp.Popen(('tcpdump', '-l','-nn','-r', 'eth1_eth2_20110207003505', 'icmp'), stdout=sp.PIPE)#gives full line
    p = sp.Popen(('tcpdump', '-l', '-nn', '-r', "traffic/"+filename, 'icmp'), stdout=sp.PIPE)

    for row in iter(p.stdout.readline, b''):
        #print row.rstrip()
        #split into seperate parts
        splitted = row.split()

        # here we filter out local traffic by removing any errors involving 192.168.x.x and 10.x.x.x IP's
        if splitted[2][0:7] != "192.168" and splitted[2][0:3] != "10.":
            #first element
            message = splitted[5]
            #read out other elements of the ICMP messsage
            for k in range(6,len(splitted)-2):
                message = message + " " + splitted[k]
            #remove comma
            message = message[0:-1]
            #print message
            newMessage = []
            #filter out unnessasary details
            for p in message:
                if not p.isdigit() and p != ".":
                    newMessage.append(p)

            message = ''.join(newMessage)

            #add into dictionary if new and increment count if not
            if dicti.has_key(message):
                dicti[message] += 1
            else:
                dicti[message] = 1

    #print(dicti)
    #remove default entry




for f in os.listdir("./traffic"):
    task1(f)
del dicti[""]
for item in dicti:
    print item + " : " + str(dicti[item])