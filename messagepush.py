#!/usr/bin/python3
import notify2
import subprocess
import time
import dlistFile

def messagePush(message):
    systemMessage(message)
    shellMessage(message)
    pass

def systemMessage(message):
    notify2.init("弹幕姬")
    dlistPush = notify2.Notification("弹幕姬",message)
    dlistPush.show()
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
            print(dlistStr)
            messagePush(dlistStr)
        else:
            dlistStr = '\n'.join(dlist)
            print(dlistStr)
            messagePush(dlistStr)
    pass