#!/usr/bin/python3
import notify2
import subprocess
import time
import dlistFile

messageIndex = {}

def messagePush(roomid,message):
    systemMessage(roomid,message)
    shellMessage(message)
    pass

def systemMessage(roomid,message):
    notify2.init("弹幕姬")
    dlistPush = notify2.Notification("弹幕姬",message)
    dlistPush.show()
    if message in messageIndex.keys():
        messageIndex[message] = int(messageIndex[message]) + 1
    else:
        messageIndex[message] = 0
    while messageIndex[message] == 20:
        messageIndex[message] = 0
        dlistFile.removeDlistKey(roomid,message)
    pass

def shellMessage(message):
    subprocess.call("echo '弹幕姬 \n" + message + "'", shell=True)
    pass

def dlistsay(roomid):
    dlist = dlistFile.readDist(roomid)
    try:
        dlistMax = len(dlist)
    except TypeError:
        pass
    else:
        dlistStr = ""
        dlistStrList = []
        if dlistMax >= 10:
            for i in range(dlistMax-10, dlistMax):
                dlistStrList.append(dlist[i])
            dlistStr = '\n'.join(dlistStrList)
            messagePush(roomid,dlistStr)
        elif dlistMax >=50:
            for i in range(dlistMax-10, dlistMax):
                dlistStrList.append(dlist[i])
            dlistStr = '\n'.join(dlistStrList)
            dlistFile.removerDlist(roomid)
            messagePush(roomid,dlistStr)
        else:
            dlistStr = '\n'.join(dlist)
            messagePush(roomid,dlistStr)
    pass