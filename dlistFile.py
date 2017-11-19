import os

def writeDlist(danmu,roomid):
    baseDir = os.path.dirname(__file__)
    filePath = os.path.join(baseDir,'dlistData',str(roomid))
    if os.path.exists(filePath) and os.path.isfile(filePath):
        file = open(filePath, 'a', encoding='utf-8')
        file.write(danmu)
        file.close()
    else:
        file = open(filePath, 'w', encoding='utf-8')
        file.write(danmu)
        file.close()
    pass

def readDist(roomid):
    baseDir = os.path.dirname(__file__)
    filePath = os.path.join(baseDir, 'dlistData', str(roomid))
    linelist = []
    if os.path.exists(filePath) and os.path.isfile(filePath):
        with open(filePath,'r') as f:
            for line in f.readlines():
                linestr = line.strip()
                linelist.append(linestr)
            return linelist
    else:
        open(filePath,'w')
    pass