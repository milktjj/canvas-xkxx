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
import audio

file_heap = []
executor = ThreadPoolExecutor(max_workers=100)


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
    ifilename = './'+generate_random_string(10) + '.pcm'
    print(ifilename)
    with open(ifilename, 'wb') as file:
        file.write(data)
    heapq.heappush(file_heap, (int(time.time() * 1000), ifilename))
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
        merged_file = open(merged_file_path, "wb")

        for file_path in sorted_files:
            with open(file_path, "rb") as file:
                data = file.read()
                merged_file.write(data)
                if os.path.exists(file_path):
                    os.remove(file_path)
        merged_file.close()
        try:
            audio.pcm_to_s3(merged_file_path)
        except Exception as e:
            print(str(e))


def generate_random_string(length):
    # 从大小写字母和数字中生成随机字符
    characters = string.ascii_letters + string.digits
    # 使用random.choice()函数从字符集中随机选择字符，并将它们组合在一起
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def run_websocket_server():
    server = SimpleWebSocketServer('', 8765, SimpleEcho)
    server.serveforever()
