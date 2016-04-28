#VHLAND002
#python file for task 2
#Bandwidth usage

import subprocess as sp
import task1v2 as t1
import datetime

csvFile = open("task2output.csv","w")

def readInPackets(filename, outputfilename):
    outgoing = {"": 0}
    incoming = {"": 0}


    print "reading in " + filename
    # command
    p = sp.Popen(('ipsumdump', '-t', '-s', '-d', '--wire-length', '-r', filename), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        splitter = row.split()
        # discard invalid output
        if len(splitter) < 4:
            continue
        source = splitter[1]
        dest = splitter[2]
        # check for local traffic

        if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):

            #format time
            #time = datetime.datetime.fromtimestamp(float(splitter[0])).strftime('%Y-%m-%d %H:%M:%S') #for seconds
            #time = datetime.datetime.fromtimestamp(float(splitter[0])).strftime('%Y-%m-%d %H:%M')
            time = datetime.datetime.fromtimestamp(float(splitter[0])).strftime('%Y-%m-%d %H')


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
    # open file
    f = open(outputfilename+filename[-14:], "w")
    # sort times
    sortedKeys = incoming.keys()
    sortedKeys.sort()
    # output
    for i in sortedKeys:
        #print str(i) + "\t incoming: " + str(incoming[str(i)]) + " \tbps\t outgoing: " + str(outgoing[str(i)]) + " \tbps"
        #f.write(str(i) + "\t incoming: " + str(incoming[str(i)]) + " \tbps\t outgoing: " + str(outgoing[str(i)]) + " \tbps\n")
        splitDate = str(i).split(" ")
        csvFile.write(splitDate[0] + "," + splitDate[1] + ":00:00" + "," + str(incoming[str(i)]) + "," + str(outgoing[str(i)]) + "\n")

    f.close()




def main():
    # create coloumn headers for csv file
    csvFile.write("Date,Time,Download,Upload\n")
    filedirs = t1.readDir()
    count = 1
    for f in filedirs:
        print "Processing " + str(count) + " /170"
        readInPackets(f,"timefiles/timefile-")
        count +=1
    csvFile.close()


if __name__ == '__main__':
    main()