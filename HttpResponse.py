import time

class HttpResponseHeader:
    def __init__(self, responseCode, responseMessage, detailDict):
        self.formalPacket = ''
        self.HTTP_VERSION = 'HTTP/1.1'
        self.responseCode = responseCode
        self.responseMessage = responseMessage
        self.date = time.asctime(time.gmtime())

    def construct200(self,detailDict):
        return

    def construct304(self,detailDict):
        return

    def construct404(self,detailDict):
        return

    def construct501(self,detailDict):
        return
