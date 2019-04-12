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
        if '-p' in arg[0]:
            defaultPort = int(arg[0][1])
        elif '-d' in arg[0]:
            defaultDoc = arg[0][1]
        elif '-l' in arg[0]:
            defaultLog = arg[0][1]
        else:
            print('Error: invaild flag')
            exit(1)
server = HttpServer.HttpServer(defaultPort, defaultDoc, defaultLog)
server.run()

