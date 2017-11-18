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
    earthMonitorPush = notify2.Notification("弹幕姬",message)
    earthMonitorPush.set_hint("x",10)
    earthMonitorPush.set_hint("y",10)
    earthMonitorPush.show()
    pass

def shellMessage(message):
    subprocess.call("echo '弹幕姬 \n" + message + "'", shell=True)
    pass

def dlistsay(roomid):
    dlist = dlistFile.readDist(roomid)
    dlistMax = len(dlist)
    dlistStr = ""
    if dlistMax >= 20:
        for i in range(dlistMax - 20,dlistMax):
            dlistStr = dlistStr + dlist[i]
    else:
        for i in range(0,dlistMax):
            dlistStr = dlistStr + dlist[i]
    messagePush(dlistStr)
    time.sleep(10)
    pass