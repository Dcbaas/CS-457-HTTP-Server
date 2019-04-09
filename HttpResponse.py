import time

class HttpResponse:
    def __init__(self):
        self.HTTP_VERSION = 'HTTP/1.1'
        self.responseCode = 404
        self.contentMessage = 'Not Found'
        self.contentLength = 0
        self.date = time.asctime(time.gmtime())
        self.content = ''

