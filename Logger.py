import time

class Logger:
    def __init__(self, outFile = ''):
        self.filename = outFile
        self.writingFile = False

        startTime = time.asctime(time.localtime())

        if self.filename != '':
            file = open(self.filename, 'w')
            file.write('Server Log starting from ' + startTime)
            file.close()
            self.writingFile = True
        return

    def addLog(self, text):
        logTime = time.asctime(time.localtime())

        logText ='\n\nEntry: ' + logTime + '\n' + text
        logText = logText.replace('\r','')

        self.printLog(logText)

        if self.writingFile:
            self.appendLogFile(logText)

        return

    def printLog(self, text):
        print(text)
        return

    def appendLogFile(self, text):
        file = open(self.filename, 'a')
        file.write(text)
        file.close
        return


