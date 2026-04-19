import time,os

def getFileModifyTime(filePath):
    if os.path.isfile(filePath):
        _ = time.strftime('%Y-%m-%d %H:%M:%S', \
                                time.localtime(os.path.getmtime(filePath)))
        return _