#VHLAND002
#python file for task 4
#http trafiic


import subprocess as sp
import operator


import task1 as t1


domains = {"":0}


def runCommand(filename):
    #run command
    counter = 0
    print "trying to read file: " + filename
    p = sp.Popen(('httpry', '-r', filename), stdout=sp.PIPE)
    for row in iter(p.stdout.readline, b''):
        splitter = row.split()
        # we are only looking at get's


        #print splitter
        if splitter[5] != "-":

            # filter out local traffic
            source = splitter[2]
            dest = splitter[3]
            if (t1.isLocal(source) and not t1.isLocal(dest)) or (not t1.isLocal(source) and t1.isLocal(dest)):
                # if "polka" in splitter[6]:
                #     counter += 1
                #     print splitter
                domain = ""
                count = 0
                # if ".co." in splitter[6]:
                #     # we start from the back looking for .
                #     for i in range(len(splitter[6]) - 1, -1, -1):
                #         if splitter[6][i] == "." and count < 2:
                #             count += 1
                #             domain = splitter[6][i] + domain
                #         elif splitter[6][i] == "." and count == 2:
                #             break
                #         else:
                #             domain = splitter[6][i] + domain
                #     domain = "*." + domain
                #     if domain in domains:
                #         domains[domain] += 1
                #     else:
                #         domains[domain] = 1
                #     #print splitter[6]
                # else:
                    # we start from the back looking for .
                for i in range(len(splitter[6])-1, -1, -1):
                    if splitter[6][i] == "." and count == 0:
                        count += 1
                        domain = splitter[6][i] + domain
                    elif splitter[6][i] == "." and count == 1:
                        break
                    else:
                        domain = splitter[6][i] + domain
                domain = "*." + domain
                if domain in domains:
                    domains[domain] += 1
                else:
                    domains[domain] = 1

    return counter

def cleanDomains(filename):
    sortedDomain = sorted(domains.items(), key=operator.itemgetter(1))
    f = file(filename, "w")
    csvf = file("task4_raw.csv", "w")
    csvf.write("Domain Name,Count\n")
    for i in range(len(sortedDomain) - 1, len(sortedDomain) - 15, -1):
        #print sortedDomain[i]
        #f.write(str(sortedDomain[i]) + "\n")
        csvf.write(str(sortedDomain[i][0]) + "," + str(sortedDomain[i][1]) + "\n")

    othercount = 0
    for i in range(0, len(sortedDomain) - 14):
        othercount += sortedDomain[i][1]

    csvf.write("other,"+str(othercount))
    f.close()
    csvf.close()



def main():
    filedirs = t1.readDir()
    filecount = 0
    polkacount = 0
    for f in filedirs:
        print "File " + str(filecount) + "/170"
        polkacount += runCommand(f)
        filecount += 1
    del domains[""]
    #sort domain
    print polkacount
    cleanDomains("task4output.txt")

if __name__ == '__main__':
    main()