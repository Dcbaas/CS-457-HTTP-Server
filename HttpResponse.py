import time

class HttpResponseHeader:
    def __init__(self, responseCode, responseMessage, contentLength, contentType, lastModified):
        self.HTTP_VERSION = 'HTTP/1.1'
        self.responseCode = responseCode
        self.responseMessage = responseMessage
        self.contentLength = 0
        self.contentType = contentType
        self.lastModified = lastModified
        self.date = time.asctime(time.gmtime())

