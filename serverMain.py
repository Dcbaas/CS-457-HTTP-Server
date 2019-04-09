#!/usr/bin/python

import HttpServer
import getopt
import sys

data = getopt.getopt(sys.argv[1:], 'p:d:l:')
print(data)
#server = HttpServer.HttpServer()
#server.run()
