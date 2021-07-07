import asyncio
import random
import time
import messagepush
import CacheContorl
import requests
import threading
from struct import unpack, pack


class bilibiliClient():
    """ b站直播间链接对象 """

    def __init__(self):
        """ 初始化对象 """
        self.api_url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        """ 获取弹幕列表的api地址 """
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        }
        """ 请求头 """
        self.room_id = int(input())
        """ 当前直播间id """
        self.data = {
            'roomid': self.room_id,
            'csrf_token': '',
            'csrf': '',
            'visit_id': '',
        }
        """ 调用api所需数据 """
        self.log_file_write = open('danmu.log', mode='a', encoding='utf-8')
        """ 日志文件 """
        log_file_read = open('danmu.log', mode='r', encoding='utf-8')
        self.log = set(log_file_read.readlines())
        """ 当前弹幕日志 """
        self.chat_port = 788
        """ websocket的连接端口 """
        self._protocolversion = 1
        """ websocket的数据协议 """
        self._reader: asyncio.StreamReader = None
        """ websocket的数据读取器 """
        self._writer: asyncio.StreamWriter = None
        """ websocket协议的写入器 """
        self.connected = False
        """ websocket是否已成功链接 """
        self.user_count = 0
        """ 当前直播间人气 """
        self._chat_host = 'livecmt-1.bilibili.com'
        """ websocket服务的链接地址 """

    async def connectServer(self):
        print('正在进入房间。。。。。')
        reader, writer = await asyncio.open_connection(self._chat_host, self.chat_port)
        self._reader = reader
        self._writer = writer
        print('链接弹幕中。。。。。')
        if (await self.SendJoinChannel(self.room_id)):
            print("连接弹幕池成功")
            self.connected = True
            tA = threading.Thread(target=self.get_danmu)
            tA.start()
            tB = threading.Thread(target=self.dlist_message_push)
            tB.start()
            await self.ReceiveMessageLoop()

    async def SendJoinChannel(self, channelId):
        self._uid = (int)(100000000000000.0 + 200000000000000.0*random.random())
        body = '{"roomid":%s,"uid":%s}' % (channelId, self._uid)
        await self.SendSocketData(0, 16, self._protocolversion, 7, 1, body)
        return 1

    async def ReceiveMessageLoop(self):
        while self.connected:
            tmp = await self._reader.read(4)
            expr, = unpack('!I', tmp)
            tmp = await self._reader.read(2)
            tmp = await self._reader.read(2)
            tmp = await self._reader.read(4)
            num, = unpack('!I', tmp)
            tmp = await self._reader.read(4)
            num2 = expr - 16

            if num2 != 0:
                num -= 1
                if num in {0, 1, 2}:
                    tmp = await self._reader.read(4)
                    num3, = unpack('!I', tmp)
                    print('房间人数为 %s' % num3)
                    self._userCount = num3
                    continue
                elif num in {3, 4}:
                    tmp = await self._reader.read(num2)
                    try: # 为什么还会出现 utf-8 decode error??????
                        messages = tmp.decode('utf-8')
                        self.parse_cmd()
                    except Exception:
                        continue
                    continue
                elif num in {5, 6, 7}:
                    tmp = await self._reader.read(num2)
                    continue
                else:
                    if num != 16:
                        tmp = await self._reader.read(num2)
                    else:
                        continue

    def get_danmu(self):
        """ 获取弹幕数据 """
        while 1:
            html = requests.post(url=self.api_url, headers=self.headers, data=self.data).json()
            self.parse_danmu(html)
            time.sleep(1)

    async def HeartbeatLoop(self):
        while not self.connected:
            await asyncio.sleep(0.5)

        while self.connected:
            await self.SendSocketData(0, 16, self._protocolversion, 2, 1, "")
            await asyncio.sleep(30)

    async def SendSocketData(self, packetlength, magic, ver, action, param, body):
        bytearr = body.encode('utf-8')
        if packetlength == 0:
            packetlength = len(bytearr) + 16
        sendbytes = pack('!IHHII', packetlength, magic, ver, action, param)
        if len(bytearr) != 0:
            sendbytes = sendbytes + bytearr
        self._writer.write(sendbytes)
        await self._writer.drain()

    def parse_danmu(self, data:dict):
        """
        解析弹幕记录数据
        Keyword arguments:
        data -- 弹幕记录数据
        """
        for content in data['data']['room']:
            nickname = content['nickname']
            text = content['text']
            timeline = content['timeline']
            log = timeline + ":" + nickname + ':' + 'say: ' + text + " \n"
            danmu = nickname + ':' + 'say: ' + text + " \n"
            if log not in self.log:
                CacheContorl.message_data[danmu] = 0
                self.log_file_write.write(log)
                self.log.add(log)

    def parse_cmd(self, message:str):
        """
        解析直播间实时消息
        Keyword arguments:
        message -- 消息json
        """
        try:
            dic = json.loads(messages)
        except: # 有些情况会 jsondecode 失败，未细究，可能平台导致
            return
        cmd = dic['cmd']
        if cmd == 'LIVE':
            print ('直播开始。。。')
            return
        if cmd == 'PREPARING':
            print ('房主准备中。。。')
            return
        if cmd == 'SEND_GIFT' and config.TURN_GIFT == 1:
            GiftName = dic['data']['giftName']
            GiftUser = dic['data']['uname']
            Giftrcost = dic['data']['rcost']
            GiftNum = dic['data']['num']
            try:
                print(GiftUser + ' 送出了 ' + str(GiftNum) + ' 个 ' + GiftName)
            except:
                pass
            return
        if cmd == 'WELCOME' and config.TURN_WELCOME == 1:
            commentUser = dic['data']['uname']
            try:
                print ('欢迎 ' + commentUser + ' 进入房间。。。。')
            except:
                pass
            return
        return

    def dlist_message_push(self):
        while 1:
            messagepush.dlistsay()
            time.sleep(1)
