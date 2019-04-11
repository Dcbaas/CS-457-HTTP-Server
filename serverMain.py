#!/usr/bin/python

import HttpServer
import getopt
import sys

defaultPort = 8008
defaultDoc = './'
defaultLog = ''

args = getopt.getopt(sys.argv[1:], 'p:d:l:')
for arg in args:
    if len(arg) != 0:
        if arg[0] == '-p':
            defaultPort = int(arg[1])
        elif arg[0] == '-d':
            defaultDoc = arg[1]
        elif arg[0] == '-l':
            defaultLog = arg[1]
        else:
            print('Error: invaild flag')
            exit(1)
server = HttpServer.HttpServer(defaultPort, defaultDoc, defaultLog)
server.run()

