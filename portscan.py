import socket, sys, random, threading

#---global---
locky = threading.Lock()
master = []
numThreads = 0


class Scanner(threading.Thread):
    def __init__(self, addr, portList):
        threading.Thread.__init__(self)
        self.addr = addr
        self.portList = portList
        self.master = []
    def run(self):
        global locky
        print("Scanning: "+self.addr)
        for port in self.portList:
            if(scan(self.addr, port)):
                self.master.append([self.addr, port])
        global numThreads
        global master
        locky.acquire()
        master.extend(self.master)
        numThreads=numThreads-1
        locky.release()
        print("Thread for", self.addr, "ending now")
        
        

def scan(address, port):
    s = socket.socket()
    s.settimeout(1.0)
    try:
        s.connect((address, port))
        return True 
    except socket.error:
        return False
    except socket.timeout:
        return False
    s.close()

def scanRange(ip, numComputers, portList):
    count=0
    global master
    global numThreads
    addr = ip
    while count < numComputers:
        if numThreads < 60:
            numThreads = numThreads + 1 # this may be a race condition
            Scanner(addr, portList).start()
            addr = incr(addr.split("."))
            count = count+1
    while (numThreads != 0):
        #print(numThreads)
        derp = False
    print("Done scanning")
    return master


def incr(ip):
    d = int(ip[3])+1
    c = int(ip[2])
    b = int(ip[1])
    a = int(ip[0])
    if(d==256):
        c = c+1
        d=0
        if(c==256):
            b= b+1
            c=0
            if(b==256):
                a=a+1
                b=0
                if(a==256):
                    print("Fuck you >__>")
    return str(a) +"."+ str(b) +"."+ str(c) +"."+ str(d)


def listDump(name, ipList):
    try:
        filehandle = open(name, "w")
    except IOError:
        print("Can't dump ips")
        return
    for ip in ipList:
        filehandle.write(ip[0]+" "+str(ip[1])+"\n")
    filehandle.close()

def scanner(ip, num, ports):
    listDump(ip+str(num)+".txt", scanRange(ip, num, ports))

print("Welcome to the port scanner I wrote in like 15 minutes.")
choice = input("Pick a type of scan: scan, random, (or type help) : ")
if(choice == "scan"):
    I = input("Input a starting ip address ")
    N = int(input("Input the number of computers you want to scan "))
    tempP = input("Input a list of ports you want to be scanned seperated by a comma (but no spaces, I'm lazy) ").split(",")
    P=[]
    for eh in tempP:
        P.append(int(eh))
elif(choice == "random"):
    N = random.randint(10, 200)
    P = [21, 80]
    I=str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
else:
    print("scan: scan a specific range of computers.")
    print("random: scans a random set of computers, and scans 10-200 computers")
    print("help: prints this message")
    exit(0)
fileName = input("Input a filename you want me to dump the results to (or - to use standard output) (just hit return to default) ")
data = scanRange(I, N, P)
if(fileName == "-"):
    for line in data:
        print(line[0]+" "+str(line[1]))
if(fileName == ""):
    listDump(I+str(N)+".txt", data)
else:
    listDump(fileName, data)
    
