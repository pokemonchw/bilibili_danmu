#!/usr/bin/python3
import notify2
import subprocess
import time
import CacheContorl


notify2.init("弹幕姬")
dlistPush = notify2.Notification("弹幕姬", '弹幕姬启动完成')

def systemMessage(message):
    dlistPush.update('弹幕姬',message)
    dlistPush.show()

def shellMessage(message):
    subprocess.call("echo '弹幕姬 \n" + message + "'", shell=True)

def dlistsay():
    while(len(CacheContorl.message_data.keys()) >= 9):
        del CacheContorl.message_data[list(CacheContorl.message_data.keys())[0]]
    messageStr = ''
    messageShellStr = ''
    for message in CacheContorl.message_data:
        messageStr += message + '\n'
        if CacheContorl.message_data[message] == 0:
            messageShellStr += message + '\n'
        CacheContorl.message_data[message] += 1
        if CacheContorl.message_data[message] >= 199:
            del CacheContorl.message_data[message]
    if messageStr != '':
        systemMessage(messageStr)
    if messageShellStr != '':
        shellMessage(messageShellStr)
