# import asyncio
# import websockets
#
#
# async def hello(websocket, path):
#     # 接收客户端的消息
#     print(path)
#     message = await websocket.recv()
#     print(f"Received from client: {message}")
#
#     # 向客户端发送消息
#     response = "Hello, client!"
#     await websocket.send(response)
#
#
# def startWS():
#     start_server = websockets.serve(hello, "localhost", 8765)
#
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from concurrent.futures import ThreadPoolExecutor
import random
import string
import os
import heapq
import time
import config
import requests
import audio
import numpy as np

file_heap = []
executor = ThreadPoolExecutor(max_workers=1000)


class SimpleEcho(WebSocket):

    def handleMessage(self):
        try:
            executor.submit(handleData, self.data, self.opcode, self.address)
        except Exception as e:
            print(str(e))
        self.sendMessage('1')

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


def handleData(data, opcode, address):
    print("rev", len(data), opcode, address)
    if opcode == 1:
        print("rev str")
        return
    ifilename = './'+generate_random_string(10) + '.pcm'
    print(ifilename)
    try:
        with open(ifilename, 'wb') as file:
            file.write(process_data(data))
        heapq.heappush(file_heap, (int(time.time() * 1000), ifilename))
    except Exception as e:
        print(str(e))
    print(len(file_heap))
    heap_size_triger = config.get_config_info()['fileLen']
    if len(file_heap) >= heap_size_triger:
        file_list = []
        for _ in range(heap_size_triger):
            if file_heap:
                timestamp, filename = heapq.heappop(file_heap)
                print(filename)
                file_list.append(filename)
            else:
                break
        sorted_files = sorted(file_list)

        merged_file_path = "./temp.pcm"
        merged_file = open(merged_file_path, "ab+")

        for file_path in sorted_files:
            with open(file_path, "rb") as file:
                data = file.read()
                merged_file.write(data)
                if os.path.exists(file_path):
                    os.remove(file_path)
        merged_file.close()
        try:
            sendToSJTU(merged_file_path)
        except Exception as e:
            print(str(e))


def process_data(pcm_data):
    binary_data = np.frombuffer(pcm_data, dtype=np.int16)
    average = np.mean(binary_data)

    if np.abs(average) < 1500:
        pcm_data = pcm_data[1:]
    if len(pcm_data) % 2 == 1:
        pcm_data = pcm_data[:-1]
    return pcm_data 


def sendToSJTU(merged_file_path):
    try:
        url = "https://lms.sjtu.edu.cn/xk/uploadB"
        payload = {}
        files = [
            ('pcm', ('serial_data.pcm', open(
                merged_file_path, 'rb'), 'application/octet-stream'))
        ]
        headers = {}
        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files)

        print(response.text)
    except Exception as e:
        print(str(e))
    finally:
        if os.path.exists(merged_file_path):
            os.remove(merged_file_path)
        print("finally")


def generate_random_string(length):
    # 从大小写字母和数字中生成随机字符
    characters = string.ascii_letters + string.digits
    # 使用random.choice()函数从字符集中随机选择字符，并将它们组合在一起
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def run_websocket_server():
    server = SimpleWebSocketServer('', 80, SimpleEcho)
    server.serveforever()
