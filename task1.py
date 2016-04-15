#VHLAND002
#python file for task1
#Extract ICMP messages


import subprocess as sp


#p = sp.Popen(('tcpdump', '-l','-nn','-r', 'eth1_eth2_20110207003505', 'icmp'), stdout=sp.PIPE)#gives full line
p = sp.Popen(('tcpdump', '-l','-nn', '-r', 'eth1_eth2_20110207003505', 'icmp', '|', 'cut', '-f', '3', '-d', '" "', '|', 'head'), stdout=sp.PIPE)#cuts
for row in iter(p.stdout.readline, b''):
    print row.rstrip()
    #what we need to do:
        #from position 6 until we hit a , is what we are looking for
        #take output and split it into this part
            #first split into array
            #then use relevant parts
        #create dictionary with parts incrementing count when reencountering
            #gives us the count of each thing
            #can be generalized more from there
