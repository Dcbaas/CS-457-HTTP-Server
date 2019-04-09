import os
import sys
import socket
import select

class HttpServer:
    def __init__(self, portNum = 8008, docRoot = './', logFile = ''):
        self.socketList = []
        self.socketIPMapping = {}

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('', portNum))
        self.serverSocket.listen(15)

        self.socketList.append(self.serverSocket)
        self.socketList.append(sys.stdin)

        if not os.path.exists(docRoot):
            serverSocket.close()
            print('The docRoot specified does not exist')
            exit(1)
        else:
            self.filePath = os.path.join(docRoot)

        if logFile != '':
            sys.stdout = open(logFile, 'w')

        if logFile == '':
            self.logFile = sys.stdout
        else:
            self.logFile = open(logFile, 'w')


    def printLog(self, message):
        if self.logFile == sys.stdout:
            print(message)
        else:
            print(message)
            self.logFile.write(message + '\n')
    
    def run(self):
        while True:
            readyToRead, readyToWrite, hasError = \
                    select.select(
                            self.socketList,
                            self.socketList,
                            self.socketList)
            if self.serverSocket in readyToRead:
                (clientSocket, clientAddress) = self.serverSocket.accept()
                self.socketList.append(clientSocket)
                self.socketIPMapping.update({clientSocket:clientAddress})
            elif sys.stdin in readyToRead:
                for line in sys.stdin:
                    line = line.strip()
                    if line == '!quit':
                        #do quit stuff
                        print('quit command called. Shame it doesn\'t work bitch')
            else:
                for socket in readyToRead:
                    httpDict = {}
                    request = socket.recv(2400).decode()
                    requestLine = request.split('\r\n')
                    fileDetail = requestLine[0].split(' ')[1]
                    for line in requestLine:
                        if line == requestLine[0]:
                            continue
                        else:
                            print('here1')
                            print(line.encode())
                            splitLine = line.split(':', 1)
                            httpDict.update({splitLine[0]:splitLine[1]})

                    print('Getting file: ' + fileDetail)
                    print(httpDict)

