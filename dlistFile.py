import os

def writeDlist(danmu,filePath):
    filePath = './dlistData/' + filePath
    if os.path.exists(filePath) and os.path.isfile(filePath):
        file = open(filePath, 'a', encoding='utf-8')
        file.write(danmu + "\n")
        file.close()
    else:
        file = open(filePath, 'w', encoding='utf-8')
        file.write(danmu + "\n")
        file.close()
    pass

def readDist(roomid):
    filePath = './dlistData/' + roomid
    linelist = []
    while os.path.exists(filePath) and os.path.isfile(filePath):
        with open(filePath,'r') as f:
            for line in f.readlines():
                linestr = line.strip()
                linestrlist = linestr.split("\n")
                linelist = map(int, linestrlist)
            return linelist
    pass