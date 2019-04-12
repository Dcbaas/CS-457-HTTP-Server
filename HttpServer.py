import os
import sys
import socket
import select
import time
from enum import Enum

class HttpServer:
    def __init__(self, portNum, docRoot, logFile):
        self.socketList = []
        self.socketIPMapping = {}
        self.socketTimeMapping = {}

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
                self.socketTimeMapping.update({clientSocket:time.time()})
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
                    requestType = requestLine[0].split(' ')[0]
                    if requestType != 'GET':
                        #Send a 501
                        continue

                    fileDetail = requestLine[0].split(' ')[1]
                    fileDetail = self.filePath + fileDetail
                    for line in requestLine:
                        if line == requestLine[0]:
                            continue
                        else:
                            splitLine = line.split(':', 1)
                            if len(splitLine) == 2:
                                httpDict.update({splitLine[0]:splitLine[1]})
                    response = self.send200(fileDetail, httpDict)
                    socket.send(response)
                    continue
            for socket in self.socketList:
                if socket == self.serverSocket or socket == sys.stdin:
                    continue
                startTime = self.socketTimeMapping[socket]
                currentTime = time.time()
                elapsed = currentTime - startTime
                if elapsed > 20:
                    socket.close()
                    self.socketList.remove(socket)
                    del self.socketIPMapping[socket]
                    del self.socketTimeMapping[socket]

    def send404(self):
        file = open('customHTML/404.html', 'rb')
        fileContents = file.read()
        file.close()
        contentType = 'text/html; charset=utf-8'
        contentLength = len(fileContents)
        date = time.asctime(time.gmtime())

        httpHeader = 'HTTP/1.1 404 NOT FOUND \r\n'
        httpHeader = httpHeader + 'Content-type: ' + contentType + ' \r\n'
        httpHeader = httpHeader + 'Content-length: ' + str(contentLength) + ' \r\n'
        httpHeader = httpHeader + 'Date: ' + date + ' \r\n'
        httpHeader = httpHeader + ' \r\n'
        httpResponse = httpHeader.encode() + fileContents
        return httpResponse

        return
    def send501(self):
        return
    def send200(self, fileDetail, httpDict):
        fileContents = None
        fileExtension = self.getExtension(fileDetail)
        lastModifiedTime = self.getLastModified(fileDetail)
        contentType = 'text/html; charset=utf-8'

        file = open(fileDetail, 'rb')
        fileContents = file.read()
        file.close()

        contentLength = len(fileContents)
        date = time.asctime(time.gmtime())
        #construct the httpHeader
        httpHeader = 'HTTP/1.1 200 OK \r\n'
        httpHeader = httpHeader + 'Date: ' + date + ' \r\n'
        httpHeader = httpHeader + 'Content-type: ' + contentType + ' \r\n'
        httpHeader = httpHeader + 'Content-length: ' + str(contentLength) + ' \r\n'
        httpHeader = httpHeader + 'Last-modified: ' + lastModifiedTime + ' \r\n'
        httpHeader = httpHeader + '\r\n'
        httpResponse = httpHeader.encode() + fileContents
        return httpResponse

    def getExtension(self, fileDetail):
        detailSplit = fileDetail.split('.')
        return detailSplit[len(detailSplit)-1]

    def getLastModified(self, fileDetail):
        raw_time = os.path.getmtime(fileDetail)
        return time.asctime(time.gmtime(raw_time))

    def compareTimeStamps(clientLastModified, serverLastModified):
        clientRaw = time.mktime(time.strptime(clientLastModified))
        serverRaw = time.mktime(time.strptime(serverLastModified))
        print(clientRaw)
        print(serverRaw)
        return serverRaw < clientRaw

class ContentTypes(Enum):
    IMAGE_FILE = {'jpeg': {'content-type':'image/jpeg'}}
    HTML_FILE = {'html': {'content-type':'text/html'}}
    TEXT_FILE ={'txt': {'content-type':'text/plain'}}
    PDF_FILE = {'pdf': {'Content-type': 'application/pdf'}}

