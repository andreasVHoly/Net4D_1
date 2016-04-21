#VHLAND002
#python file for task 2
#Bandwidth usage

import subprocess as sp
import task1v2 as t1
import datetime



def readInPackets(filename, outputfilename):
    outgoing = {"": 0}
    incoming = {"": 0}


    print "reading in " + filename
    p = sp.Popen(('ipsumdump', '-t', '-s', '-d', '--wire-length', '-r', filename), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        splitter = row.split()

        if len(splitter) < 4:
            continue
        source = splitter[1]
        dest = splitter[2]
        # check for local traffic

        if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):

            #format time
            #time = datetime.datetime.fromtimestamp(float(splitter[0])).strftime('%Y-%m-%d %H:%M:%S') #for seconds
            time = datetime.datetime.fromtimestamp(float(splitter[0])).strftime('%Y-%m-%d %H:%M')


            #print "time " + str(time)

            if str(time) not in outgoing:
                outgoing[str(time)] = 0
            if str(time) not in incoming:
                incoming[str(time)] = 0



            # check if outgoing or incoming connection
            if t1.isLocal(source):
                # means outgoing
                if str(time) in outgoing:
                    outgoing[str(time)] += int(splitter[3])
            elif t1.isLocal(dest):
                #means incoming
                if str(time) in incoming:
                    incoming[str(time)] += int(splitter[3])
    # delete init
    del incoming[""]
    del outgoing[""]

    f = open(outputfilename+filename[-14:], "w")
    #sort times
    sortedKeys = incoming.keys()
    sortedKeys.sort()
    for i in sortedKeys:
        print str(i) + "\t incoming: " + str(incoming[str(i)]) + " \tbps\t outgoing: " + str(outgoing[str(i)]) + " \tbps"
        f.write(str(i) + "\t incoming: " + str(incoming[str(i)]) + " \tbps\t outgoing: " + str(outgoing[str(i)]) + " \tbps\n")





def main():
    filedirs = t1.readDir()
    ipsumdumpappr = True
    tcpstatappr = False
    for f in filedirs:
        readInPackets(f,"timefiles/timefile-")


if __name__ == '__main__':
    main()